import re
import ast

known_headers = (
    "parameters",
    "arguments",
    "args",
    "returns",
    "yields",
    "example",
    "examples",
    "note",
    "warning",
    "raises",
)


def measure_indent(line):
    for indent, char in enumerate(line):
        if char not in [" "]:
            return indent
    return -1


def strip_non_alpha_num(raw):
    pattern = re.compile(r"[\W_]+")
    return pattern.sub("", raw)


def create_md_content(node, title=None, cls=False):

    current_header = ""

    if title != node.name:
        print(
            node.name,
            isinstance(node, ast.FunctionDef),
            ", ".join([a.arg for a in node.args.args if a.arg != "self"]),
        )

    doc_string = ast.get_docstring(node)

    cache = ""
    if cls:
        cache += "CLASS: "
    cache += str(title)
    if isinstance(node, ast.FunctionDef):
        cache += " ("
        cache += ", ".join([a.arg for a in node.args.args if a.arg != "self"])
        cache += ")"

    cache = "## _" + cache + "_"

    if doc_string is None:
        return cache + " \n"

    last_indent = -1
    for line in doc_string.splitlines():
        indent = measure_indent(line)
        line = line.strip()

        if len(line) == 0:
            cache += "\n"

        header = [h for h in known_headers if strip_non_alpha_num(line.lower()) == h]
        if len(header) == 1:
            if current_header in ["Example", "Examples"]:
                cache += "\n~~~\n"
            current_header = header.pop().title()
            cache += " \n### " + current_header + " \n"
            last_indent = 100
            continue

        if last_indent == indent:
            # if its the same indent, its a line continuation
            if current_header in ["Example", "Examples"]:
                cache += "\n" + line
            else:
                cache += " " + line
        else:
            if last_indent > indent:
                # this is an inner_header
                parts = line.split(":")
                for index, part in enumerate(parts):
                    if index == 0 and len(part.split()) > 0:
                        print("********", current_header)
                        if current_header not in ["Example", "Examples"]:
                            cache += " \n- **" + part + "**  "
                        else:
                            cache += " \n~~~python\n" + part + "  "
                    elif len(part.split()) == 0:
                        pass
                    else:
                        cache += " - " + part + "  "
            else:
                # this is the body of the inner_header
                cache += " \n" + line

        last_indent = indent

    if current_header in ["Example", "Examples"]:
        cache += "\n~~~\n"

    # print(cache)
    return cache + " \n"
