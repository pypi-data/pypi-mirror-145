import traceback
from math import ceil, floor
from re import findall
from typing import Any

from tiivad.results import Results


def execute_test(func, points, before_message, failed_message: str, passed_message, test_name, user_inputs, *args):
    if failed_message is None:
        failed_message = ""
    result = {}
    try:
        test_result, failed_message = func(*args, failed_message=failed_message)
    except Exception as e:  # TODO: Refactor me, too much duplication
        result['test_name'] = func.__name__
        result['points'] = 0.0
        result['exceptionMessage'] = str(traceback.format_exc())
        result['beforeMessage'] = before_message
        result['failedMessage'] = str(e)
        result['passedMessage'] = passed_message
        result['testName'] = test_name
        result['userInputs'] = user_inputs
        result['testStatus'] = "Exception"
    else:
        if test_result:
            result['test_name'] = func.__name__
            result['points'] = points
            result['beforeMessage'] = before_message
            result['failedMessage'] = failed_message
            result['passedMessage'] = passed_message
            result['testName'] = test_name
            result['userInputs'] = user_inputs
            result['testStatus'] = "TestPass"
        else:
            result['test_name'] = func.__name__
            result['points'] = 0.0
            result['beforeMessage'] = before_message
            result['failedMessage'] = failed_message
            result['passedMessage'] = passed_message
            result['testName'] = test_name
            result['userInputs'] = user_inputs
            result['testStatus'] = "TestFail"
    Results(result)
    print(result)
    return result


def format_error(error_message, mapping_dict):
    for k, v in mapping_dict.items():
        a = {k: "{" + str(v) + "}"}
        try:
            error_message = error_message.format(**a)
        except:
            pass
    return error_message


def create_input_file(file_name: str, file_content: str):
    f = open(file_name, "w", encoding="utf-8")
    f.write(file_content)
    f.close()


def get_file_text(file_name: str) -> str:
    with open(file_name, encoding='utf-8') as f:
        return f.read()


def value_not_empty(value: Any) -> bool:
    if value is None:
        return False
    if type(value) == str and value.strip() == "":
        return False
    return True


def string_not_empty(string: str) -> bool:
    return string is not None and string.strip() != ""


def unified_value_correct(value: Any, expected_value: Any, value_type: str = 'str') -> bool:
    # TODO lisa mõned testid
    # TODO: See on utils?
    """
    # * mida tagastatud väärtusele rakendatakse
    # * enne kui väärtuse õigsust kontrollitakse
    # - probleemid siis, kui programm tagastab ujukomaarve, seetõttu võiks vastust kontrollida hoopis vahemikku sobivusega
    # - funktsioon tagastab sõne, aga pole tegelikult oluline, et kas tegemist on suur- või väiketähtedega
    # - ehk me rakendame tudengi kirjutatud funktsiooni poolt tagastatud väärtusele mingi funktsiooni (nt .lower()) ja alles siis võrdleme etteantud tulemusega
    :param expected_value:
    :param result_value:
    :return:
    """
    if value_type == 'str':
        return value.strip().lower() == expected_value
    elif value_type == 'number':
        return floor(float(expected_value)) <= value <= ceil(float(expected_value))
    # TODO: Kas veel mõni tüüp?


def list_contains_items_ordered(lst: list, items: list) -> bool:
    """
    Abifunktsioon järgnevate jaoks
    """
    j = 0
    for item in items:
        while j < len(lst) and lst[j] != item:
            j += 1
        if j == len(lst):
            return False
        else:
            j += 1
    return True


# -- Numbers

def list_of_numbers(string: str) -> list[float]:
    if string is None:
        return []
    exp = r"([-]?[0-9]+(?:[.][0-9]+)?)"
    return list(map(float, findall(exp, string)))


def number_of_numbers(string: str) -> int:
    return len(list_of_numbers(string))


def number_of_numbers_exactly(string: str, n: int) -> bool:
    return number_of_numbers(string) == n


def number_of_numbers_at_least(string: str, n: int) -> bool:
    return number_of_numbers(string) >= n


def number_of_numbers_at_most(string: str, n: int) -> bool:
    return number_of_numbers(string) <= n


def string_contains_any_number(string: str) -> bool:
    return number_of_numbers_at_least(string, 1)


def string_contains_number(string: str, item: float) -> bool:
    return item in list_of_numbers(string)


def string_contains_numbers(string: str, items: list[float]) -> bool:
    sorted_numbers = sorted(list_of_numbers(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_numbers, sorted_items)


def string_contains_numbers_ordered(string: str, items: list[float]) -> bool:
    numbers = list_of_numbers(string)
    return list_contains_items_ordered(numbers, items)


def string_contains_only_these_numbers(string: str, items: list[float]) -> bool:
    sorted_numbers = sorted(list_of_numbers(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_numbers, sorted_items) and \
           len(sorted_numbers) == len(sorted_items)


def string_contains_only_these_numbers_ordered(string: str, items: list[float]) -> bool:
    numbers = list_of_numbers(string)
    return list_contains_items_ordered(numbers, items) and len(numbers) == len(items)


# -- Strings

def list_of_strings(string: str) -> list[str]:
    if string is None:
        return []
    s = string.replace(".", " ").replace(",", " ").replace(":", " ").replace(";", " ")
    s = s.replace("?", " ").replace("!", " ").replace('"', " ")
    return s.split()


def number_of_strings(string: str) -> int:
    return len(list_of_strings(string))


def number_of_strings_exactly(string: str, n: int) -> bool:
    return number_of_strings(string) == n


def number_of_strings_at_least(string: str, n: int) -> bool:
    return number_of_strings(string) >= n


def number_of_strings_at_most(string: str, n: int) -> bool:
    return number_of_strings(string) <= n


def string_contains_any_string(string: str) -> bool:
    return number_of_strings_at_least(string, 1)


def string_equals_string(string: str, item: str) -> bool:
    return string is not None and item == string


def string_contains_string(string: str, item: str) -> bool:
    return string is not None and item in string


def string_contains_strings(string: str, items: list[float]) -> bool:
    sorted_strings = sorted(list_of_strings(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_strings, sorted_items)


def string_contains_strings_ordered(string: str, items: list[float]) -> bool:
    strings = list_of_strings(string)
    return list_contains_items_ordered(strings, items)


def string_contains_only_these_strings(string: str, items: list[float]) -> bool:
    sorted_strings = sorted(list_of_strings(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_strings, sorted_items) and \
           len(sorted_strings) == len(sorted_items)


def string_contains_only_these_strings_ordered(string: str, items: list[float]) -> bool:
    strings = list_of_strings(string)
    return list_contains_items_ordered(strings, items) and len(strings) == len(items)


# -- Lines

def list_of_lines(string: str):
    if string is None:
        return []
    lines = []
    for s in string.strip().split("\n"):
        if s.strip() != "":
            lines.append(s)
    return lines


def number_of_lines(string: str) -> int:
    return len(list_of_lines(string))


def number_of_lines_exactly(string: str, n: int) -> bool:
    return number_of_lines(string) == n


def number_of_lines_at_least(string: str, n: int) -> bool:
    return number_of_lines(string) >= n


def number_of_lines_at_most(string: str, n: int) -> bool:
    return number_of_lines(string) <= n


def string_line_contains_string(string: str, line_nr: int, item: str) -> bool:
    lines = list_of_lines(string)
    if 1 <= line_nr <= len(lines):
        if item in lines[line_nr - 1]:
            return True
    return False


def string_line_equals(string: str, line_nr: int, item: str) -> bool:
    lines = list_of_lines(string)
    if 1 <= line_nr <= len(lines):
        if item == lines[line_nr - 1]:
            return True
    return False


def string_contains_lines(string: str, items: list[float]) -> bool:
    sorted_lines = sorted(list_of_lines(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_lines, sorted_items)


def string_contains_lines_ordered(string: str, items: list[float]) -> bool:
    lines = list_of_lines(string)
    return list_contains_items_ordered(lines, items)


def string_contains_only_these_lines(string: str, items: list[float]) -> bool:
    sorted_lines = sorted(list_of_lines(string))
    sorted_items = sorted(items)
    return list_contains_items_ordered(sorted_lines, sorted_items) and \
           len(sorted_lines) == len(sorted_items)


def string_contains_only_these_lines_ordered(string: str, items: list[float]) -> bool:
    lines = list_of_lines(string)
    return list_contains_items_ordered(lines, items) and len(lines) == len(items)
