import tkinter as tk
import TvClientClass
import MovieClientClass
import FindClientClass
import DigClientClass
import sys


def destroycurrent(current_option):
    if current_option == 'TvShows':
        tvclient.destroyelements()
    if current_option == 'Find':
        findclient.destroyelements()
    if current_option == 'Dig':
        digclient.destroyelements()
    if current_option == 'Movies':
        movieclient.destroyelements()

def movies():
    global current_option
    canvas.pack_forget()
    if current_option:
        destroycurrent(current_option)
    current_option = 'Movies'
    movieclient.loadmovieclient()

def tvshows():
    global current_option
    canvas.pack_forget()
    if current_option:
        destroycurrent(current_option)
    current_option = 'TvShows'
    tvclient.loadtvshowclient()

def findgenre():
    global current_option
    canvas.pack_forget()
    if current_option:
        destroycurrent(current_option)
    current_option = 'Find'
    findclient.loadfindclient()

def dig():
    global current_option
    canvas.pack_forget()
    if current_option:
        destroycurrent(current_option)
    current_option = 'Dig'
    digclient.loaddigclient()

root = tk.Tk()
root.title("Plex File Tool")
root.geometry("800x900")

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = '.'

mvdb_logo = tk.PhotoImage(file="%s/images/themoviedblogo.png" % base_path)
tvdb_logo = tk.PhotoImage(file="%s/images/thetvdblogo.png" % base_path)
canvas = tk.Canvas(root, width=800,height=800)
canvas.pack()
canvas.create_text(20,60, anchor=tk.NW, text="-" * 60, fill="Blue")
canvas.create_text(20,80, anchor=tk.NW, text="Choose an option above to get started", fill="Blue")
canvas.create_text(20,100, anchor=tk.NW, text="-" * 60, fill="Blue")
canvas.create_image(20,200, anchor=tk.NW, image=mvdb_logo)
canvas.create_image(20,525, anchor=tk.NW, image=tvdb_logo)
canvas.create_text(20,170, anchor=tk.NW, text="All movie data is provided by TheMovieDB.org", fill="Green")
canvas.create_text(20,500, anchor=tk.NW, text="All tv show data is provided by TheTVDB.com", fill="Green")
menu = tk.Menu(root)
root.config(menu=menu)
file = tk.Menu(menu)
movieclient = MovieClientClass.MovieClient(root)
tvclient = TvClientClass.TvClient(root)
findclient = FindClientClass.FindClient(root)
digclient = DigClientClass.DigClient(root)
file.add_command(label="Movies", command=movies)
file.add_command(label="TV Shows", command=tvshows)
file.add_command(label="Find Genre", command=findgenre)
file.add_command(label="Dig", command=dig)
menu.add_cascade(label="Options", menu=file)
current_option = ""
root.mainloop()
