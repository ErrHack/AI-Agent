from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info


def main():
    # print(get_files_info("calculator", "."))
    # print(get_files_info("calculator", "pkg"))
    # print(get_files_info("calculator", "/bin"))
    # print(get_files_info("calculator", "../"))

    # print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "."))


if __name__ == "__main__":
    main()