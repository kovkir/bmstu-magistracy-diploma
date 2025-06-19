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
from comparison import plot_comparison_graph
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
            x = 0,
            y = 10,
        )

        Label(
            text = "Путь до исходного файла", 
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
        ).place(
            width = windowWidth * 0.38, 
            height = 35, 
            x = windowWidth * 0.1, 
            y = 50,
        )
    
        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.38, 
            height = 35, 
            x = windowWidth * 0.52, 
            y = 50,
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
            height = 31, 
            x = windowWidth * 0.52 + 2, 
            y = 52,
        )

        self.inputFilenameEntry = Entry(
            font = ("Arial", 14),
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.inputFilenameEntry.place(
            width = windowWidth * 0.8, 
            height = 35, 
            x = windowWidth * 0.1, 
            y = 95,
        )

        Label(
            text = "Путь до директории с результатами", 
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
        ).place(
            width = windowWidth * 0.38, 
            height = 35, 
            x = windowWidth * 0.1, 
            y = 140,
        )
        
        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.38, 
            height = 35, 
            x = windowWidth * 0.52, 
            y = 140,
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
            height = 31, 
            x = windowWidth * 0.52 + 2, 
            y = 142,
        )

        self.outputDirectoryEntry = Entry(
            font = ("Arial", 14),
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE_DARK,
        )
        self.outputDirectoryEntry.place(
            width = windowWidth * 0.8, 
            height = 35, 
            x = windowWidth * 0.1, 
            y = 185,
        )

        self.methodVar = IntVar()

        Radiobutton(
            text = "Разработанный метод", 
            variable = self.methodVar, value = CompressionMethods.HYBRID.value,
            font = ("Arial", 16),
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.3, 
            height = 30, 
            x = windowWidth * 0.1, 
            y = 230,
        )
        Radiobutton(
            text = "Метод Хаффмана", 
            variable = self.methodVar, value = CompressionMethods.HUFFMAN.value,
            font = ("Arial", 16), 
            bg = PURPLE_LIGHT, 
            fg = PURPLE_SUPER_DARK,
            anchor = "w",
        ).place(
            width = windowWidth * 0.3, 
            height = 30, 
            x = windowWidth * 0.4,
            y = 230,
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
            y = 230,
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
            y = 270,
        )
        self.textEditor = Text(
            font = ("Arial", 16), 
            bg = "white", 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = "white",
        )
        self.textEditor.place(
            width = windowWidth, 
            height = windowHeight - 110 - 310, 
            x = 0, 
            y = 310,
        )
        self.textEditor.tag_configure("bold", font=("Arial", 16, "bold"))
        self.textEditor.tag_configure("center", justify="center")

        progressbarLabel = Label(
            bg = "white", 
        )
        progressbarLabel.place(
            width = windowWidth,
            x = 0,
            y = windowHeight - 110,
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
            y = windowHeight - 85,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 35, 
            x = windowWidth * 0.1, 
            y = windowHeight - 45,
        )
        Button(
            text = "Сжать и распаковать", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = lambda: self.startEncryption(),
        ).place(
            width = windowWidth * 0.24 - 4, 
            height = 31, 
            x = windowWidth * 0.1 + 2, 
            y = windowHeight - 43,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 35, 
            x = windowWidth * 0.38, 
            y = windowHeight - 45,
        )
        Button(
            text = "Сравнить методы", 
            font = ("Arial", 16), 
            fg = PURPLE_SUPER_DARK,
            highlightbackground = PURPLE, 
            highlightthickness = 30, 
            command = self.compareCompressionMethods
        ).place(
            width = windowWidth * 0.24 - 4, 
            height = 31, 
            x = windowWidth * 0.38 + 2, 
            y = windowHeight - 43,
        )

        Button(
            highlightbackground = PURPLE_DARK, 
            highlightthickness = 30, 
            fg = PURPLE_LIGHT, 
            state = DISABLED,
        ).place(
            width = windowWidth * 0.24, 
            height = 35, 
            x = windowWidth * 0.66, 
            y = windowHeight - 45,
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
            height = 31, 
            x = windowWidth * 0.66 + 2, 
            y = windowHeight - 43,
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
    
        inputFile = self.getInputFile()
        if inputFile is None:
            return
        
        outputDirectory = self.getOutputDirectory()
        if outputDirectory is None:
            return

        compressor = Compression(
            method=method,
            text_editor=self.textEditor,
            progressbar=self.progressbar,
        )
        compressor.compress(
            inputFile,
            outputDirectory + "/compressed.bin",
        )
        compressor.decompress(
            outputDirectory + "/compressed.bin",
            outputDirectory + "/decompressed.bmp",
        )

    def getOutputDirectory(self) -> str | None:
        path = self.outputDirectoryEntry.get()
        if not os.path.exists(path) or not os.path.isdir(path):
            messagebox.showwarning(
                "Ошибка",
                "Директории с таким именем не существует!"
            )
            return
        
        return path
    
    def getInputFile(self) -> str | None:
        path = self.inputFilenameEntry.get()
        if not os.path.exists(path) or not os.path.isfile(path):
            messagebox.showwarning(
                "Ошибка",
                "Файла с таким именем не существует!"
            )
            return
        
        return path

    def compareCompressionMethods(self) -> None:
        plot_comparison_graph(
            image_paths=IMAGE_PATHS, 
            compression_rates=COMPRESSION_RATES,
            title="Сравнение методов по степени сжатия изображений",
            y_label="Степень сжатия (%)",
            x_label="Изображения (названия)",
            y_lim=105,
        )
        plot_comparison_graph(
            image_paths=IMAGE_PATHS, 
            compression_rates=INFORMATION_TO_DECOMPRESS,
            title="Сравнение методов по размеру данных для распаковки изображений",
            y_label="Кол-во информации для распаковки\nизображения в сжатом файле (%)",
            x_label="Изображения (названия)",
            y_lim=44,
        )

    def aboutProgram(self):
        messagebox.showinfo(
            "О программе", 
            "Реализация метода сжатия статических изображений "\
            "без потерь на основе алгоритма Хаффмана\n\n"\
            "Ковалец Кирилл ИУ7-42М (2025)"
        )

    def run(self):
        self.methodVar.set(CompressionMethods.HYBRID.value)

        self.inputFilenameEntry.insert(0, "/Users/kirill/Documents/bmstu/magistracy_diploma/input_data/heart.bmp")
        self.outputDirectoryEntry.insert(0, "/Users/kirill/Documents/bmstu/magistracy_diploma/output_data")

        self.window.mainloop()
