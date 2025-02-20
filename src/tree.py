from tkinter import Text, END
from progress.bar import IncrementalBar


class Node():
    def __init__(
        self, 
        symbols: list[bytes], 
        frequency: int, 
        left=None, 
        right=None
    ):
        self.symbols = symbols
        self.frequency = frequency
        self.value = ""

        self.left  = left
        self.right = right


class Tree():
    def __init__(
        self, 
        frequency_table: dict,
        text_editor: Text,
    ) -> None:
        self.text_editor = text_editor

        self.nodes: list[Node] = list()
        self.__add_nodes(frequency_table)

        self.tree = self.__build_tree()
        self.__fill_node_value(self.tree)

    def get_code_by_symbol(self, symbol: bytes) -> str:
        return self.__find_code_by_symbol(
            symbol=symbol, 
            node=self.tree,
        )
    
    def get_symbol_by_code(self, code: str) -> bytes:
        return self.__find_symbol_by_code(
            code=code, 
            node=self.tree,
        )

    def __add_nodes(self, frequency_table: dict) -> None:
        for key in frequency_table.keys():
            if frequency_table[key] > 0:
                self.nodes.append(
                    Node(
                        symbols=[key], 
                        frequency=frequency_table[key],
                    )
                )

    def __find_index_of_min_elem(self) -> int:
        index = 0
        for i in range(1, len(self.nodes)):
            if self.nodes[i].frequency < self.nodes[index].frequency:
                index = i

        return index

    def __build_tree(self) -> Node:
        self.text_editor.insert(END, 'Построение дерева Хаффмана\n')
        self.text_editor.update()
        print()
        bar = IncrementalBar(
            'Построение дерева Хаффмана', 
            max = len(self.nodes) - 1,
        )
        while len(self.nodes) > 1:
            first_node = self.nodes.pop(self.__find_index_of_min_elem())
            second_node = self.nodes.pop(self.__find_index_of_min_elem())
            self.nodes.append(
                Node(
                    symbols=first_node.symbols + second_node.symbols, 
                    frequency=first_node.frequency + second_node.frequency,
                    left=first_node,
                    right=second_node,
                )
            )
            bar.next()
        bar.finish()

        return self.nodes[0]

    def __fill_node_value(self, node: Node) -> None:
        if node.left != None:
            node.left.value += node.value + "0"
            self.__fill_node_value(node.left)
        
        if node.right != None:
            node.right.value += node.value + "1"
            self.__fill_node_value(node.right)

    def __find_code_by_symbol(self, symbol: bytes, node: Node) -> str:
        if len(node.symbols) == 1 and node.symbols[0] == symbol:
            code = node.value  
        # есть ли искомый символ в левой части дерева
        elif symbol in node.left.symbols:
            code = self.__find_code_by_symbol(symbol, node.left)
        # есть ли искомый символ в правой части дерева
        else:
            code = self.__find_code_by_symbol(symbol, node.right)

        return code

    def __find_symbol_by_code(self, code: str, node: Node) -> bytes:
        if len(code) == 0:
            # не дошли до конца дерева, надо взять больший код
            if node.left != None or node.left != None:
                symbol = None
            else:
                symbol = node.symbols[0]

        # есть ли искомый символ в левой части дерева
        elif node.left.value[-1] == code[0]:
            symbol = self.__find_symbol_by_code(code[1:], node.left)
        # есть ли искомый символ в правой части дерева
        else:
            symbol = self.__find_symbol_by_code(code[1:], node.right)

        return symbol
