# foldersort
A small program to sort files into directories named after their filetypes

## how to use
There are two different ways you can use foldersort, one is to run foldersort.py trought cmd or powershell, the other is to use controller.py. The controller does not foldersort by it self, it makes .bat files in the correct

### cmd/powershell examples:

```
foldersort.py {path} {filetypes seperated with :}(optional)
```

__cmd:__
```
foldersort.py C:\Users\lavhr\Downloads exe:lnk:url
```

__powershell:__
```
python foldersort.py C:\Users\lavhr\Downloads exe:lnk:url
```

### controller example:
![controller](https://user-images.githubusercontent.com/88582860/145403732-12fd6194-2040-44d2-aa4a-3c655a5e26dc.png)

#### left side:
|button|function|
|------|--------|
|save|creates/updates/removes sort.bat|
|load|loads the selected path into the editor|
|add|creates a new path|
|remove|removes selected path|

#### right side:
|button|function|
|------|--------|
|+|adds filtype to ignored|
|-|removes seleted from ignored|

![.bat in correct directory](https://user-images.githubusercontent.com/88582860/145403844-7cf96865-952e-4f9f-a2c1-c75d741cb5a4.png)
#### step by step on how to create and use sort.bat
1. open `controller.py`
2. click `add`
3. doubleclick or click and press load on `!newpath`
4. write in a path next to `path:`
5. write a filetype in the entry/field under `ignored:`
6. click `+`
7. do step 5 and 6 a few times more if you want more ignored filetypes
8. click `save`
9. open the directory you wrote in the path
10. doubleclick `sort.bat`

## installation
1. download the files
