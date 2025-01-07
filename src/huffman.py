from bitarray import bitarray
from progress.bar import IncrementalBar

from tree import Tree


class Huffman():
    frequencyTable: dict
    tree: Tree
    countBitsMsg: int

    def multipleLength(self, bitsArr: bitarray, numb):
        return bitsArr + bitarray("0" * (len(bitsArr) % numb))

    def toBits(self, bytesStr: bytes):
        bitsArr = bitarray()
        bitsArr.frombytes(bytesStr)
        return bitsArr

    def toBytes(self, bitsArr: bitarray):
        return bitsArr.tobytes()

    def fillFrequencyTable(self, bytesStr: bytes):
        self.frequencyTable = {bytes([i]): 0 for i in range(256)}

        print()
        bar = IncrementalBar('Вычисление таблицы частот символов', max = len(bytesStr))
        for i in bytesStr:
            self.frequencyTable[bytes([i])] = bytesStr.count(i)
            bar.next()
        bar.finish()

    def buildTree(self):
        self.tree = Tree(self.frequencyTable)

    def compress(self, data: bytes) -> str:
        print()
        bar = IncrementalBar('Сжатие методом Хаффмана', max = len(data))
        bitsStr = ""
        for byte in data:
            # обход дерева в поисках кода переданного символа
            bitsStr += self.tree.getCodeBySymbol(bytes([byte]))
            bar.next()
        bar.finish()

        self.countBitsMsg = len(bitsStr)
        bitsArr = self.multipleLength(bitarray(bitsStr), 8)
  
        return self.toBytes(bitsArr)

    def getDecompressedSymbol(self, bitsStr: str) -> bytes:
        for i in range(1, len(bitsStr) + 1):
            # обход дерева в поисках символа переданного кода
            symbol = self.tree.getSymbolByCode(bitsStr[:i])
            
            if symbol != None:
                return symbol, i
            # иначе не дошли до конца дерева, надо взять больший код

    def decompress(self, data: bytes) -> bytes:
        bitsArr = self.toBits(data)
        bitsStr = bitsArr[:self.countBitsMsg].to01()

        print()
        bar = IncrementalBar('Распаковка методом Хаффмана', max = len(bitsStr))
        bytesStr = bytes()
        while len(bitsStr) > 0:
            byte, lenSymbol = self.getDecompressedSymbol(bitsStr)

            bytesStr += byte
            bitsStr = bitsStr[lenSymbol:]

            bar.next(n=lenSymbol)
        bar.finish()
        
        return bytesStr
