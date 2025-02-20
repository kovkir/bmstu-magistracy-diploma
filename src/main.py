# import subprocess

from window import Window

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
# from color import *


# INPUT_DATA_FOLDER = "../input_date/"
# OUTPUT_DATA_FOLDER = "../output_date/"
# CODE_SIZE_IN_BYTES = 4


# def get_input_file() -> str | None:
#     files_list = subprocess.getoutput(
#         cmd="cd " + INPUT_DATA_FOLDER + " && ls"
#     ).split("\n")

#     print(f"\n{yellow}Выберете входной файл для сжатия разработанным методом:{base_color}")
    
#     for i in range(len(files_list)):
#         print(f"\t{blue}{i + 1}.{base_color} {files_list[i]}")

#     try:
#         file_number = input(f"\n{green}Номер выбранного файла: {base_color}")
#         if int(file_number) <= 0:
#             print(f"\n{red}Номер команды должен быть > 0!{base_color}\n")
#         else:
#             file_path = INPUT_DATA_FOLDER + files_list[int(file_number) - 1]
#             return file_path
#     except:
#         print(f"\n{red}Ввод некоректных данных!{base_color}\n")


# def start_encryption(file_path) -> None:
#     compressor = Compression(
#         code_size=CODE_SIZE_IN_BYTES,
#     )
#     compressor.compress(
#         file_path,
#         OUTPUT_DATA_FOLDER + "/compressed.bin",
#     )
#     compressor.decompress(
#         OUTPUT_DATA_FOLDER + "/compressed.bin",
#         OUTPUT_DATA_FOLDER + "/decompressed." + file_path.split(".")[-1],
#     )


def main() -> None:
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.run()

    # file_path = get_input_file()
    # if file_path != None:
    #     start_encryption(file_path)


if __name__ == "__main__":
    main()
