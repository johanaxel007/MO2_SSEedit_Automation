from datetime import datetime


def get_current_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def print_start(plugin_count: int, plugin_whitelist_count: int, plugin_blacklist_count: int, xedit_script: str):
    print("-----------------------------------------------------------")
    print(f"Starting xEdit automatic script apply | {get_current_datetime()}")
    print("-----------------------------------------------------------")
    print(f"Total plugins: {plugin_count}")
    print(f"Whitelisted plugins: {plugin_whitelist_count}")
    print(f"Blacklisted plugins: {plugin_blacklist_count}")
    print(f"Script: {xedit_script}")
    print("-----------------------------------------------------------")


def print_finished():
    print("-----------------------------------------------------------")
    print(f"Finished xEdit automatic script apply | {get_current_datetime()}")
    print("-----------------------------------------------------------")


def print_dated(content: str):
    print(f"{get_current_datetime()} | {content}")


def read_file_to_string(file_path: str) -> str:
    f = open(file_path, mode='r', encoding="utf-8", errors="ignore")
    lines = f.read()
    f.close()
    return lines


def read_file_to_list(file_path: str) -> list:
    with open(file_path, encoding="utf-8", errors="ignore") as file:
        lines = [line.rstrip() for line in file]
    return lines


def write_string_to_file(file_path: str, contents: str) -> None:
    f = open(file_path, "w", encoding="utf-8", errors="ignore")
    f.write(contents)
    f.close()


def write_list_to_file(file_path: str, contents: list) -> None:
    f = open(file_path, "w", encoding="utf-8", errors="ignore")
    contents = '\n'.join(contents) + '\n'
    f.write(contents)
    f.close()


def escape_path(path_string: str) -> str:
    return path_string.replace('\\', '\\\\')


def pretty_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_print(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))
