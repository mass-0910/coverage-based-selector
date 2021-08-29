from arguments import get_inputs
from extract import extract_testcase_line_number
from maketest import make_alone_test
from maketest import make_selected_test
from coverage import measure_coverage
from select_cov import select_testcase
from shutil import rmtree
import traceback


if __name__ == "__main__":
    print("Coverage-based Testcase Selector")
    inputs = get_inputs()
    try:
        testcase_line_numbers = extract_testcase_line_number(inputs['junit_testsuite_path'])
        testcase_count = len(testcase_line_numbers)
        alone_test_path_list = []
        for i in range(testcase_count):
            alone_test_path = make_alone_test(inputs['junit_testsuite_path'], i, testcase_line_numbers, inputs['temp_testcase_dir'])
            alone_test_path_list.append(alone_test_path)
        coverage_list = measure_coverage(alone_test_path_list, inputs['junit_testsuite_path'], inputs['target'], inputs['classpath'], inputs['sourcepath'], inputs['testsuite_classname'], inputs['classfile_dir'], inputs['jacoco_dumpfile_dir'], inputs['jacoco_report_dir'], additional_testsource_path_list=inputs['additional_test_path'])
        # for i, coverage in enumerate(coverage_list):
        #     print(i, coverage)
        selected_testcase_number_list = select_testcase(coverage_list)
        print("selected_testcase_number_list =", selected_testcase_number_list)
        selected_test_path = make_selected_test(inputs['junit_testsuite_path'], selected_testcase_number_list, testcase_line_numbers, inputs['outdir'])
    except Exception as e:
        print(traceback.format_exc())
    finally:
        if not inputs['remain_temp']:
            rmtree(inputs['temp_dir'], ignore_errors=True)