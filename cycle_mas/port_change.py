import sys
import re


def change_port_in_html(input_file, new_port):
    with open(input_file, "r") as f:
        lines = f.readlines()

    pattern = re.compile(r"^(PORT\s*=\s*)\d+")
    for i, line in enumerate(lines):
        if pattern.match(line):
            lines[i] = f"PORT = {new_port}\n"
            break

    with open(input_file, "w") as f:
        f.writelines(lines)
    print(f"Updated PORT to {new_port} in {input_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python port_change.py <new_port>")
        sys.exit(1)
    new_port = sys.argv[1]
    input_file = "initial.html"
    change_port_in_html(input_file, new_port)
