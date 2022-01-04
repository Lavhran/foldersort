from sys import argv
from glob import glob as getPath
from os import mkdir, rename
from os.path import isdir
from shutil import move


def foldersort(path: str, ignore: list) -> None:
    pathitems = getPath(f'{path}\\*')

    files = []
    filetypes = []

    for item in pathitems:
        if '.' in item:
            type = item.split('.')[-1]
            if type in ignore or isdir(item):
                continue
            filetypes.append(type)
            files.append(item)

    filetypes = list(set(filetypes))

    for type in filetypes:
        try:
            mkdir(f'{path}\\{type}')
        except:
            continue

    files.sort(reverse=True)

    for file in files:
        destination = "{0}\\{1}\\".format(path, file.split('.')[-1])
        file = file.split('\\')
        file = ["\\".join(file[:-1]), file[-1]]
        
        while len(getPath(destination+file[1])):
            rename("\\".join(file), file[0] + '\\_' + file[1])
            file[1] = '_' + file[1]

        move("\\".join(file), destination)


if __name__ == "__main__":
    try:
        foldersort(argv[1], argv[2].split(":"))
    except IndexError:
        foldersort(argv[1], [])
