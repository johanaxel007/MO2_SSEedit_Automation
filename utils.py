def read_file_to_string(file_path: str) -> str:
    f = open(file_path, mode='r')
    lines = f.read()
    f.close()
    return lines


def read_file_to_list(file_path: str) -> list:
    with open(file_path) as file:
        lines = [line.rstrip() for line in file]
    return lines


def write_string_to_file(file_path: str, contents: str) -> None:
    f = open(file_path, "w")
    f.write(contents)
    f.close()


def write_list_to_file(file_path: str, contents: list) -> None:
    f = open(file_path, "w")
    contents = '\n'.join(contents) + '\n'
    f.write(contents)
    f.close()


def pretty_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))