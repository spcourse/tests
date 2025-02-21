from checkpy import *
import ast

m = """Make sure that all your code is inside a function or inside of
if __name__ == "__main__":."""
@test()
def has_main():
    """All code in functions or 'if __name__ == "__main__":''"""
    expressions = ['if __name__ == "__main__":', "if __name__ == '__main__':"]
    lines = extract_main_lines(file.name)
    assert len(lines) == 1, m
    assert lines[0] in expressions, m

@passed(has_main, hide=False)
def contains_rabbit():
    """Contains a Rabbit class"""
    Rabbit = getModule().__dict__.get("Rabbit")
    assert Rabbit, "Does not contain a Rabbit class"

@passed(has_main, hide=False)
def contains_fox():
    """Contains a Fox class"""
    Fox = getModule().__dict__.get("Fox")
    assert Fox, "Does not contain a Fox class"

@passed(has_main, hide=False)
def contains_experiment():
    """Contains an Experiment class"""
    Rabbit = getModule().__dict__.get("Experiment")
    assert Rabbit, "Does not contain a Experiment class"

@passed(has_main, hide=False)
def contains_creature():
    """Contains a Creature class"""
    Creature = getModule().__dict__.get("Creature")
    assert Creature, "Does not contain a Creature class"

@passed(contains_rabbit, timeout=10, hide=False)
def rabbit_attributes():
    """Rabbit contains all important attributes
        rabbit = Rabbit(0.1, 0.1, 10)"""

    Rabbit = getModule().Rabbit._function
    rabbit = Rabbit(0.1, 0.1, 10)

    fields = rabbit.__dict__
    assert "pos_x" in fields, "required attribute: pos_x"
    assert "pos_y" in fields, "required attribute: pos_y"
    assert "angle" in fields, "required attribute: angle"
    assert "speed" in fields, "required attribute: speed"
    assert "color" in fields, "required attribute: color"

@passed(rabbit_attributes, hide=False)
def rabbit_values():
    """Rabbit contains all attribute values set correctly
        rabbit = Rabbit(0.1, 0.1, 10)"""

    Rabbit = getModule().Rabbit._function
    rabbit = Rabbit(0.1, 0.1, 10)

    assert rabbit.pos_x == 0.1
    assert rabbit.pos_y == 0.1
    assert rabbit.angle == 10
    assert rabbit.color == "blue"
    assert rabbit.speed == 0.01

@passed(contains_fox, timeout=10, hide=False)
def fox_attributes():
    """Rabbit contains all important attributes
        fox = Fox(0.1, 0.1, 10)"""

    Fox = getModule().Fox._function
    fox = Fox(0.1, 0.1, 10)

    fields = fox.__dict__
    assert "pos_x" in fields, "required attribute: pos_x"
    assert "pos_y" in fields, "required attribute: pos_y"
    assert "angle" in fields, "required attribute: angle"
    assert "speed" in fields, "required attribute: speed"
    assert "color" in fields, "required attribute: color"

@passed(fox_attributes, hide=False)
def fox_values():
    """Rabbit contains all attribute values set correctly
        fox = Fox(0.1, 0.1, 10)"""

    Fox = getModule().Fox._function
    fox = Fox(0.1, 0.1, 10)

    assert fox.pos_x == 0.1
    assert fox.pos_y == 0.1
    assert fox.angle == 10
    assert fox.color == "red"
    assert fox.speed == 0.03


def extract_main_lines(file_path: str) -> str:
    """
    Reads the Python file at file_path and returns all lines of main code (except imports)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source, filename=file_path)

    func_ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_ranges.append((node.lineno, node.end_lineno))

    func_ranges.sort()
    merged_ranges = []
    for start, end in func_ranges:
        if merged_ranges and start <= merged_ranges[-1][1]:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))
        else:
            merged_ranges.append((start, end))

    lines = source.splitlines()
    result_lines = []
    current_line = 1

    for start, end in merged_ranges:
        while current_line < start:
            result_lines.append(lines[current_line - 1])
            current_line += 1
        current_line = end + 1

    while current_line <= len(lines):
        result_lines.append(lines[current_line - 1])
        current_line += 1

    return [line for line in result_lines if \
        line.split(" ")[0] not in ["class", "import", "", "from"] and \
        line[0] != "#"]


def collect_all_of_type(obj, stype):
    collect = [value for field, value in obj.__dict__.items() if isinstance(value, stype)]
    lists = [value for field, value in obj.__dict__.items() if isinstance(value, list)]
    for _list in lists:
        for e in _list:
            if isinstance(e, stype):
                collect.append(e)
    return collect
