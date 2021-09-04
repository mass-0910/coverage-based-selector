from coverage import Coverage
from copy import deepcopy
from typing import List

def select_testcase(coverage_list: List[Coverage]):
    empty_coverage = Coverage()
    empty_coverage.not_passed_line = coverage_list[0].passed_line + coverage_list[0].not_passed_line
    empty_coverage.not_covered_branch = coverage_list[0].covered_branch + coverage_list[0].not_covered_branch
    road = func(empty_coverage, coverage_list)
    return sorted(road)


def func(pre_merge: Coverage, left: List[Coverage], number: int = None) -> List[int]:
    road_list = None
    for i, l in enumerate(left):
        if l == None:
            continue
        post_merge = pre_merge.merged(l)
        pre_C0, pre_C1 = pre_merge.coverage_percentage()
        post_C0, post_C1 = post_merge.coverage_percentage()
        if pre_C0 < post_C0 or pre_C1 < post_C1:
            left_copy = deepcopy(left)
            left_copy[i] = None
            road = func(post_merge, left_copy, i)
            if road_list == None or len(road_list) > len(road):
                road_list = road
    if road_list == None:
        road_list = []
    if number != None:
        road_list.append(number)
    return road_list