from PIL import Image
from os.path import getsize
from tkinter import Text, END
from tkinter.ttk import Progressbar

from constants import CompressionMethods, BYTES_AMOUNT_PER_PIXEL
from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    def __init__(
        self,
        method: CompressionMethods,
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.lzw = LZW(text_editor, progressbar)
        self.huffman = Huffman(text_editor, progressbar)
        self.text_editor = text_editor
        self.method = method

    def compress(self, input_file_name: str, output_file_name: str) -> None:
        short_filename = input_file_name.split("/")[-1]
        size = getsize(input_file_name)
        size_str = self.__get_file_size(size)

        self.text_editor.insert(
            END, 
            f"Сжатие файла {short_filename} ({self.method.name})\n\n", 
            ("bold", "center",)
        )
        self.text_editor.insert(END, f"Размер изначального файла: {size_str}\n")
        self.text_editor.update()
        print(f"\n{blue}Сжатие файла {short_filename} ({self.method.name}){base_color}")
        print(f"\nРазмер изначального файла: {size_str}")
        
        image = Image.open(input_file_name)
        image = image.convert("RGB")
        data = image.tobytes()
        self.width, self.height = image.size

        match self.method:
            case CompressionMethods.HYBRID:
                lzw_compressed = self.lzw.compress(data)

                self.huffman.fill_frequency_table(lzw_compressed, self.lzw.code_size)
                self.huffman.build_tree()

                compressed = self.huffman.compress(lzw_compressed, self.lzw.code_size)
                method_str = "LZW + Хаффман"
                size_data_to_decompress = 4 + 4 + 4 + 4 + 4 + \
                    len(self.lzw.unique_pixels) * BYTES_AMOUNT_PER_PIXEL + \
                    len(self.huffman.frequency_table) * (self.lzw.code_size + self.huffman.frequency_size_in_bytes)
            case CompressionMethods.HUFFMAN:
                self.huffman.fill_frequency_table(data, BYTES_AMOUNT_PER_PIXEL)
                self.huffman.build_tree()

                compressed = self.huffman.compress(data, BYTES_AMOUNT_PER_PIXEL)
                method_str = "Хаффман"
                size_data_to_decompress = 4 + 4 + 4 + 4 + \
                    len(self.huffman.frequency_table) * (BYTES_AMOUNT_PER_PIXEL + self.huffman.frequency_size_in_bytes)
            case _:
                compressed = self.lzw.compress(data)
                method_str = "LZW"
                size_data_to_decompress = 4 + 4 + 4 + \
                    len(self.lzw.unique_pixels) * BYTES_AMOUNT_PER_PIXEL

        with open(output_file_name, "wb") as f:
            f.write(compressed)

        compressed_file_size = getsize(output_file_name)
        compression_ratio = (size - compressed_file_size - size_data_to_decompress) / size * 100

        size_data_to_decompress_str = self.__get_file_size(size_data_to_decompress)
        compressed_file_size_str = self.__get_file_size(compressed_file_size)

        self.text_editor.insert(END, f"Размер сжатого файла: {compressed_file_size_str}\n")
        self.text_editor.insert(END, f"Размер информации для распаковки файла: {size_data_to_decompress_str}\n")
        self.text_editor.insert(END, "Степень сжатия файла: {:2.2f}%\n".format(compression_ratio))
        self.text_editor.insert(END, f"Файл успешно сжат ({method_str})\n", ("bold",))
        self.text_editor.update()
        print(f"\nРазмер сжатого файла: {compressed_file_size_str}")
        print(f"\nРазмер информации для распаковки файла: {size_data_to_decompress_str}")
        print("\nСтепень сжатия файла: {:2.2f}%".format(compression_ratio))
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

        size_str = self.__get_file_size(getsize(output_file_name))

        self.text_editor.insert(END, f"Размер распакованного файла: {size_str}\n")
        self.text_editor.insert(END, f"Файл успешно распакован ({method_str})\n\n", ("bold",))
        self.text_editor.update()
        print(f"\nРазмер распакованного файла: {size_str}")
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
