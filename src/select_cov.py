from coverage import Coverage
from copy import deepcopy
from typing import List

def select_testcase(coverage_list: List[Coverage]) -> List[int]:
    full_coverage = Coverage()
    full_coverage.not_passed_line = coverage_list[0].passed_line + coverage_list[0].not_passed_line
    full_coverage.not_covered_branch = coverage_list[0].covered_branch + coverage_list[0].not_covered_branch
    for c in coverage_list:
        full_coverage = full_coverage.merged(c)
    remain_testcase_numbers = remain_testcase_number_list(full_coverage, coverage_list)
    return sorted(remain_testcase_numbers)


def remain_testcase_number_list(full_coverage: Coverage, coverage_list: List[Coverage]) -> List[int]:
    coverage_list_copy = deepcopy(coverage_list)
    remain: List[int] = []
    full_C0, full_C1 = full_coverage.coverage_percentage()
    for i in reversed(range(len(coverage_list_copy))):
        #make deleted coverage
        deleted_coverage = Coverage()
        deleted_coverage.not_passed_line = coverage_list[0].passed_line + coverage_list[0].not_passed_line
        deleted_coverage.not_covered_branch = coverage_list[0].covered_branch + coverage_list[0].not_covered_branch
        for j, c in enumerate(coverage_list_copy):
            if i == j or c == None:
                continue
            deleted_coverage = deleted_coverage.merged(c)
        deleted_C0, deleted_C1 = deleted_coverage.coverage_percentage()
        if full_C0 == deleted_C0 and full_C1 == deleted_C1:
            coverage_list_copy[i] = None
        else:
            remain.append(i)
    return remain
