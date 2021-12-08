import json
from tkinter import *
from functools import partial


def saveJson(path: str, content: list) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=3)


def loadJson(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
        new = Button(toolframe, width=30, text="new")

        save.grid(column=0, row=0, sticky=(W, E))
        load.grid(column=0, row=1, sticky=(W, E))
        new.grid(column=0, row=2, sticky=(W, E))

        pathbox = Listbox(self.selectionframe, width=30)
        pathscroll = Scrollbar(self.selectionframe, command=pathbox.yview)

        pathbox.configure(yscrollcommand=pathscroll.set)

        for path in self.json:
            pathbox.insert(END, path['path'])

        toolframe.grid(column=0, row=0, columnspan=2)
        pathbox.grid(column=0, row=1, sticky=(W, E))
        pathscroll.grid(column=1, row=1, sticky=NSEW)

        self.selectionframe.grid(column=0, row=0)
        self.infoframe.grid(column=1, row=0)

        save.configure(command=self.save)
        load.configure(command=lambda: self.load(
            pathbox.get(pathbox.curselection()[0])))

    def load(self, path: str) -> None:
        for i in self.json:
            if i['path'] == path:
                self.selectedpath = i['path']
                self.selectedignore = i['ignore']
                self.updateInfoFrame(i)

    def updateInfoFrame(self, path: dict) -> None:
        for i in self.infoframe.winfo_children():
            i.destroy()

        label = Label(self.infoframe, text='Path:')
        self.pathentry = Entry(self.infoframe, width=30)
        self.pathentry.insert(0, path['path'])

        ignorelabel = Label(self.infoframe, text='ignored:')
        self.ignoreentry = Entry(self.infoframe, width=10)
        addbutton = Button(self.infoframe, text='+', command=self.addIgnored)
        removebutton = Button(self.infoframe, text='-')

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
        try:
            self.ignorebox.insert(END, self.ignoreentry.get())
            self.selectedignore.append(self.ignoreentry.get())
        except:
            pass

    def save(self):
        index = None
        for i in range(len(self.json)):
            if self.json[i]['path'] == self.selectedpath:
                index = i
        if not index:
            return
        else:
            self.json[index]['path'] = self.pathentry.get()
            self.json[index]['ignore'] = self.selectedignore

        saveJson('controller.json', self.json)


root = Window()

root.mainloop()
