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
from tkinter.ttk import Progressbar

from compression import Compression
from constants import *
from color import *


class Window():
    window: Tk
    codeSizeEntry: Entry
    inputFilenameEntry: Entry
    outputDirectoryEntry: Entry
    textEditor: Text
    progressbar: Progressbar

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
            variable = self.methodVar, value = CompressionMethods.HYBRID.value,
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.35, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 220,
        )
        Radiobutton(
            text = "Метод Хаффмана", 
            variable = self.methodVar, value = CompressionMethods.HUFFMAN.value,
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
            variable = self.methodVar, value = CompressionMethods.LZW.value,
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
            highlightbackground = "white",
        )
        self.textEditor.place(
            width = windowWidth, 
            height = 240, 
            x = 0, 
            y = 300,
        )

        progressbarLabel = Label(
            bg = "white", 
        )
        progressbarLabel.place(
            width = windowWidth,
            x = 0,
            y = 540,
        )
        self.progressbar = Progressbar(
            progressbarLabel,
            orient="horizontal",
            length=windowWidth,
            maximum=100,
        )
        self.progressbar.pack()
        self.progressbar.step(0)

        Label(
            text = "ВОЗМОЖНЫЕ ДЕЙСТВИЯ", 
            font = ("Arial", 16, "bold"), bg = PURPLE_DARK, fg = "white",
        ).place(
            width = windowWidth, 
            height = 30, 
            x = 0 ,
            y = windowHeight - 90,
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
        method = CompressionMethods(self.methodVar.get())
        if method == CompressionMethods.HUFFMAN:
            codeSize = 1
        else:
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
            method=method,
            code_size=codeSize,
            text_editor=self.textEditor,
            progressbar=self.progressbar,
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

    def aboutProgram(self):
        messagebox.showinfo(
            "О программе", 
            "Реализация метода сжатия статических изображений "\
            "без потерь на основе алгоритма Хаффмана\n\n"\
            "Ковалец Кирилл ИУ7-42М (2025)"
        )

    def run(self):
        self.codeSizeEntry.insert(0, CODE_SIZE_IN_BYTES)
        self.methodVar.set(CompressionMethods.HYBRID.value)

        self.window.mainloop()
