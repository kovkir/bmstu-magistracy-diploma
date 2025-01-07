from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    def __init__(self, code_size: int) -> None:
        self.huffman = Huffman(code_size)
        self.lzw = LZW(code_size)

    def compress(self, input_file_name: str, output_file_name: str) -> None:
        input_file = open(input_file_name, "rb")
        output_file = open(output_file_name, "wb")

        data = input_file.read()

        size = self.__get_file_size(len(data))
        print(f"\nРазмер изначального файла: {size}")

        lzw_compressed = self.lzw.compress(data)
        self.huffman.fill_frequency_table(lzw_compressed)
        self.huffman.build_tree()

        huffman_compressed = self.huffman.compress(lzw_compressed)
        output_file.write(huffman_compressed)

        size = self.__get_file_size(len(huffman_compressed))
        print(f"\nРазмер сжатого файла: {size}")

        input_file.close()
        output_file.close()

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
        print(f"\nРазмер распакованного файла: {size}")

        output_file.write(lzw_decompressed)

        input_file.close()
        output_file.close()

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
