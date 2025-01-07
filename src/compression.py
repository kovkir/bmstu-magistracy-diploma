from huffman import Huffman
from lzw import LZW
from color import *


class Compression():
    huffman: Huffman
    lzw: LZW
    countBitsMsg: int

    def __init__(self):
        self.huffman = Huffman()
        self.lzw = LZW()

    def compress(self, inputFileName: str, outputFileName: str):
        inputFile = open(inputFileName, "rb")
        outputFile = open(outputFileName, "wb")

        data = inputFile.read()
        lzw_compressed = self.lzw.compress(data)

        self.huffman.fillFrequencyTable(lzw_compressed)
        self.huffman.buildTree()

        huffman_compressed = self.huffman.compress(lzw_compressed)
        outputFile.write(huffman_compressed)

        inputFile.close()
        outputFile.close()

        print(f"{purple}\nФайл успешно сжат (LZW + Хаффман){base_color}")

    def decompress(self, inputFileName: str, outputFileName: str):
        inputFile = open(inputFileName, "rb")
        outputFile = open(outputFileName, "wb")

        bytesStr = inputFile.read()
        if not bytesStr:
            return None

        huffman_decompressed = self.huffman.decompress(bytesStr)
        lzw_decompressed = self.lzw.decompress(huffman_decompressed)

        outputFile.write(lzw_decompressed)

        inputFile.close()
        outputFile.close()

        print(f"{purple}\nФайл успешно распакован (Хаффман + LZW){base_color}\n")
