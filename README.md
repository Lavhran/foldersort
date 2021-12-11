# Foldersort
A small program to sort files into directories named after their filetypes

## How to use
There are two different ways you can use foldersort, one is to run foldersort.py trought cmd or powershell, the other is to use controller.py. The controller does not foldersort by itself, it makes .bat files in the correct directories.

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

### Controller:
<img width="395" alt="image" src="https://user-images.githubusercontent.com/88582860/145661837-87e1212a-ca14-47c4-a58f-da3f00b09b98.png">

On the left side of the window can you see paths that have a `sort.bat`, path can be created by pressing the `+` or be removed by clicking a path then pressing the `-`. Double click a path to edit it on the right side. 

And on the right side can you see what path it is and the filetypes it ignores, you can manually change the path or use the filedialog that appears when you press `find`. Ignored filetypes can be added and removed by writing inn the field next to "ignored:" and pressing `+` or `-`, you can also select from the already added ignored files by double clicking them. Press `save` to create a `sort.bat` in the directory the path points to.

#### Tips
* If a `sort.bat` can't be found in a path a "!" will show up in front of the path (left side).
* Add "ALLOW_DEFAULTS" to ignored to disable `DEFAULT_IGNORED`
* Non valid paths will not be saved

#### Step by step on how to create and use sort.bat
1. Open `controller.pyw`
2. Click `+`
3. Doubleclick `!newpath`
4. Click `find`
5. Choose a directory
6. Write a filetype in the entry/field next to `ignored:`
7. Click `+`
8. Do step 5 and 6 a few times more if you want more ignored filetypes
9. Click `save`
10. Open the directory you wrote in the path
11. Doubleclick `sort.bat` (to use)

![.bat in correct directory](https://user-images.githubusercontent.com/88582860/145403844-7cf96865-952e-4f9f-a2c1-c75d741cb5a4.png)


## Installation
1. download the files
