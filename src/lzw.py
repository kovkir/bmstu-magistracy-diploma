from tkinter import Text, END
from tkinter.ttk import Progressbar
from progress.bar import IncrementalBar


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
        dictionary = {bytes([i]): i for i in range(256)}
        chain_count = 256
        max_number_of_chains = pow(256, self.code_size)

        curr_msg = bytes()
        result = []

        size_data = len(data)
        bar = self.__init_progressbar(
            name="Сжатие методом LZW",
            size=size_data,
        )
        for i, byte in enumerate(data):
            curr_char = bytes([byte])
            if curr_msg + curr_char in dictionary:
                curr_msg += curr_char
            else:
                # Добавляем код текущей последовательности в результат
                result.append(dictionary[curr_msg])
                # Добавляем новую цепочку в словарь
                if chain_count < max_number_of_chains:
                    dictionary[curr_msg + curr_char] = chain_count
                    chain_count += 1

                curr_msg = curr_char
            
            self.__update_progressbar(
                iteration=i + 1,
                size=size_data,
            )
            bar.next()
        bar.finish()

        # Добавляем последний код, если есть
        if curr_msg:
            result.append(dictionary[curr_msg])

        self.text_editor.insert(END, f"Кол-во цепочек байт в словаре: {chain_count}\n")
        self.text_editor.insert(END, "Среднее число байт в цепочках: {:.2f}\n".format(size_data / chain_count))
        self.text_editor.update()
        print(f"\nКол-во цепочек байт в словаре: {chain_count}")
        print("\nСреднее число байт в цепочках: {:.2f}".format(size_data / chain_count))

        # Преобразуем результат в байты
        compressed_data = b''.join(
            code.to_bytes(self.code_size, byteorder='big') for code in result
        )
        return compressed_data
    
    def decompress(self, data: bytes) -> bytes:
        inverted_dict = {i: bytes([i]) for i in range(256)}
        chain_count = 256
        max_number_of_chains = pow(256, self.code_size)

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
                chain = prev_chain + prev_chain[:1]
            else:
                raise ValueError("Неверный код в сжатых данных")

            result.extend(chain)

            # Добавляем новую цепочку в словарь
            if chain_count < max_number_of_chains:
                inverted_dict[chain_count] = prev_chain + chain[:1]
                chain_count += 1

            prev_chain = chain

            self.__update_progressbar(
                iteration=i + 1,
                size=size_data,
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
