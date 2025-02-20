import os
from tkinter import (
    Tk, 
    Label, 
    Entry, 
    Radiobutton, 
    IntVar,
    Button, 
    messagebox, 
    filedialog, 
    Text, 
    END,
    DISABLED,
)

from compression import Compression
from constants import *
from color import *


class Window():
    window: Tk
    codeSizeEntry: Entry
    inputFilenameEntry: Entry
    outputDirectoryEntry: Entry
    textEditor: Text

    def __init__(self, windowWidth: int, windowHeight: int):
        self.window = self.createWindow(windowWidth, windowHeight)
        self.createInterface(windowWidth, windowHeight)

    def createWindow(self, windowWidth: int, windowHeight: int):
        window = Tk()
        window.title("Выпускная квалификационная работа (Ковалец Кирилл ИУ7-42М)")
        window.geometry("{0}x{1}".format(windowWidth, windowHeight))
        window.resizable(False, False)
        window["bg"] = PURPLE_LIGHT

        return window

    def createInterface(self, windowWidth: int, windowHeight: int):
        Label(
            text = "ВХОДНЫЕ ДАННЫЕ", 
            font = ("Arial", 16, "bold"), 
            bg = PURPLE_DARK, 
            fg = "white",
        ).place(
            width = windowWidth, 
            height = 30, 
            x = 0 , 
            y = 10,
        )

        Label(
            text = "Размер кода для метода LZW в байтах", 
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
        ).place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 50,
        )
        self.codeSizeEntry = Entry(
            font = ("Arial", 14),
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.codeSizeEntry.place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.52, 
            y = 50,
        )

        Label(
            text = "Путь до исходного файла", 
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
        ).place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 90,
        )
        self.inputFilenameEntry = Entry(
            font = ("Arial", 14),
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.inputFilenameEntry.place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.52, 
            y = 90,
        )

        Label(
            text = "Путь до директории с результатами", 
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
        ).place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 130,
        )
        self.outputDirectoryEntry = Entry(
            font = ("Arial", 14),
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.outputDirectoryEntry.place(
            width = windowWidth * 0.38, 
            height = 30, 
            x = windowWidth * 0.52, 
            y = 130,
        )
        
        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.38, 
            height = 40, 
            x = windowWidth * 0.1, 
            y = 170,
        )
        Button(
            text = "Выбрать исходный файл", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE,
            highlightthickness = 30, 
            command = lambda: self.setInputFilenameEntry(),
        ).place(
            width = windowWidth * 0.38 - 4, 
            height = 36, 
            x = windowWidth * 0.1 + 2, 
            y = 172,
        )
        
        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.38, 
            height = 40, 
            x = windowWidth * 0.52, 
            y = 170,
        )
        Button(
            text = "Выбрать директорию для результатов", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = lambda: self.setOutputDirectoryEntry(),
        ).place(
            width = windowWidth * 0.38 - 4, 
            height = 36, 
            x = windowWidth * 0.52 + 2, 
            y = 172,
        )

        self.methodVar = IntVar()

        Radiobutton(
            text = "Разработанный гибридный метод", 
            variable = self.methodVar, value = HYBRID,
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.3, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 220,
        )
        Radiobutton(
            text = "Метод Хаффмана", 
            variable = self.methodVar, value = HUFFMAN,
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.2, 
            height = 30, 
            x = windowWidth * 0.45,
            y = 220,
        )
        Radiobutton(
            text = "Метод LZW", 
            variable = self.methodVar, value = LZW,
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.2, 
            height = 30, 
            x = windowWidth * 0.7, 
            y = 220,
        )

        Label(
            text = "ЭТАПЫ СЖАТИЯ И РАСПАКОВКИ ИЗОБРАЖЕНИЙ",
            font = ("Arial", 16, "bold"), 
            bg = PURPLE_DARK, 
            fg = "white",
        ).place(
            width = windowWidth, 
            height = 30, 
            x = 0, 
            y = 260,
        )
        self.textEditor = Text(
            font = ("Arial", 16), 
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.textEditor.place(
            width = windowWidth, 
            height = 260, 
            x = 0, 
            y = 300,
        )

        Label(
            text = "ВОЗМОЖНЫЕ ДЕЙСТВИЯ", 
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white",
        ).place(
            width = windowWidth, height = 30, 
            x = 0 , y = windowHeight - 90,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 40, 
            x = windowWidth * 0.1, 
            y = windowHeight - 50,
        )
        Button(
            text = "Сжать и рапаковать", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = lambda: self.startEncryption(),
        ).place(
            width = windowWidth * 0.24 - 4, 
            height = 36, 
            x = windowWidth * 0.1 + 2, 
            y = windowHeight - 48,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 40, 
            x = windowWidth * 0.38, 
            y = windowHeight - 50,
        )
        Button(
            text = "Сравнить методы", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = lambda: self.aboutProgram(),
        ).place(
            width = windowWidth * 0.24 - 4, 
            height = 36, 
            x = windowWidth * 0.38 + 2, 
            y = windowHeight - 48,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 40, 
            x = windowWidth * 0.66, 
            y = windowHeight - 50,
        )
        Button(
            text = "О программе", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = lambda: self.aboutProgram(),
        ).place(
            width = windowWidth * 0.24 - 4, 
            height = 36, 
            x = windowWidth * 0.66 + 2, 
            y = windowHeight - 48,
        )
    
    def setInputFilenameEntry(self) -> None:
        filepath = filedialog.askopenfilename()
        if filepath != "":
            self.inputFilenameEntry.delete(0, END)
            self.inputFilenameEntry.insert(0, filepath)

    def setOutputDirectoryEntry(self) -> None:
        filepath = filedialog.askdirectory()
        if filepath != "":
            self.outputDirectoryEntry.delete(0, END)
            self.outputDirectoryEntry.insert(0, filepath)
    
    def startEncryption(self) -> None:
        codeSize = self.getCodeSize()
        if codeSize is None:
            return
        
        inputFile = self.getInputFile()
        if inputFile is None:
            return
        
        outputDirectory = self.getOutputDirectory()
        if outputDirectory is None:
            return

        compressor = Compression(
            code_size=codeSize,
            text_editor=self.textEditor,
        )
        compressor.compress(
            inputFile,
            outputDirectory + "/compressed.bin",
        )
        compressor.decompress(
            outputDirectory + "/compressed.bin",
            outputDirectory + "/decompressed." + inputFile.split(".")[-1],
        )

    def getOutputDirectory(self) -> str | None:
        path = self.outputDirectoryEntry.get()
        if not os.path.exists(path) or not os.path.isdir(path):
            messagebox.showwarning(
                "Ошибка",
                "Директории с таким имененм не существует!"
            )
            return
        
        return path
    
    def getInputFile(self) -> str | None:
        path = self.inputFilenameEntry.get()
        if not os.path.exists(path) or not os.path.isfile(path):
            messagebox.showwarning(
                "Ошибка",
                "Файла с таким имененм не существует!"
            )
            return
        
        return path
    
    def getCodeSize(self) -> int | None:
        try:
            codeSize = int(self.codeSizeEntry.get())
        except:
            codeSize = None
        
        if codeSize is None or \
           codeSize < 1 or codeSize > 8:
            messagebox.showwarning(
                "Ошибка",
                "Невозможное значение размера кода для метода LZW в байтах!\n"
                "Ожидался ввод натурального числа в диапазоне от 1 до 8."
            )
            return
        
        return codeSize
    
    
    # def getNumberRuns(self) -> Union[int, None]:
    #     try:
    #         numberRuns = int(self.numberRuns.get())
    #     except:
    #         numberRuns = None
        
    #     if numberRuns == None or numberRuns < 1:
    #         messagebox.showwarning("Ошибка",
    #             "Невозможное значение количества прогонов!\n"
    #             "Ожидался ввод натурального числа.")
    #         return
        
    #     return numberRuns
    

    # def doClustering(self):
    #     numberObjects = self.getNumberObjects()
    #     if numberObjects == None:
    #         return

    #     numberClusters = self.getNumberClusters(numberObjects)
    #     if numberClusters == None:
    #         return
        
    #     objects = self.objects[:numberObjects]

    #     if self.methodVar.get() == HA:
    #         distance = Distance()
    #         dissimilarityMatrix = distance.createDissimilarityMatrix(objects)

    #         haClusterization = HAClusterization(dissimilarityMatrix)
    #         haClusterization.buildDendrogram()

    #     elif self.methodVar.get() == K_PROTOTYPES:
    #         kPrototypesClusterization = KPrototypesClusterization(objects, numberClusters)
    #         kPrototypesClusterization.buildGraph()

    #     elif self.methodVar.get() == HYBRID:
    #         hybridClusterization = HybridClusterization(objects, numberClusters)
    #         hybridClusterization.buildGraph()


    # def doComparison(self):
    #     numberObjects = self.getNumberObjects()
    #     if numberObjects == None:
    #         return

    #     numberRuns = self.getNumberRuns()
    #     if numberRuns == None:
    #         return
        
    #     objects = self.objects[:numberObjects]

    #     if self.comparisonVar.get() == ELBOW:
    #         test = TestElbow(objects, numberRuns)
    #         test.comparisonMethods()

    #     elif self.comparisonVar.get() == EVALUATION_SILHOUETTES:
    #         test = TestSilhouettes(objects, numberRuns)
    #         test.comparisonMethods()
    

    def aboutProgram(self):
        messagebox.showinfo(
            "О программе", 
            "Реализация метода сжатия статических изображений "\
            "без потерь на основе алгоритма Хаффмана\n\n"\
            "Ковалец Кирилл ИУ7-42М (2025)"
        )

    def run(self):
        self.codeSizeEntry.insert(0, CODE_SIZE_IN_BYTES)
        self.methodVar.set(HYBRID)

        self.window.mainloop()
