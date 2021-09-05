import subprocess
import os
from os import path
from os import makedirs
from shutil import rmtree
from typing import List, Tuple
from copy import deepcopy
from analyze import get_package_name
import tqdm
from bs4 import BeautifulSoup
from copy import deepcopy


class CompileFailureError(Exception):
    pass


class JacocoReportFailureError(Exception):
    pass


class Coverage:
    passed_line: List[int]
    not_passed_line: List[int]
    covered_branch: List[int]
    not_covered_branch: List[int]

    def __init__(self):
        self.passed_line: List[int] = []
        self.not_passed_line: List[int] = []
        self.covered_branch: List[int] = []
        self.not_covered_branch: List[int] = []

    def __str__(self):
        return f"passed:{self.passed_line}, npassed:{self.not_passed_line}, covered:{self.covered_branch}, ncovered:{self.not_covered_branch}"

    def merged(self, merge_coverage: 'Coverage'):
        ret_cov = deepcopy(self)
        for ln in merge_coverage.passed_line:
            if not ln in ret_cov.passed_line:
                ret_cov.passed_line.append(ln)
                ret_cov.not_passed_line.remove(ln)
        ret_cov.passed_line.sort()
        ret_cov.not_passed_line.sort()
        for ln in merge_coverage.covered_branch:
            if not ln in ret_cov.covered_branch:
                ret_cov.covered_branch.append(ln)
                ret_cov.not_covered_branch.remove(ln)
        ret_cov.covered_branch.sort()
        ret_cov.not_covered_branch.sort()
        return ret_cov

    def coverage_percentage(self) -> Tuple[float, float]:
        return (
            len(self.passed_line) / (len(self.passed_line) + len(self.not_passed_line)),
            len(self.covered_branch) / (len(self.covered_branch) + len(self.not_covered_branch))
        )


def make_classpath(additional_classpath: List[str]) -> str:
    class_path = deepcopy(additional_classpath)
    class_path.append("./ext-modules/evosuite-1.1.0.jar")
    class_path.append("./ext-modules/evosuite-standalone-runtime-1.1.0.jar")
    class_path.append("./ext-modules/hamcrest-2.2.jar")
    class_path.append("./ext-modules/junit-4.12.jar")
    if os.name == "nt":
        return ";".join(class_path)
    else:
        return ":".join(class_path)


def compile_testcase(testsource_path: str, class_path: List[str], additional_testsource_path_list: List[str], classfile_dir: str) -> None:
    if path.exists(classfile_dir):
        rmtree(classfile_dir, ignore_errors=True)
    makedirs(classfile_dir)
    proc = subprocess.run(["javac", "-g", "-cp", make_classpath(class_path), "-d", classfile_dir, testsource_path] + additional_testsource_path_list)
    if proc.returncode != 0:
        raise CompileFailureError(f"{testsource_path}のコンパイルに失敗")


def execute_testcase(class_path: List[str], class_name: str, id: int, jacoco_dumpfile_dir: str) -> str:
    if not path.exists(jacoco_dumpfile_dir):
        makedirs(jacoco_dumpfile_dir)
    jacoco_settings = {
        "destfile": path.join(jacoco_dumpfile_dir, f"jacoco{id}.exec"),
        "append": "false",
        "output": "file"
    }
    subprocess.run(["java", jacocoagent_option(jacoco_settings), "-cp", make_classpath(class_path), "org.junit.runner.JUnitCore", class_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return path.join(jacoco_dumpfile_dir, f"jacoco{id}.exec")


def jacocoagent_option(jacoco_settings: dict) -> str:
    retval = "-javaagent:ext-modules/jacoco/lib/jacocoagent.jar="
    settings = []
    for setting_attr, setting_value in jacoco_settings.items():
        settings.append(f"{setting_attr}={setting_value}")
    retval += ",".join(settings)
    return retval


def swap_file_contents(file1_path: str, file2_path: str) -> None:
    with open(file1_path, mode='r') as fp1, open(file2_path, mode='r') as fp2:
        file1_content = fp1.read()
        file2_content = fp2.read()
    with open(file1_path, mode='w') as fp1, open(file2_path, mode='w') as fp2:
        fp1.write(file2_content)
        fp2.write(file1_content)


def get_classfiles_options(class_pathes: List[str]):
    classfiles_options = []
    for c in class_pathes:
        classfiles_options += ["--classfiles", c]
    return classfiles_options


def convert_to_report(jacoco_exec_file_path: str, id: str, dest_dir: str, project_class_path: List[str], project_source_pathes: List[str]) -> None:
    proc = subprocess.run(["java", "-jar", "ext-modules/jacoco/lib/jacococli.jar", "report", jacoco_exec_file_path] + get_classfiles_options(project_class_path) + ["--html", dest_dir, "--name", f"jacoco{id}_report", "--sourcefiles", ";".join(project_source_pathes)], stdout=subprocess.DEVNULL)
    if proc.returncode != 0:
        raise JacocoReportFailureError


def measure_coverage(alone_test_path_list: List[str], original_test_path: str, tested_source_path: str, project_class_path: List[str], project_source_path: List[str], class_name: str, classfile_dir: str, jacoco_dumpfile_dir: str, jacoco_report_dir: str, additional_testsource_path_list: List[str] = []):
    coverage_list: List[Coverage] = []
    for i, alone_test_path in enumerate(tqdm.tqdm(alone_test_path_list)):
        swap_file_contents(alone_test_path, original_test_path)
        try:
            compile_testcase(original_test_path, project_class_path, additional_testsource_path_list, classfile_dir)
            jacoco_exec_file_path = execute_testcase(project_class_path + [classfile_dir], class_name, i, jacoco_dumpfile_dir)
            convert_to_report(jacoco_exec_file_path, i, path.join(jacoco_report_dir, f"test{i}"), project_class_path, project_source_path)
            package_name = get_package_name(original_test_path)
            coverage_list.append(get_line_coverage_info(path.join(jacoco_report_dir, f"test{i}", package_name, f"{path.basename(tested_source_path)}.html")))
            swap_file_contents(alone_test_path, original_test_path)
        except:
            swap_file_contents(alone_test_path, original_test_path)
            raise
    return coverage_list


def get_line_coverage_info(html_path: str) -> Coverage:
    with open(html_path) as fp:
        htmltext = fp.read()
        soup = BeautifulSoup(htmltext, 'html.parser')
        pre = soup.find("pre")
        measured_lines = pre.find_all("span")
        coverage = Coverage()
        for line in measured_lines:
            line_number = int(line.attrs["id"][1:])
            class_sep = line.attrs["class"]
            if class_sep[0] == "fc":
                coverage.passed_line.append(line_number)
            elif class_sep[0] == "nc" or class_sep[0] == "pc":
                coverage.not_passed_line.append(line_number)
            if len(class_sep) == 2:
                if class_sep[1] == "bfc":
                    coverage.covered_branch.append(line_number)
                elif class_sep[1] == "bnc" or class_sep[1] == "bpc":
                    coverage.not_covered_branch.append(line_number)
        return coverage