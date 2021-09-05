from argparse import ArgumentParser
import os
from typing import List
from os import path
import random
import string
from analyze import get_package_name

temp_testcase_dir = "temp"
out_testcase_dir = "out"
classfile_dir = "tempobj"
jacoco_dumpfile_dir = "jacocoout"
jacoco_report_dir = "jacocoreport"

def get_inputs() -> dict:
    argparser = ArgumentParser()
    argparser.add_argument("junit_testsuite_path", help="テストスイートソースファイルへのパス")
    argparser.add_argument("-t", "--targetsource", dest="target_source_path", required=True, help="ユニットテスト対象のソースコードへのパス")
    argparser.add_argument("--classpath", required=True, help="プロジェクトのクラスパス")
    argparser.add_argument("--sourcepath", required=True, help="プロジェクトのソースパス")
    argparser.add_argument("--additional_test_path", dest="additional_test_path", help="テストスイートと同時にコンパイルすべきソースコードへのパス")
    argparser.add_argument("--remain_temp", action="store_true", help="ツールが終了しても一時ファイルを残す")
    argparser.add_argument("--temp", dest="tempfolder", help="一時ファイルの格納場所(デフォルトはランダムネーム)")
    argparser.add_argument("-o", "--outdir", dest="output_dir", required=True, help="出力先ディレクトリ")
    args = argparser.parse_args()
    if args.tempfolder:
        temp_dir = args.tempfolder
    else:
        temp_dir = "".join([random.choice(string.ascii_letters + string.digits) for i in range(10)])
    return {
        "junit_testsuite_path": args.junit_testsuite_path,
        "target": args.target_source_path,
        "testsuite_classname": get_package_name(args.junit_testsuite_path) + "." + path.basename(args.junit_testsuite_path).replace(".java", ""),
        "classpath": path_split(args.classpath),
        "sourcepath": path_split(args.sourcepath),
        "additional_test_path": path_split(args.additional_test_path),
        "temp_dir": temp_dir,
        "temp_testcase_dir": path.join(temp_dir, temp_testcase_dir),
        "out_testcase_dir": path.join(temp_dir, out_testcase_dir),
        "classfile_dir": path.join(temp_dir, classfile_dir),
        "jacoco_dumpfile_dir": path.join(temp_dir, jacoco_dumpfile_dir),
        "jacoco_report_dir": path.join(temp_dir, jacoco_report_dir),
        "remain_temp": True if args.remain_temp else False,
        "outdir": args.output_dir
    }


def path_split(separated_path: str) -> List[str]:
    if not separated_path:
        return []
    if os.name == "nt":
        return separated_path.split(";")
    else:
        return separated_path.split(":")