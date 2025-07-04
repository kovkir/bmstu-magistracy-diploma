import re
from tkinter import Text, END
from tkinter.ttk import Progressbar
from progress.bar import IncrementalBar

from constants import BYTES_AMOUNT_PER_PIXEL


class LZW:
    def __init__(
        self,
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.text_editor = text_editor
        self.progressbar = progressbar
    
    def compress(self, data: bytes) -> tuple[bytes, int, list[bytes]]:
        """Сжатие данных с 3-байтовыми последовательностями (RGB)."""
        if len(data) % BYTES_AMOUNT_PER_PIXEL != 0:
            raise ValueError(f"Размер данных должен быть кратен {BYTES_AMOUNT_PER_PIXEL} (RGB-пиксели).")

        codes: list[bytes] = re.findall(b"[\x00-\xff]{%d}" % BYTES_AMOUNT_PER_PIXEL, data)
        size_data = len(codes)

        unique_pixels = self.__get_unique_pixels(codes)
        dictionary = self.__get_initial_dictionary(unique_pixels)
        chain_count = len(dictionary)

        curr_msg = bytes()
        result = []

        bar = self.__init_progressbar(
            name="Сжатие методом LZW",
            size=size_data,
        )
        for i, code in enumerate(codes):
            if curr_msg + code in dictionary:
                curr_msg += code
            else:
                # Добавляем код текущей последовательности в результат
                result.append(dictionary[curr_msg])
                # Добавляем новую цепочку в словарь
                dictionary[curr_msg + code] = chain_count
                chain_count += 1
                curr_msg = code
            
            self.__update_progressbar(
                iteration=i + 1, 
                size=size_data
            )
            bar.next()
        bar.finish()

        # Добавляем последний код, если есть
        if curr_msg:
            result.append(dictionary[curr_msg])

        code_size = self.__calculate_code_size(chain_count)

        self.text_editor.insert(END, f"Кол-во цепочек пикселей в словаре: {chain_count}\n")
        self.text_editor.insert(END, f"Размер кода для метода LZW в байтах: {code_size}\n")
        self.text_editor.insert(END, "Среднее число пикселей в цепочках: {:.2f}\n".format(size_data / chain_count))
        self.text_editor.update()
        print(f"\nКол-во цепочек пикселей в словаре: {chain_count}")
        print(f"\nРазмер кода для метода LZW в байтах: {code_size}")
        print("\nСреднее число пикселей в цепочках: {:.2f}".format(size_data / chain_count))

        # Преобразуем результат в байты
        compressed_data = b''.join(
            code.to_bytes(code_size, byteorder='big') for code in result
        )
        return compressed_data, code_size, unique_pixels
    
    def decompress(self, data: bytes, code_size: int, unique_pixels: list[bytes]) -> bytes:
        """Распаковка данных с 3-байтовыми RGB-последовательностями."""
        inverted_dict = self.__get_inverted_initial_dictionary(unique_pixels)
        chain_count = len(inverted_dict)

        # Разбиваем данные на n-байтовые коды
        codes = [
            int.from_bytes(data[i:i + code_size], byteorder='big')
            for i in range(0, len(data), code_size)
        ]

        # Восстанавливаем данные
        result = bytearray()
        prev_chain = inverted_dict[codes[0]]
        result.extend(prev_chain)

        size_data = len(codes) - 1
        bar = self.__init_progressbar(
            name="Распаковка методом LZW",
            size=size_data,
        )
        for i, code in enumerate(codes[1:]):
            if code in inverted_dict:
                chain = inverted_dict[code]
            elif code == chain_count:
                # Специальный случай: новый код, равный следующему индексу
                chain = prev_chain + prev_chain[:BYTES_AMOUNT_PER_PIXEL]
            else:
                raise ValueError("Неверный код в сжатых данных")

            result.extend(chain)

            # Добавляем новую цепочку в словарь
            inverted_dict[chain_count] = prev_chain + chain[:BYTES_AMOUNT_PER_PIXEL]
            chain_count += 1
            prev_chain = chain

            self.__update_progressbar(
                iteration=i + 1, 
                size=size_data
            )
            bar.next()
        bar.finish()

        return bytes(result)
    
    def __get_unique_pixels(self, codes: list[bytes]) -> list[bytes]:
        pixels = []
        for code in codes:
            if code not in pixels:
                pixels.append(code)

        size = len(pixels)
        self.text_editor.insert(END, f"Кол-во различных пикселей в изображении: {size}\n")
        self.text_editor.update()
        print(f"\nКол-во различных пикселей в изображении: {size}")

        return pixels
    
    def __get_initial_dictionary(self, pixels: list[bytes]) -> dict[bytes, int]:
        dictionary = {}
        chain_count = 0
        for pixel in pixels:
            dictionary[pixel] = chain_count
            chain_count += 1

        return dictionary
    
    def __get_inverted_initial_dictionary(self, pixels: list[bytes]) -> dict[int, bytes]:
        dictionary = {}
        chain_count = 0
        for pixel in pixels:
            dictionary[chain_count] = pixel
            chain_count += 1

        return dictionary
    
    def __init_progressbar(self, name: str, size: int) -> IncrementalBar:
        self.text_editor.insert(END, f"{name}\n")
        self.text_editor.update()
        
        self.progressbar.step(0)
        self.progressbar.update()
        print()

        return IncrementalBar(name, max=size)
    
    def __update_progressbar(self, iteration: int, size: int) -> None:
        percent = round(iteration / size * 100)
        if self.progressbar['value'] + 5 <= percent:
            self.progressbar['value'] = percent
            self.progressbar.update()

    def __calculate_code_size(self, number: int) -> int:
        return (number.bit_length() + 7) // 8
