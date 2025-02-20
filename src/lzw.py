from tkinter import Text
from progress.bar import IncrementalBar


class LZW:
    def __init__(self, code_size: int, text_editor: Text) -> None:
        self.code_size = code_size
        self.text_editor = text_editor
        
    def compress(self, data: bytes) -> bytes:
        dictionary = {bytes([i]): i for i in range(256)}
        chain_count = 256
        max_number_of_chains = pow(256, self.code_size)

        curr_msg = bytes()
        result = []

        print()
        bar = IncrementalBar(
            'Сжатие методом LZW', 
            max = len(data),
        )
        for byte in data:
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
            
            bar.next()
        bar.finish()

        # Добавляем последний код, если есть
        if curr_msg:
            result.append(dictionary[curr_msg])

        print(f"\nКол-во цепочек байт в словаре: {chain_count}")
        print("\nСреднее число байт в цепочках: {:.2f}".format(len(data) / chain_count))

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

        print()
        bar = IncrementalBar(
            'Распаковка методом LZW', 
            max = len(codes) - 1,
        )
        for code in codes[1:]:
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

            bar.next()
        bar.finish()

        return bytes(result)
