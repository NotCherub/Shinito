# Shinito
Shinito is made to clear the movie names downloaded from various sources. We all download movies from torrents and various sources. But downloading them from such sources have file names very weird and messy. 
So, I made **Shinito** to rename such file names.

# Requirements
If you are on Linux/Ubuntu only terminal and type `pip3 install imdbpie` and open the terminal in the folder where you have saved all the movies and type `python3 Shinito.py`.
If you are on Windows make sure your python is added to PATH variable. If not, try [this link](https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command).

Then move the command prompt in the movies folder and type `python Shinito.py`.

Only extra dependency required is [`imdbpie`](https://pypi.org/project/imdbpie/)

# How it Works
It first crwals into each subfolder and detect every video file. Then it finds the movie name from IMDb database and renames the files accordingly. Before renaming it will ask you. 
### If any file is wrongly detected,Please Email me `Data.txt` file.
