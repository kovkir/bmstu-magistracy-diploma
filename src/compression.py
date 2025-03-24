from PIL import Image
from os.path import getsize
from tkinter import Text, END
from tkinter.ttk import Progressbar

from constants import CompressionMethods
from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    def __init__(
        self,
        method: CompressionMethods,
        code_size: int,
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.lzw = LZW(code_size, text_editor, progressbar)
        self.huffman = Huffman(code_size, text_editor, progressbar)
        self.text_editor = text_editor
        self.method = method
        self.code_size = code_size

    def compress(self, input_file_name: str, output_file_name: str) -> None:
        size = self.__get_file_size(getsize(input_file_name))
        self.text_editor.insert(END, f"Размер изначального файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер изначального файла: {size}")
        
        image = Image.open(input_file_name)
        image = image.convert("RGB")
        data = image.tobytes()
        self.width, self.height = image.size

        match self.method:
            case CompressionMethods.HYBRID:
                lzw_compressed = self.lzw.compress(data)

                self.huffman.fill_frequency_table(lzw_compressed)
                self.huffman.build_tree()

                compressed = self.huffman.compress(lzw_compressed)
                method_str = "LZW + Хаффман"
                size_data_to_decompress = self.__get_file_size(
                    4 + 4 + 4 + 4 + len(self.lzw.unique_pixels) * self.code_size + \
                        len(self.huffman.frequency_table) * (self.code_size + 4)
                )
            case CompressionMethods.HUFFMAN:
                self.huffman.fill_frequency_table(data)
                self.huffman.build_tree()

                compressed = self.huffman.compress(data)
                method_str = "Хаффман"
                size_data_to_decompress = self.__get_file_size(
                    4 + 4 + 4 + len(self.huffman.frequency_table) * (self.code_size + 4)
                )
            case _:
                compressed = self.lzw.compress(data)
                method_str = "LZW"
                size_data_to_decompress = self.__get_file_size(
                    4 + 4 + 4 + len(self.lzw.unique_pixels) * self.code_size
                )

        with open(output_file_name, "wb") as f:
            f.write(compressed)

        size = self.__get_file_size(getsize(output_file_name))
        self.text_editor.insert(END, f"Размер сжатого файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер сжатого файла: {size}")

        self.text_editor.insert(END, f"Размер информации для распаковки файла: {size_data_to_decompress}\n")
        self.text_editor.update()
        print(f"\nРазмер информации для распаковки файла: {size_data_to_decompress}")

        self.text_editor.insert(END, f"Файл успешно сжат ({method_str})\n\n")
        self.text_editor.update()
        print(f"{purple}\nФайл успешно сжат ({method_str}){base_color}")

    def decompress(self, input_file_name: str, output_file_name: str) -> None:
        with open(input_file_name, "rb") as f:
            bytesStr = f.read()
            if not bytesStr:
                return None

        match self.method:
            case CompressionMethods.HYBRID:
                huffman_decompressed = self.huffman.decompress(bytesStr)
                decompressed = self.lzw.decompress(huffman_decompressed)
                method_str = "LZW + Хаффман"
            case CompressionMethods.HUFFMAN:
                decompressed = self.huffman.decompress(bytesStr)
                method_str = "Хаффман"
            case _:
                decompressed = self.lzw.decompress(bytesStr)
                method_str = "LZW"

        image = Image.frombytes("RGB", (self.width, self.height), decompressed)
        image.save(output_file_name, "BMP")

        size = self.__get_file_size(getsize(output_file_name))
        self.text_editor.insert(END, f"Размер распакованного файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер распакованного файла: {size}")

        self.text_editor.insert(END, f"Файл успешно распакован ({method_str})\n\n")
        self.text_editor.update()
        print(f"{purple}\nФайл успешно распакован ({method_str}){base_color}\n")

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
