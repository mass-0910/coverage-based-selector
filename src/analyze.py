import javalang


def get_package_name(java_source_path: str) -> str:
    with open(java_source_path, mode='r') as fp:
        filetext = fp.read()
        tree = javalang.parse.parse(filetext)
    for path, node in tree:
            if isinstance(node, javalang.tree.PackageDeclaration):
                return node.name
    return None
