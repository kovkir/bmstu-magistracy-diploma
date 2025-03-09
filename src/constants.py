from enum import Enum

# размеры окна приложения
WINDOW_WIDTH  = 1100
WINDOW_HEIGHT = 660

# размер кода в байтах для метода LZW в байтах
CODE_SIZE_IN_BYTES = 4
# количество байт на пиксель
BYTES_AMOUNT_PER_PIXEL = 3

# методы сжатия для выбора
class CompressionMethods(Enum):
    HYBRID  = 0
    HUFFMAN = 1
    LZW     = 2
