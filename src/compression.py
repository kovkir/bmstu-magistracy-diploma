from tkinter import Text, END

from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    def __init__(self, code_size: int, text_editor: Text) -> None:
        self.huffman = Huffman(code_size, text_editor)
        self.lzw = LZW(code_size, text_editor)
        self.text_editor = text_editor

    def compress(self, input_file_name: str, output_file_name: str) -> None:
        input_file = open(input_file_name, "rb")
        output_file = open(output_file_name, "wb")

        data = input_file.read()

        size = self.__get_file_size(len(data))
        self.text_editor.insert(END, f"Размер изначального файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер изначального файла: {size}")

        lzw_compressed = self.lzw.compress(data)
        self.huffman.fill_frequency_table(lzw_compressed)
        self.huffman.build_tree()

        huffman_compressed = self.huffman.compress(lzw_compressed)
        output_file.write(huffman_compressed)

        size = self.__get_file_size(len(huffman_compressed))
        self.text_editor.insert(END, f"Размер сжатого файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер сжатого файла: {size}")

        input_file.close()
        output_file.close()

        self.text_editor.insert(END, f"Файл успешно сжат (LZW + Хаффман)\n")
        self.text_editor.update()
        print(f"{purple}\nФайл успешно сжат (LZW + Хаффман){base_color}")

    def decompress(self, input_file_name: str, output_file_name: str) -> None:
        input_file = open(input_file_name, "rb")
        output_file = open(output_file_name, "wb")

        bytesStr = input_file.read()
        if not bytesStr:
            return None

        huffman_decompressed = self.huffman.decompress(bytesStr)
        lzw_decompressed = self.lzw.decompress(huffman_decompressed)

        size = self.__get_file_size(len(lzw_decompressed))
        self.text_editor.insert(END, f"Размер распакованного файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер распакованного файла: {size}")

        output_file.write(lzw_decompressed)

        input_file.close()
        output_file.close()

        self.text_editor.insert(END, f"Файл успешно распакован (Хаффман + LZW)\n")
        self.text_editor.update()
        print(f"{purple}\nФайл успешно распакован (Хаффман + LZW){base_color}\n")

    def __get_file_size(self, bytes_count: int) -> str:
        kilobytes = bytes_count / 1024
        megabytes = kilobytes / 1024
        gigabyte = megabytes / 1024

        if gigabyte >= 1:
            size = f"{round(gigabyte, 2)} ГБ"
        elif megabytes >= 1:
            size = f"{round(megabytes, 2)} МБ"
        elif kilobytes >= 1:
            size = f"{round(kilobytes, 2)} КБ"
        else:
            size = f"{bytes_count} Б"

        return size
