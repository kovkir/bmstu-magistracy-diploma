from progress.bar import IncrementalBar


class LZW:
    def compress(self, data: bytes):
        # Инициализируем базовый словарь для всех возможных байтов
        dictionary = {bytes([i]): i for i in range(256)}
        chain_count = 256  # Начало пользовательских кодов
        curr_msg = bytes()
        result = []

        print()
        bar = IncrementalBar('Сжатие методом LZW', max = len(data))
        for byte in data:
            curr_char = bytes([byte])
            if curr_msg + curr_char in dictionary:
                curr_msg += curr_char
            else:
                # Добавляем код текущей последовательности в результат
                result.append(dictionary[curr_msg])
                # Добавляем новую цепочку в словарь
                if chain_count < 65536:
                    dictionary[curr_msg + curr_char] = chain_count
                    chain_count += 1

                curr_msg = curr_char
            
            bar.next()
        bar.finish()

        # Добавляем последний код, если есть
        if curr_msg:
            result.append(dictionary[curr_msg])

        # Преобразуем результат в байты (фиксированный размер кодов — 2 байта)
        compressed_data = b''.join(
            code.to_bytes(2, byteorder='big') for code in result
        )
        print(f"\nКол-во цепочек в словаре: {chain_count}")
        return compressed_data
    
    def decompress(self, compressed_data: bytes):
        # Инициализируем базовый словарь для всех возможных байтов
        inverted_dict = {i: bytes([i]) for i in range(256)}
        chain_count = 256  # Начало пользовательских кодов

        # Разбиваем данные на 2-байтовые коды
        codes = [
            int.from_bytes(compressed_data[i:i + 2], byteorder='big')
            for i in range(0, len(compressed_data), 2)
        ]

        # Восстанавливаем данные
        result = bytearray()
        prev_chain = inverted_dict[codes[0]]
        result.extend(prev_chain)

        print()
        bar = IncrementalBar('Распаковка методом LZW', max = len(codes) - 1)
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
            if chain_count < 65536:
                inverted_dict[chain_count] = prev_chain + chain[:1]
                chain_count += 1

            prev_chain = chain

            bar.next()
        bar.finish()

        return bytes(result)
