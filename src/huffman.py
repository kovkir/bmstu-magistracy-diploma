import re
from tkinter import Text, END
from tkinter.ttk import Progressbar
from bitarray import bitarray
from progress.bar import IncrementalBar

from tree import Tree


class Huffman():
    def __init__(
        self,
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.text_editor = text_editor
        self.progressbar = progressbar
    
    def build_frequency_table(
        self, 
        bytes_str: bytes, 
        code_size: int,
    ) -> tuple[dict[bytes, int], int]:
        codes: list[bytes] = re.findall(rb"[\x00-\xff]{%d}" % code_size, bytes_str)
        size_data = len(codes)

        frequency_table = {}

        bar = self.__init_progressbar(
            name="Вычисление таблицы частот символов",
            size=size_data,
        )
        for i, code in enumerate(codes):
            if code not in frequency_table:
                frequency_table[code] = 1
            else: 
                frequency_table[code] += 1

            self.__update_progressbar(
                iteration=i + 1,
                size=size_data,
            )
            bar.next()
        bar.finish()

        size_table = len(frequency_table)
        max_frequency = max(frequency_table.values())
        frequency_size = self.__calculate_number_size_in_bytes(max_frequency)
        
        self.text_editor.insert(END, f"Размер таблицы частот символов: {size_table}\n")
        self.text_editor.insert(
            END, 
            "Максимальная частота символа: {} ({} байт(а) на сохранение частоты символа) \n".format(
            max_frequency, frequency_size
        ))
        self.text_editor.insert(
            END, 
            "Среднее кол-во повторных использований цепочек байт: {:.2f}\n".format(
            size_data / size_table
        ))
        self.text_editor.update()
        print(f"\nРазмер таблицы частот символов: {size_table}")
        print("\nМаксимальная частота символа: {} ({} байт(а) на сохранение частоты)".format(
            max_frequency, frequency_size
        ))
        print("\nСреднее кол-во повторных использований цепочек байт: {:.2f}".format(
            size_data / size_table
        ))

        return frequency_table, frequency_size

    def build_tree(self, frequency_table: dict[bytes, int]) -> Tree:
        return Tree(
            frequency_table=frequency_table,
            text_editor=self.text_editor,
            progressbar=self.progressbar,
        )

    def compress(self, data: bytes, code_size: int, tree: Tree) -> bytes:
        codes: list[bytes] = re.findall(rb"[\x00-\xff]{%d}" % code_size, data)
        size_data = len(codes)

        bar = self.__init_progressbar(
            name="Сжатие методом Хаффмана",
            size=size_data,
        )
        bits_str = ""
        for i, code in enumerate(codes):
            # обход дерева в поисках кода переданного символа
            bits_str += tree.get_code_by_symbol(code)

            self.__update_progressbar(
                iteration=i + 1,
                size=size_data,
            )
            bar.next()
        bar.finish()

        bits = self.__add_missing_bits(
            bits=bitarray(bits_str), 
            multiplicity=8,
        )

        return self.__to_bytes(bits)

    def decompress(self, data: bytes, tree: Tree) -> bytes:
        bits = self.__to_bits(data)
        bits_str = self.__remove_extra_bits(bits).to01()

        size_data = len(bits_str)
        bar = self.__init_progressbar(
            name="Распаковка методом Хаффмана",
            size=size_data,
        )
        bytes_str = bytes()
        amount_processed_chars = 0
        while amount_processed_chars < size_data:
            byte_sequence, len_symbol = self.__get_decompressed_symbol(
                bits_str=bits_str, 
                initial_index=amount_processed_chars,
                tree=tree,
            )
            bytes_str += byte_sequence
            amount_processed_chars += len_symbol

            self.__update_progressbar(
                iteration=amount_processed_chars,
                size=size_data,
            )
            bar.next(n=len_symbol)
        bar.finish()
        
        return bytes_str
    
    def __add_missing_bits(
        self, 
        bits: bitarray, 
        multiplicity: int,
    ) -> bitarray:
        bits += bitarray("1")
        return bits + bitarray("0" * (len(bits) % multiplicity))
    
    def __remove_extra_bits(self, bits: bitarray) -> bitarray:
        counter = 1
        for i in range(len(bits) - 1, 0, -1):
            if bits[i] == 0:
                counter += 1
            else:
                break

        return bits[:-counter]

    def __to_bytes(self, bits: bitarray) -> bytes:
        return bits.tobytes()
    
    def __to_bits(self, bytes_str: bytes) -> bitarray:
        bits = bitarray()
        bits.frombytes(bytes_str)
        return bits
    
    def __get_decompressed_symbol(
        self, 
        bits_str: str,
        initial_index: int,
        tree: Tree,
    ) -> tuple[bytes, int] | None:
        for i in range(initial_index, len(bits_str) + 1):
            # обход дерева в поисках символа переданного кода
            symbol = tree.get_symbol_by_code(bits_str[initial_index:i])
            if symbol != None:
                return symbol, i - initial_index
            # иначе не дошли до конца дерева, надо взять больший код

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

    def __calculate_number_size_in_bytes(self, number: int) -> int:
        return (number.bit_length() + 7) // 8
    