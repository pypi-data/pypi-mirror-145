import ast
from typing import Tuple, List

from tiivad.file import File
from tiivad.utils import format_error


class Program:
    def __init__(self, program_name: str):
        self.file: File = File(program_name)
        self.syntax_tree: ast.Module = None
        self.contains_loop: bool = None
        self.calls_print: bool = None
        self.contains_try_except: bool = None

    def get_syntax_tree(self) -> ast.Module:
        """
        Get AST syntax tree of the program at hand.
        :return: Syntax tree of the program at hand.
        """
        if self.syntax_tree is None:
            try:
                self.syntax_tree = ast.parse(self.file.get_file_text())
            except Exception as e:
                self.syntax_tree = ""
        return self.syntax_tree

    def program_imports_module(self, module_name: str, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program imports module.
        :param module_name: Module name that is being checked.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if the program imports the specified module, False if doesn't import.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        for node in ast.walk(self.get_syntax_tree()):
            if isinstance(node, ast.Import):
                if 'names' in node._fields:
                    for mod_name in node.names:
                        if 'name' in mod_name._fields:
                            if mod_name.name == module_name:
                                return True, failed_message
                            split_names = mod_name.name.split(".")
                            for split_name in split_names:
                                if split_name == module_name:
                                    return True, failed_message
            if isinstance(node, ast.ImportFrom):
                if 'module' in node._fields:
                    for name in node.names:
                        if name.name == module_name:
                            return True, failed_message
                    if node.module == module_name:
                        return True, failed_message
                    split_names = node.module.split(".")
                    for split_name in split_names:
                        if split_name == module_name:
                            return True, failed_message

        return False, format_error(failed_message, {"module_name": module_name})

    def program_imports_module_from_set(self, module_names: List[str], failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program imports any given module from the set.
        :param module_names: Module names that are being checked.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if the program imports any module from the set, False if it doesn't import.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        for module_name in module_names:
            if self.program_imports_module(module_name)[0]:
                return True, failed_message
        return False, format_error(failed_message, {"module_name": module_names})

    def program_imports_any_module(self, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program imports any module.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if imports any, False if not.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        for node in ast.walk(self.get_syntax_tree()):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return True, failed_message
        return False, failed_message

    def program_defines_function(self, function_name: str, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program defines a function.
        :param failed_message: The message that will be displayed in case of failing the test.
        :param function_name: Function name that is being checked.
        :return: True if the program defines the function, False if doesn't use.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        defines_function = function_name in [c.name for c in ast.walk(self.get_syntax_tree())
                                             if isinstance(c, ast.FunctionDef) and not isinstance(c, ast.Attribute)]
        if not defines_function:
            failed_message = format_error(failed_message, {"function_name": function_name})

        return defines_function, failed_message

    def program_defines_any_function(self, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program defines any function in it.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if defines any other function, False if doesn't.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        defines_function = len([c.name for c in ast.walk(self.get_syntax_tree())
                                if isinstance(c, ast.FunctionDef)
                                and not isinstance(c, ast.Attribute)]) > 0

        return defines_function, failed_message

    def program_contains_loop(self, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program contains a while/for loop (including in functions).
        :return: True if contains a loop, False if not.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        if self.contains_loop is None:
            self.contains_loop = False
            for node in ast.walk(self.get_syntax_tree()):
                if isinstance(node, (ast.For, ast.While, ast.comprehension)):
                    self.contains_loop = True
                    break
        return self.contains_loop, failed_message

    def program_contains_try_except(self, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program contains a try/except block (including in functions).
        :return: True if contains a try/except block, False if not.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        if self.contains_try_except is None:
            self.contains_try_except = False
            for node in ast.walk(self.get_syntax_tree()):
                if isinstance(node, (ast.Try, ast.ExceptHandler)):
                    self.contains_try_except = True
                    break
        return self.contains_try_except, failed_message

    def program_calls_function(self, function_name: str, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program calls a given function.
        :param function_name: str, function name to be checked.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if program calls the given function, False if not.
        """
        result, _ = self.program_calls_function_from_set([function_name])
        if not result:
            return result, format_error(failed_message, {"function_name": function_name})
        return result, failed_message

    def program_calls_function_from_set(self, functions_list: list[str], failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program calls a function from a given list.
        :param functions_list: List of function names.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if any of the functions in list are called, False if not.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        for node in ast.walk(self.get_syntax_tree()):
            if isinstance(node, ast.Call):
                if 'func' in node._fields:
                    if 'id' in node.func._fields:
                        for i in range(len(functions_list)):
                            if node.func.id == functions_list[i]:
                                return True, failed_message
                    if 'attr' in node.func._fields:
                        for i in range(len(functions_list)):
                            if node.func.attr == functions_list[i]:
                                return True, failed_message
        return False, format_error(failed_message, {"functions_list": functions_list})

    def program_calls_print(self, failed_message: str = "") -> Tuple[bool, str]:
        """
        Checks if program calls print.
        :param failed_message: The message that will be displayed in case of failing the test.
        :return: True if program calls print, False if not.
        """
        if not self.get_syntax_tree():
            return False, failed_message
        if self.calls_print is None:
            self.calls_print, _ = self.program_calls_function("print")
        return self.calls_print, failed_message


if __name__ == '__main__':
    prog = Program("../test/samples/solution.py")
    print(prog.get_syntax_tree())
    print(prog.program_defines_function("test"))
    print(prog.program_defines_any_function())
    print(prog.program_imports_module("math"))
    print(prog.program_imports_any_module())
    print(prog.program_calls_function("test"))
    print(prog.program_calls_function("ceil"))
    print(prog.program_calls_function_from_set(["t", "test"]))
    print(prog.program_calls_function_from_set(["t", "t2"]))
    print(prog.program_contains_loop())
    print(prog.program_calls_print())
