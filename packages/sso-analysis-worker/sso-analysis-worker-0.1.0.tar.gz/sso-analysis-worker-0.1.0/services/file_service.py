from os import path


def read_line_from_file(filename: str, line_number: int) -> str:
    return_line = None
    with open(filename) as file:
        for i, line in enumerate(file):
            if i == line_number:
                return_line = line
                break
    return return_line


def save_to_file(file_path: str, base_page: str, ids: list) -> bool:
    if not path.isfile(file_path):
        with open(file_path, "w") as file:
            file.write("Site,Found Google,Found Facebook,Found Apple\n")
    with open(file_path, "a") as file:
        file.write(base_page)
        file.write("," + str(ids.__contains__(1)))
        file.write("," + str(ids.__contains__(2)))
        file.write("," + str(ids.__contains__(3)))
        file.write("\n")
    return True
