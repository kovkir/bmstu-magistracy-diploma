import subprocess
from compression import Compression
from color import *


INPUT_DATA_FOLDER = "../input_date/"
OUTPUT_DATA_FOLDER = "../output_date/"


def getInputFile():
    listFiles = subprocess.getoutput("cd " + INPUT_DATA_FOLDER + " && ls").split("\n")

    print(f"\n{yellow}Выберете входной файл для сжатия алгоритмом Хафмана:{base_color}")
    
    for i in range(len(listFiles)):
        print(f"\t{blue}{i + 1}.{base_color} {listFiles[i]}")

    try:
        fileNumber = input(f"\n{green}Номер выбранного файла: {base_color}")
        if int(fileNumber) <= 0:
            print(f"\n{red}Номер команды должен быть > 0!{base_color}\n")
        else:
            filePath = INPUT_DATA_FOLDER + listFiles[int(fileNumber) - 1]
            return filePath
    except:
        print(f"\n{red}Ввод некоректных данных!{base_color}\n")


def startEncryption(filePath):
    compressor = Compression()
    compressor.compress(
        filePath,
        OUTPUT_DATA_FOLDER + "compressed.bin",
    )
    compressor.decompress(
        OUTPUT_DATA_FOLDER + "compressed.bin",
        OUTPUT_DATA_FOLDER + "decompressed." + filePath.split(".")[-1],
    )


def main():
    filePath = getInputFile()
    if filePath != None:
        startEncryption(filePath)


if __name__ == "__main__":
    main()
