from enum import Enum

# размеры окна приложения
WINDOW_WIDTH  = 1100
WINDOW_HEIGHT = 1020 # 660

# количество байт на пиксель
BYTES_AMOUNT_PER_PIXEL = 3

# методы сжатия для выбора
class CompressionMethods(Enum):
    HYBRID  = 0
    HUFFMAN = 1
    LZW     = 2

# пути к изображениям для тестирования
IMAGE_PATHS = [
    "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/sunrise.bmp",
    "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/mars.bmp",
    "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/wheat.bmp",
    "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/forest.bmp",
    "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/girl.bmp",
]
# степени сжатия изображений для каждого метода
COMPRESSION_RATES = {
    CompressionMethods.HYBRID: [75.29, 78.30, 70.52, 54.23, 48.05],
    CompressionMethods.HUFFMAN: [69.91, 71.59, 68.02, 67.77, 59.23],
    CompressionMethods.LZW: [83.01, 84.61, 77.67, 44.52, 40.84],
}
# кол-во информации для распаковки изображения в сжатом файле для каждого метода
INFORMATION_TO_DECOMPRESS = {
    CompressionMethods.HYBRID: [41.20, 41.81, 39.07, 33.50, 39.05],
    CompressionMethods.HUFFMAN: [0.51, 0.72, 0.88, 0.73, 6.59],
    CompressionMethods.LZW: [0.53, 0.77, 0.76, 0.25, 2.72],
}
