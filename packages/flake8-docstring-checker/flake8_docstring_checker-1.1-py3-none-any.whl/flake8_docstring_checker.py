from typing import NoReturn, List, Tuple
import ast


__version__ = "1.1"


DC100 = "DC100 Module has no docstring"
DC101 = "DC101 Missing docstring in class {name}"
DC102 = "DC102 Missing docstring in public function {name}"
DC103 = "DC103 Missing docstring in private function {name}"
DC104 = "DC104 Missing docstring in special function {name}"


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Module(self, node: ast.Module) -> NoReturn:
        try:
            if isinstance(node.body[0].value.value, str):
                self.generic_visit(node)
                return
        except:
            pass
        self.errors.append((0, 0, DC100))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> NoReturn:
        try:
            if isinstance(node.body[0].value.value, str):
                self.generic_visit(node)
                return
        except:
            pass
        self.errors.append((node.lineno, node.col_offset, DC101.format(name=node.name)))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> NoReturn:
        try:
            if isinstance(node.body[0].value.value, str):
                self.generic_visit(node)
                return
        except:
            pass
        if node.name.startswith("__") and node.name.endswith("__"):
            self.errors.append((node.lineno, node.col_offset, DC104.format(name=node.name)))
        elif node.name.startswith("_"):
            self.errors.append((node.lineno, node.col_offset, DC103.format(name=node.name)))
        else:
            self.errors.append((node.lineno, node.col_offset, DC102.format(name=node.name)))
        self.generic_visit(node)


class Plugin:
    name = "flake8-docstring-checker"
    version = __version__

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        visitor = Visitor()
        visitor.visit(self._tree)
        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
