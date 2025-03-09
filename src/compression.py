from PIL import Image
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

    def compress(self, input_file_name: str, output_file_name: str) -> None:
        output_file = open(output_file_name, "wb")

        image = Image.open(input_file_name)
        image = image.convert("RGB")
        data = image.tobytes()
        self.width, self.height = image.size

        size = self.__get_file_size(len(data))
        self.text_editor.insert(END, f"Размер изначального файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер изначального файла: {size}")
        
        match self.method:
            case CompressionMethods.HYBRID:
                lzw_compressed = self.lzw.compress(data)
                self.huffman.fill_frequency_table(lzw_compressed)
                self.huffman.build_tree()

                huffman_compressed = self.huffman.compress(lzw_compressed)
                output_file.write(huffman_compressed)
                size = self.__get_file_size(len(huffman_compressed))
                method_str = "LZW + Хаффман"
            case CompressionMethods.HUFFMAN:
                self.huffman.fill_frequency_table(data)
                self.huffman.build_tree()

                huffman_compressed = self.huffman.compress(data)
                output_file.write(huffman_compressed)
                size = self.__get_file_size(len(huffman_compressed))
                method_str = "Хаффман"
            case _:
                lzw_compressed = self.lzw.compress(data)
                output_file.write(lzw_compressed)
                size = self.__get_file_size(len(lzw_compressed))
                method_str = "LZW"

        self.text_editor.insert(END, f"Размер сжатого файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер сжатого файла: {size}")

        # input_file.close()
        output_file.close()

        self.text_editor.insert(END, f"Файл успешно сжат ({method_str})\n\n")
        self.text_editor.update()
        print(f"{purple}\nФайл успешно сжат ({method_str}){base_color}")

    def decompress(self, input_file_name: str, output_file_name: str) -> None:
        input_file = open(input_file_name, "rb")
        bytesStr = input_file.read()
        if not bytesStr:
            return None

        match self.method:
            case CompressionMethods.HYBRID:
                huffman_decompressed = self.huffman.decompress(bytesStr)
                lzw_decompressed = self.lzw.decompress(huffman_decompressed)
                image = Image.frombytes("RGB", (self.width, self.height), lzw_decompressed)
                size = self.__get_file_size(len(lzw_decompressed))
                method_str = "LZW + Хаффман"
            case CompressionMethods.HUFFMAN:
                huffman_decompressed = self.huffman.decompress(bytesStr)
                image = Image.frombytes("RGB", (self.width, self.height), huffman_decompressed)
                size = self.__get_file_size(len(huffman_decompressed))
                method_str = "Хаффман"
            case _:
                lzw_decompressed = self.lzw.decompress(bytesStr)
                image = Image.frombytes("RGB", (self.width, self.height), lzw_decompressed)
                size = self.__get_file_size(len(lzw_decompressed))
                method_str = "LZW"

        self.text_editor.insert(END, f"Размер распакованного файла: {size}\n")
        self.text_editor.update()
        print(f"\nРазмер распакованного файла: {size}")

        input_file.close()
        image.save(output_file_name, "BMP")

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
