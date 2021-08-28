from os import path
from os import mkdir
from typing import List
import re


def remove_area_lines(s: str, start: int, end: int, test_number: int) -> str:
    l = s.split('\n')
    for i in range(len(s)):
        if i >= start - 1 and i < end:
            l[i] = f"// test{test_number} deleted"
    return '\n'.join(l)


def make_alone_test(testsource_path: str, leave_test_number: int, testcase_line_areas: list, temp_testcase_dir: str) -> str:
    alone_test_path = path.join(temp_testcase_dir, path.basename(testsource_path).replace(".java", f"_{leave_test_number}.java"))
    if not path.exists(temp_testcase_dir):
        mkdir(temp_testcase_dir)
    with open(testsource_path, mode='r') as fip, open(alone_test_path, mode='w') as fop:
        filetext = fip.read()
        for i, area in enumerate(testcase_line_areas):
            if i != leave_test_number:
                filetext = remove_area_lines(filetext, area[0], area[1], i)
        fop.write(filetext)
    return alone_test_path

def make_selected_test(testsource_path: str, selected_test_number_list: int, testcase_line_areas: list, out_testcase_dir: str) -> str:
    selected_testsource_name = path.basename(testsource_path).replace(".java", f"_selected.java")
    selected_test_path = path.join(out_testcase_dir, selected_testsource_name)
    if not path.exists(out_testcase_dir):
        mkdir(out_testcase_dir)
    with open(testsource_path, mode='r') as fip, open(selected_test_path, mode='w') as fop:
        filetext = fip.read()
        for i, area in enumerate(testcase_line_areas):
            if not i in selected_test_number_list:
                filetext = remove_area_lines(filetext, area[0], area[1], i)
        filetext = re.sub(rf"(\W){path.basename(testsource_path).replace('.java', '')}(\W)", rf"\1{selected_testsource_name.replace('.java', '')}\2", filetext)
        fop.write(filetext)
    return selected_test_path