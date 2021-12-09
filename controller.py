import json
from tkinter import *
from functools import partial
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


BATFILENAME = "\\sort.bat"
NEWPATH = "!newpath"


def createBat(path: str, args: list) -> None:
    currentpath = pathlib.Path().resolve()
    with open(path+BATFILENAME, 'w', encoding='utf-8') as shortcut:
        shortcut.write(f'{currentpath}\\foldersort.py {path} {":".join(args)}')


def removeBat(path: str) -> None:
    if len(glob(path+BATFILENAME)):
        removeFile(path+BATFILENAME)


class Window(Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('foldersort controller')
        self.minsize(400, 200)

        self.json = loadJson('controller.json')
        self.selectedpath = None
        self.selectedignore = None

        self.selectionframe = Frame()
        self.infoframe = Frame()

        toolframe = Frame(self.selectionframe)
        save = Button(toolframe, width=30, text='save')
        load = Button(toolframe, width=30, text='load')
        add = Button(toolframe, width=30, text="add")
        remove = Button(toolframe, width=30, text="remove")

        save.grid(column=0, row=0, sticky=(W, E))
        load.grid(column=0, row=1, sticky=(W, E))
        add.grid(column=0, row=2, sticky=(W, E))
        remove.grid(column=0, row=3, sticky=(W, E))

        self.pathbox = Listbox(self.selectionframe, width=30)
        pathscroll = Scrollbar(self.selectionframe, command=self.pathbox.yview)

        self.pathbox.configure(yscrollcommand=pathscroll.set)

        self.updatePathbox()

        toolframe.grid(column=0, row=0, columnspan=2)
        self.pathbox.grid(column=0, row=1, sticky=(W, E))
        pathscroll.grid(column=1, row=1, sticky=NSEW)

        self.selectionframe.grid(column=0, row=0)
        self.infoframe.grid(column=1, row=0)

        save.configure(command=self.save)
        load.configure(command=lambda: self.load(
            self.pathbox.get(self.pathbox.curselection()[0])))
        add.configure(command=self.addPath)
        remove.configure(command=self.removePath)

    def updatePathbox(self) -> None:
        self.pathbox.delete(0, END)
        for path in self.json:
            self.pathbox.insert(END, path['path'])

    def addPath(self) -> None:
        self.pathbox.insert(END, NEWPATH)

    def removePath(self) -> None:
        index = self.pathbox.curselection()[0]
        self.pathbox.delete(index)
        removeBat(self.json.pop(index)['path'])

    def updateInfoFrame(self, path: dict) -> None:
        for i in self.infoframe.winfo_children():
            i.destroy()

        label = Label(self.infoframe, text='Path:')
        self.pathentry = Entry(self.infoframe, width=30)
        self.pathentry.insert(0, path['path'])

        ignorelabel = Label(self.infoframe, text='ignored:')
        self.ignoreentry = Entry(self.infoframe, width=10)
        addbutton = Button(self.infoframe, text='+', command=self.addIgnored)
        removebutton = Button(self.infoframe, text='-',
                              command=self.removeIgnored)

        self.ignorebox = Listbox(self.infoframe)
        ignorescroll = Scrollbar(self.infoframe, command=self.ignorebox.yview)

        self.ignorebox.configure(yscrollcommand=ignorescroll.set)

        for i in self.selectedignore:
            self.ignorebox.insert(END, i)

        label.grid(column=0, row=0)
        self.pathentry.grid(column=1, row=0, columnspan=2)

        ignorelabel.grid(column=0, row=1)
        self.ignoreentry.grid(column=0, row=2, sticky=(W, E))
        addbutton.grid(column=1, row=2, sticky=(W, E))
        removebutton.grid(column=2, row=2, sticky=(W, E))

        self.ignorebox.grid(column=0, row=3, columnspan=3, sticky=(W, E))
        ignorescroll.grid(column=4, row=3, sticky=NSEW)

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

    def load(self, path: str) -> None:
        if path == NEWPATH:
            self.selectedpath = NEWPATH
            self.selectedignore = []
            self.updateInfoFrame({'path': NEWPATH})
        else:
            for i in self.json:
                if i['path'] == path:
                    self.selectedpath = i['path']
                    self.selectedignore = i['ignore']
                    self.updateInfoFrame(i)

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

            saveJson('controller.json', self.json)
            self.updatePathbox()


root = Window()

root.mainloop()
