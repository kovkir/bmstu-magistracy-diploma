from tkinter import Text, END
from bitarray import bitarray
from progress.bar import IncrementalBar

from tree import Tree


class Huffman():
    def __init__(self, code_size: int, text_editor: Text) -> None:
        self.code_size = code_size
        self.text_editor = text_editor

    def fill_frequency_table(self, bytes_str: bytes) -> None:
        self.frequency_table = {}

        self.text_editor.insert(END, "Вычисление таблицы частот символов\n")
        self.text_editor.update()
        print()
        bar = IncrementalBar(
            'Вычисление таблицы частот символов', 
            max = len(bytes_str) / self.code_size,
        )
        for i in range(0, len(bytes_str) - self.code_size + 1, self.code_size):
            byte_sequence = bytes_str[i:i + self.code_size]
            self.frequency_table[byte_sequence] = \
                bytes_str.count(byte_sequence)
            
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
        )

    def compress(self, data: bytes) -> bytes:
        self.text_editor.insert(END, "Сжатие методом Хаффмана\n")
        self.text_editor.update()
        print()
        bar = IncrementalBar(
            'Сжатие методом Хаффмана', 
            max = len(data) / self.code_size,
        )
        bits_str = ""
        for i in range(0, len(data) - self.code_size + 1, self.code_size):
            byte_sequence = data[i:i + self.code_size]
            # обход дерева в поисках кода переданного символа
            bits_str += self.tree.get_code_by_symbol(byte_sequence)

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

        self.text_editor.insert(END, 'Распаковка методом Хаффмана\n')
        self.text_editor.update()
        print()
        bar = IncrementalBar(
            'Распаковка методом Хаффмана', 
            max = len(bits_str),
        )
        bytes_str = bytes()
        while len(bits_str) > 0:
            byte_sequence, lenSymbol = \
                self.__get_decompressed_symbol(bits_str)

            bytes_str += byte_sequence
            bits_str = bits_str[lenSymbol:]

            bar.next(n=lenSymbol)
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
