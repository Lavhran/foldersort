import json
from tkinter import *
from tkinter import filedialog as tkfd
from glob import glob
from os import remove as removeFile
import pathlib


def saveJson(path: str, content: list) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=3)


def loadJson(path: str) -> list:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


JSONPATH = 'controller.json'
BATFILENAME = "\\sort.bat"
NEWPATH = "!newpath"


def createBat(path: str, args: list) -> None:
    currentpath = pathlib.Path().resolve()
    with open(path+BATFILENAME, 'w', encoding='utf-8') as shortcut:
        shortcut.write(
            f'python {currentpath}\\foldersort.py {path} {":".join(args)}')


def removeBat(path: str) -> None:
    if len(glob(path+BATFILENAME)):
        removeFile(path+BATFILENAME)


class Window(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('foldersort controller')
        self.minsize(550, 250)

        self.json = loadJson(JSONPATH)
        self.selectedpath = None
        self.selectedignore = None

        self.selectionframe = Frame()
        self.infoframe = Frame()

        toolframe = Frame(self.selectionframe)
        add = Button(toolframe, width=15, text="+")
        remove = Button(toolframe, width=15, text="-")

        add.grid(column=0, row=0, sticky=(W, E))
        remove.grid(column=1, row=0, sticky=(W, E))

        self.pathbox = Listbox(self.selectionframe, width=30, height=14)
        pathscroll = Scrollbar(self.selectionframe, command=self.pathbox.yview)

        self.pathbox.configure(yscrollcommand=pathscroll.set)
        self.pathbox.bind('<Double-Button-1>', self.load)

        self.updatePathbox()

        toolframe.grid(column=0, row=2)
        self.pathbox.grid(column=0, row=1, sticky=(W, E))
        pathscroll.grid(column=1, row=1, sticky=NSEW)

        self.selectionframe.grid(column=0, row=0)
        Label(text='\t').grid(column=1, row=0)  # divider
        self.infoframe.grid(column=2, row=0)

        add.configure(command=self.addPath)
        remove.configure(command=self.removePath)

    def updatePathbox(self) -> None:
        self.pathbox.delete(0, END)
        for path in self.json:
            if len(glob(path['path']+BATFILENAME)):
                self.pathbox.insert(END, path['path'])
            else:
                self.pathbox.insert(END, '!'+path['path'])

    def addPath(self) -> None:
        self.pathbox.insert(END, NEWPATH)

    def removePath(self) -> None:
        index = self.pathbox.curselection()[0]
        self.pathbox.delete(index)
        removeBat(self.json.pop(index)['path'])
        saveJson(JSONPATH, self.json)

    def updateInfoFrame(self, path: dict) -> None:
        for i in self.infoframe.winfo_children():
            i.destroy()

        pathframe = Frame(self.infoframe)

        pathlabel = Label(pathframe, text='Path:')
        self.pathentry = Entry(pathframe, width=32)
        self.pathentry.insert(0, path['path'])
        pathbutton = Button(pathframe, text='find', command=self.getPath)

        ignoreframe = Frame(self.infoframe)
        ignorecontrolframe = Frame(ignoreframe)

        ignorelabel = Label(ignorecontrolframe, text='ignored:')
        self.ignoreentry = Entry(ignorecontrolframe, width=10)
        addbutton = Button(ignorecontrolframe, text='+',
                           command=self.addIgnored)
        removebutton = Button(ignorecontrolframe, text='-',
                              command=self.removeIgnored)

        self.ignorebox = Listbox(ignoreframe, height=5)
        ignorescroll = Scrollbar(ignoreframe, command=self.ignorebox.yview)

        self.ignorebox.configure(yscrollcommand=ignorescroll.set)

        for i in self.selectedignore:
            self.ignorebox.insert(END, i)

        savebutton = Button(self.infoframe, text='save', command=self.save)

        pathframe.grid(column=0, row=0)

        pathlabel.grid(column=0, row=0)
        self.pathentry.grid(column=1, row=0)
        pathbutton.grid(column=2, row=0)

        ignoreframe.grid(column=0, row=1)
        ignorecontrolframe.grid(column=0, row=0)

        ignorelabel.grid(column=0, row=0)
        self.ignoreentry.grid(column=1, row=0, sticky=(W, E))
        addbutton.grid(column=1, row=1, sticky=(W, E))
        removebutton.grid(column=1, row=2, sticky=(W, E))

        self.ignorebox.grid(column=1, row=0, sticky=(W, E))
        ignorescroll.grid(column=2, row=0, sticky=NSEW)

        savebutton.grid(column=0, row=2, sticky=(W, E))

    def getPath(self) -> None:
        directory = tkfd.askdirectory()
        directory = directory.replace('/', '\\')
        if directory != "":
            self.pathentry.delete(0, END)
            self.pathentry.insert(END, directory)

    def addIgnored(self) -> None:
        self.ignorebox.insert(END, self.ignoreentry.get())
        self.selectedignore.append(self.ignoreentry.get())

    def removeIgnored(self) -> None:
        try:
            removeindex = self.ignorebox.get(
                0, END).index(self.ignoreentry.get())
            self.ignorebox.delete(removeindex)
            self.selectedignore.remove(self.ignoreentry.get())
        except ValueError:
            pass

    def load(self, buttonevent=None) -> None:
        try:
            path = self.json[self.pathbox.curselection()[0]]
            self.selectedpath = path['path']
            self.selectedignore = path['ignore']
            self.updateInfoFrame(path)
        except IndexError:
            self.selectedpath = NEWPATH
            self.selectedignore = []
            self.updateInfoFrame({'path': NEWPATH})

    def save(self):
        index = None
        for i in range(len(self.json)):
            if self.json[i]['path'] == self.selectedpath:
                index = i
        if index == None and self.selectedpath != NEWPATH:
            return
        else:
            if self.pathentry.get() == NEWPATH:
                return

            createBat(self.pathentry.get(), self.selectedignore)
            if self.pathentry.get() != self.selectedpath:
                removeBat(self.selectedpath)

            if self.selectedpath == NEWPATH:
                self.json.append({'path': None, 'ignore': None})
                index = len(self.json) - 1

            self.json[index]['path'] = self.pathentry.get()
            self.json[index]['ignore'] = self.selectedignore

            self.selectedpath = self.pathentry.get()

            saveJson(JSONPATH, self.json)
            self.updatePathbox()


root = Window()

root.mainloop()
