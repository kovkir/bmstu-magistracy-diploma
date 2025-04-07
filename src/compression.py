import re
from PIL import Image
from os.path import getsize
from tkinter import Text, END
from tkinter.ttk import Progressbar

from constants import CompressionMethods, BYTES_AMOUNT_PER_PIXEL
from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    compression_methods_names = {
        CompressionMethods.HYBRID: "LZW + Хаффман",
        CompressionMethods.HUFFMAN: "Хаффман",
        CompressionMethods.LZW: "LZW",
    }

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
        method_name = self.compression_methods_names[self.method]
        size = getsize(input_file_name)
        size_str = self.__get_file_size(size)

        self.text_editor.insert(END, f"Сжатие файла {short_filename} ({method_name})\n\n", ("bold", "center",))
        self.text_editor.insert(END, f"Размер изначального файла: {size_str}\n")
        self.text_editor.update()
        print(f"\n{blue}Сжатие файла {short_filename} ({method_name}){base_color}")
        print(f"\nРазмер изначального файла: {size_str}")
        
        image = Image.open(input_file_name)
        image = image.convert("RGB")
        data = image.tobytes()
        self.width, self.height = image.size

        match self.method:
            case CompressionMethods.HYBRID:
                lzw_compressed, lzw_code_size, unique_pixels = self.lzw.compress(data)
                frequency_table, frequency_size = self.huffman.build_frequency_table(
                    bytes_str=lzw_compressed, 
                    code_size=lzw_code_size
                )
                self.huffman.build_tree(frequency_table)
                compressed = self.huffman.compress(lzw_compressed, lzw_code_size)

                data_to_decompress = (
                    self.width.to_bytes(4, byteorder='big') + 
                    self.height.to_bytes(4, byteorder='big') + 
                    lzw_code_size.to_bytes(4, byteorder='big') + 
                    len(unique_pixels).to_bytes(4, byteorder='big') + 
                    b''.join(unique_pixels) +
                    frequency_size.to_bytes(4, byteorder='big') +
                    len(frequency_table).to_bytes(4, byteorder='big') + 
                    self.__convert_frequency_table_to_bytes(frequency_table, frequency_size)
                )
            case CompressionMethods.HUFFMAN:
                frequency_table, frequency_size = self.huffman.build_frequency_table(
                    bytes_str=data, 
                    code_size=BYTES_AMOUNT_PER_PIXEL
                )
                self.huffman.build_tree(frequency_table)
                compressed = self.huffman.compress(data, BYTES_AMOUNT_PER_PIXEL)

                data_to_decompress = (
                    self.width.to_bytes(4, byteorder='big') + 
                    self.height.to_bytes(4, byteorder='big') + 
                    frequency_size.to_bytes(4, byteorder='big') +
                    len(frequency_table).to_bytes(4, byteorder='big') + 
                    self.__convert_frequency_table_to_bytes(frequency_table, frequency_size)
                )
            case _:
                compressed, lzw_code_size, unique_pixels = self.lzw.compress(data)

                data_to_decompress = (
                    self.width.to_bytes(4, byteorder='big') + 
                    self.height.to_bytes(4, byteorder='big') + 
                    lzw_code_size.to_bytes(4, byteorder='big') + 
                    len(unique_pixels).to_bytes(4, byteorder='big') + 
                    b''.join(unique_pixels)
                )

        with open(output_file_name, "wb") as f:
            f.write(data_to_decompress + compressed)

        compressed_file_size = getsize(output_file_name)
        compressed_file_size_str = self.__get_file_size(compressed_file_size)
        size_data_to_decompress_str = self.__get_file_size(len(data_to_decompress))
        compression_ratio = (size - compressed_file_size) / size * 100

        self.text_editor.insert(END, f"Размер сжатого файла (вместе с информацией для распаковки): {compressed_file_size_str}\n")
        self.text_editor.insert(END, f"Размер информации для распаковки файла: {size_data_to_decompress_str}\n")
        self.text_editor.insert(END, "Степень сжатия файла: {:2.2f}%\n".format(compression_ratio))
        self.text_editor.insert(END, f"Файл успешно сжат ({method_name})\n", ("bold",))
        self.text_editor.update()
        print(f"\nРазмер сжатого файла (вместе с информацией для распаковки): {compressed_file_size_str}")
        print(f"\nРазмер информации для распаковки файла: {size_data_to_decompress_str}")
        print("\nСтепень сжатия файла: {:2.2f}%".format(compression_ratio))
        print(f"{purple}\nФайл успешно сжат ({method_name}){base_color}")

    def decompress(self, input_file_name: str, output_file_name: str) -> None:
        with open(input_file_name, "rb") as f:
            bytes_str = f.read()
            if not bytes_str:
                return None

        start = 0
        match self.method:
            case CompressionMethods.HYBRID:
                width = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                height = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                lzw_code_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                unique_pixels_count = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                unique_pixels = self.__convert_bytes_to_list_of_unique_pixels(
                    byte_string=bytes_str[start:start + unique_pixels_count * BYTES_AMOUNT_PER_PIXEL],
                )
                start += unique_pixels_count * BYTES_AMOUNT_PER_PIXEL
                frequency_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                frequency_table_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                frequency_table = self.__convert_bytes_to_frequency_table(
                    byte_string=bytes_str[start:start + frequency_table_size * (lzw_code_size + frequency_size)],
                    code_size=lzw_code_size,
                    frequency_size=frequency_size,
                )
                start += frequency_table_size * (lzw_code_size + frequency_size)

                self.huffman.build_tree(frequency_table)
                huffman_decompressed = self.huffman.decompress(bytes_str[start:])
                decompressed = self.lzw.decompress(
                    data=huffman_decompressed, 
                    code_size=lzw_code_size, 
                    unique_pixels=unique_pixels,
                )
            case CompressionMethods.HUFFMAN:
                width = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                height = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                frequency_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                frequency_table_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                frequency_table = self.__convert_bytes_to_frequency_table(
                    byte_string=bytes_str[start:start + frequency_table_size * (BYTES_AMOUNT_PER_PIXEL + frequency_size)],
                    code_size=BYTES_AMOUNT_PER_PIXEL,
                    frequency_size=frequency_size,
                )
                start += frequency_table_size * (BYTES_AMOUNT_PER_PIXEL + frequency_size)

                self.huffman.build_tree(frequency_table)
                decompressed = self.huffman.decompress(bytes_str[start:])
            case _:
                width = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                height = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                lzw_code_size = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                unique_pixels_count = int.from_bytes(bytes_str[start:start + 4], byteorder='big')
                start += 4
                unique_pixels = self.__convert_bytes_to_list_of_unique_pixels(
                    byte_string=bytes_str[start:start + unique_pixels_count * BYTES_AMOUNT_PER_PIXEL],
                )
                start += unique_pixels_count * BYTES_AMOUNT_PER_PIXEL
            
                decompressed = self.lzw.decompress(
                    data=bytes_str[start:], 
                    code_size=lzw_code_size, 
                    unique_pixels=unique_pixels,
                )

        image = Image.frombytes("RGB", (width, height), decompressed)
        image.save(output_file_name, "BMP")

        size_str = self.__get_file_size(getsize(output_file_name))
        
        method_name = self.compression_methods_names[self.method]
        self.text_editor.insert(END, f"Размер распакованного файла: {size_str}\n")
        self.text_editor.insert(END, f"Файл успешно распакован ({method_name})\n\n", ("bold",))
        self.text_editor.update()
        print(f"\nРазмер распакованного файла: {size_str}")
        print(f"{purple}\nФайл успешно распакован ({method_name}){base_color}\n")

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
    
    def __convert_frequency_table_to_bytes(
        self,
        frequency_table: dict[bytes, int],
        frequency_size: int,
    ) -> bytes:
        byte_string = bytes()
        for code, frequency in frequency_table.items():
            byte_string += code
            byte_string += frequency.to_bytes(frequency_size, byteorder='big')
        
        return byte_string
    
    def __convert_bytes_to_frequency_table(
        self, 
        byte_string: bytes,
        code_size: int,
        frequency_size: int,
    ) -> dict[bytes, int]:
        frequency_table = {}
        for i in range(0, len(byte_string), code_size + frequency_size):
            code = byte_string[i:i + code_size]
            frequency = byte_string[i + code_size:i + code_size + frequency_size]
            frequency_table[code] = int.from_bytes(frequency, byteorder='big')
        
        return frequency_table

    def __convert_bytes_to_list_of_unique_pixels(
        self, 
        byte_string: bytes,
    ) -> list[bytes]:
        return re.findall(
            rb"[\x00-\xff]{%d}" % BYTES_AMOUNT_PER_PIXEL, 
            byte_string,
        )
