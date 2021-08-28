from extract import extract_testcase_line_number
from maketest import make_alone_test
from maketest import make_selected_test
from coverage import measure_coverage
from coverage import swap_file_contents
from select_cov import select_testcase

testcase_file_path = "fizzbuzz/evosuite-tests/com/fizzbuzz/BugFizzBuzz_ESTest.java"
temp_testcase_dir = "temp/"
out_testcase_dir = "out"

if __name__ == "__main__":
    testcase_line_numbers = extract_testcase_line_number(testcase_file_path)
    testcase_count = len(testcase_line_numbers)
    alone_test_path_list = []
    for i in range(testcase_count):
        alone_test_path = make_alone_test(testcase_file_path, i, testcase_line_numbers, temp_testcase_dir)
        alone_test_path_list.append(alone_test_path)
    coverage_list = measure_coverage(alone_test_path_list, testcase_file_path, "fizzbuzz/src/main/java/com/fizzbuzz/BugFizzBuzz.java", ["./fizzbuzz/target/classes"], "./fizzbuzz/target/classes", ["fizzbuzz/src/main/java"], "com.fizzbuzz.BugFizzBuzz_ESTest", additional_testsource_path_list=["fizzbuzz/evosuite-tests/com/fizzbuzz/BugFizzBuzz_ESTest_scaffolding.java"])
    for i, coverage in enumerate(coverage_list):
        print(i, coverage)
    selected_testcase_number_list = select_testcase(coverage_list)
    print("selected_testcase_number_list =", selected_testcase_number_list)
    selected_test_path = make_selected_test(testcase_file_path, selected_testcase_number_list, testcase_line_numbers, out_testcase_dir)