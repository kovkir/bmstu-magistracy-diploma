from tkinter import Text, END
from tkinter.ttk import Progressbar
from bitarray import bitarray
from progress.bar import IncrementalBar

from tree import Tree


class Huffman():
    def __init__(
        self,
        code_size: int,
        text_editor: Text,
        progressbar: Progressbar,
    ) -> None:
        self.code_size = code_size
        self.text_editor = text_editor
        self.progressbar = progressbar

    def fill_frequency_table(self, bytes_str: bytes) -> None:
        self.frequency_table = {}

        size_data = len(bytes_str) / self.code_size
        bar = self.__init_progressbar(
            name="Вычисление таблицы частот символов",
            size=size_data,
        )
        for iteration, i in enumerate(
            range(0, len(bytes_str) - self.code_size + 1, self.code_size)
        ):
            byte_sequence = bytes_str[i:i + self.code_size]
            self.frequency_table[byte_sequence] = \
                bytes_str.count(byte_sequence)
            
            self.__update_progressbar(
                iteration=iteration + 1,
                size=size_data,
            )
            bar.next()
        bar.finish()

        self.text_editor.insert(
            END, 
            "Среднее кол-во повторных использований цепочек байт: {:.2f}\n".format(
            len(bytes_str) / self.code_size / len(self.frequency_table)
        ))
        self.text_editor.update()
        print("\nСреднее кол-во повторных использований цепочек байт: {:.2f}".format(
            len(bytes_str) / self.code_size / len(self.frequency_table)
        ))

    def build_tree(self) -> None:
        self.tree = Tree(
            frequency_table=self.frequency_table,
            text_editor=self.text_editor,
            progressbar=self.progressbar,
        )

    def compress(self, data: bytes) -> bytes:
        size_data = len(data) / self.code_size
        bar = self.__init_progressbar(
            name="Сжатие методом Хаффмана",
            size=size_data,
        )
        bits_str = ""
        for iteration, i in enumerate(
            range(0, len(data) - self.code_size + 1, self.code_size)
        ):
            byte_sequence = data[i:i + self.code_size]
            # обход дерева в поисках кода переданного символа
            bits_str += self.tree.get_code_by_symbol(byte_sequence)

            self.__update_progressbar(
                iteration=iteration + 1,
                size=size_data,
            )
            bar.next()
        bar.finish()

        self.bits_in_msg_count = len(bits_str)
        bits = self.__add_zeros_to_bits(
            bits=bitarray(bits_str), 
            multiplicity=8,
        )
  
        return self.__to_bytes(bits)

    def decompress(self, data: bytes) -> bytes:
        bits = self.__to_bits(data)
        bits_str = bits[:self.bits_in_msg_count].to01()

        size_data = len(bits_str)
        bar = self.__init_progressbar(
            name="Распаковка методом Хаффмана",
            size=size_data,
        )
        bytes_str = bytes()
        amount_processed_chars = 0
        while len(bits_str) > 0:
            byte_sequence, len_symbol = \
                self.__get_decompressed_symbol(bits_str)

            bytes_str += byte_sequence
            bits_str = bits_str[len_symbol:]
            amount_processed_chars += len_symbol

            self.__update_progressbar(
                iteration=amount_processed_chars,
                size=size_data,
            )
            bar.next(n=len_symbol)
        bar.finish()
        
        return bytes_str
    
    def __add_zeros_to_bits(
        self, 
        bits: bitarray, 
        multiplicity: int,
    ) -> bitarray:
        return bits + bitarray("0" * (len(bits) % multiplicity))

    def __to_bytes(self, bits: bitarray) -> bytes:
        return bits.tobytes()
    
    def __to_bits(self, bytes_str: bytes) -> bitarray:
        bits = bitarray()
        bits.frombytes(bytes_str)
        return bits
    
    def __get_decompressed_symbol(
        self, 
        bits_str: str,
    ) -> tuple[bytes, int] | None:
        for i in range(1, len(bits_str) + 1):
            # обход дерева в поисках символа переданного кода
            symbol = self.tree.get_symbol_by_code(bits_str[:i])
            if symbol != None:
                return symbol, i
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
