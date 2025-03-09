import re
from tkinter import Text, END
from tkinter.ttk import Progressbar
from progress.bar import IncrementalBar

from constants import BYTES_AMOUNT_PER_PIXEL


class LZW:
    def __init__(
        self,
        code_size: int, 
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.code_size = code_size
        self.text_editor = text_editor
        self.progressbar = progressbar
    
    def compress(self, data: bytes) -> bytes:
        """Сжатие данных с 3-байтовыми последовательностями (RGB)."""
        if len(data) % BYTES_AMOUNT_PER_PIXEL != 0:
            raise ValueError(f"Размер данных должен быть кратен {BYTES_AMOUNT_PER_PIXEL} (RGB-пиксели).")
        
        # Инициализация словаря всеми возможными RGB значениями
        dictionary = {
            bytes([r, g, b]): i for i, (r, g, b) in enumerate(
                ((r, g, b) 
                    for r in range(256) 
                    for g in range(256) 
                    for b in range(256)
                )
            )
        }
        chain_count = len(dictionary)
        
        max_number_of_chains = pow(2, self.code_size * 8)
        curr_msg = bytes()
        result = []

        codes: list[bytes] = re.findall(rb"[\x00-\xff]{%d}" % BYTES_AMOUNT_PER_PIXEL, data)
        size_data = len(codes)

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
                if chain_count < max_number_of_chains:
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

        self.text_editor.insert(END, f"Кол-во цепочек пикселей в словаре: {chain_count}\n")
        self.text_editor.insert(END, "Среднее число пикселей в цепочках: {:.2f}\n".format(size_data / chain_count))
        self.text_editor.update()
        print(f"\nКол-во цепочек пикселей в словаре: {chain_count}")
        print("\nСреднее число пикселей в цепочках: {:.2f}".format(size_data / chain_count))

        # Преобразуем результат в байты
        compressed_data = b''.join(
            code.to_bytes(self.code_size, byteorder='big') for code in result
        )
        return compressed_data
    
    def decompress(self, data: bytes) -> bytes:
        """Распаковка данных с 3-байтовыми RGB-последовательностями."""
        # Инициализация словаря всеми возможными 3-байтовыми значениями
        inverted_dict = {
            i: bytes([r, g, b]) for i, (r, g, b) in enumerate(
                ((r, g, b) 
                    for r in range(256) 
                    for g in range(256) 
                    for b in range(256)
                )
            )
        }
        chain_count = len(inverted_dict)

        max_number_of_chains = pow(2, self.code_size * 8)

        # Разбиваем данные на n-байтовые коды
        codes = [
            int.from_bytes(data[i:i + self.code_size], byteorder='big')
            for i in range(0, len(data), self.code_size)
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
            if chain_count < max_number_of_chains:
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
