import javalang
import shlex


def extract_lines(s: str, start, end):
    l = s.split('\n')
    return '\n'.join(l[start - 1: end])


def extract_declaration_area_close_line(s: str):
    first_blace_found = False
    count = 0
    close_count = 0
    final_line = 0
    for token in shlex.split(s):
        if not first_blace_found and token == "{":
            first_blace_found = True
            count = 1
        elif first_blace_found:
            if token == "{":
                count += 1
            elif token == "}":
                count -= 1
                close_count += 1
            if count == 0:
                break
    count = 0
    for i, line in enumerate(s.split('\n')):
        count += shlex.split(line).count("}")
        if count == close_count:
            final_line = i
            break
    return final_line


def extract_testcase_line_number(file_path: str) -> list:
    with open(file_path, mode='r') as fp:
        filetext = fp.read()
        tree = javalang.parse.parse(filetext)
        member_start_lines = []
        testmethod_declaration_areas = []

        for path, node in tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                if "Test" in node.name:
                    for c in node.body:
                        is_test_method = False
                        if hasattr(c, "annotations"):
                            if len(c.annotations) > 0:
                                first_line = c.annotations[0].position.line
                                if isinstance(c, javalang.tree.MethodDeclaration) and any(a.name == "Test" for a in c.annotations):
                                    is_test_method = True
                            else:
                                first_line = c.position.line
                        else:
                            first_line = c.position.line
                        member_start_lines.append((first_line, is_test_method))
                    break

        for i in range(len(member_start_lines) - 1):
            if member_start_lines[i][1]:
                testmethod_declaration_areas.append(
                    (member_start_lines[i][0], member_start_lines[i][0] + extract_declaration_area_close_line(extract_lines(filetext, member_start_lines[i][0], member_start_lines[i + 1][0])))
                )
        testmethod_declaration_areas.append(
            (member_start_lines[-1][0], member_start_lines[-1][0] + extract_declaration_area_close_line(extract_lines(filetext, member_start_lines[-1][0], len(filetext.split('\n')))))
        )
        return testmethod_declaration_areas
