import tkinter as tk
from tkinter import filedialog
import MvdbApiClass
import os
import re

if __name__=='__main__':
    import FindClientClass
    help(FindClientClass)

class FindClient():
    root = ""
    mvdbapi = MvdbApiClass.MvdbApi()
    loaded = False

    def __init__(self,root,debug=False):
        self.root = root
        if debug:
            print("DBG> root = %s" % self.root)

    def Close(self):
        self.mvdbapi.Close()
        return True

    def exitprogram(self):
        self.root.destroy()

    def filebrowser(self):
        self.resetmenus()
        self.directory.configure(state=tk.NORMAL)
        self.directory.delete(0, tk.END)
        fb = filedialog.askdirectory(parent=self.root)
        self.directory.insert(0, fb)
        self.directory.configure(state=tk.DISABLED)
        self.lookup_butt.configure(state=tk.NORMAL)

    def popupmessage(self):
        toplevel = tk.Toplevel()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        w = 600
        h = 200
        toplevel.geometry("%dx%d+%d+%d" % (w, h, x + 100, y + 300))
        label1 = tk.Label(toplevel, text="This is a test")
        label1.grid(row=10,column=1)

    def revertfiles(self):
        newdir = os.path.join(self.curr_dir, self.genre_folder)
        for file in self.files_to_change:
            oldfile = os.path.join(self.curr_dir, file)
            newfile = os.path.join(newdir, file)
            if os.path.exists(oldfile):
                continue
            os.rename(newfile,oldfile)
        msg = "Files have been moved back"
        self.msg_label3['text'] = msg
        self.msg_label3['fg'] = "red"
        self.revert_butt.configure(state=tk.DISABLED)
        self.rename_butt.configure(state=tk.NORMAL)

    def renamefiles(self):
        newdir = os.path.join(self.curr_dir, self.genre_folder)
        if not os.path.exists(newdir):
            os.mkdir(newdir)
        for file in self.files_to_change:
            oldfile = os.path.join(self.curr_dir, file)
            newfile = os.path.join(newdir, file)
            if os.path.exists(newfile):
                continue
            os.rename(oldfile,newfile)
        msg = "Files have been moved"
        self.msg_label3['text'] = msg
        self.msg_label3['fg'] = "green"
        self.rename_butt.configure(state=tk.DISABLED)
        self.revert_butt.configure(state=tk.NORMAL)

    def resetmenus(self):
        self.msg_label['text'] = ""
        self.msg_label2['text'] = ""
        self.msg_label3['text'] = ""
        self.msg_label4['text'] = ""
        self.listbox.configure(state=tk.NORMAL)
        self.listbox2.configure(state=tk.NORMAL)
        self.listbox3.configure(state=tk.NORMAL)
        self.listbox.delete(0, tk.END)
        self.listbox2.delete(0, tk.END)
        self.listbox3.delete(0, tk.END)
        self.genre_popup.configure(state=tk.NORMAL)
        self.select_butt.configure(state=tk.DISABLED)
        self.discover_butt.configure(state=tk.DISABLED)
        self.rename_butt.configure(state=tk.DISABLED)
        self.revert_butt.configure(state=tk.DISABLED)

    def getselection(self,event):
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return
        self.show_selection = widget.get(selection[0])
        self.select_butt.configure(state=tk.NORMAL)


    def getfiles(self):
        self.curr_dir = self.directory.get()
        self.dir_files = []
        try:
            dirfiles = os.listdir(self.curr_dir)
        except Exception as e:
            print(e)
            dirfiles = None
            msg = "Error Retrieving Files"
            self.msg_label['text'] = msg
            self.msg_label['fg'] = "red"

        if dirfiles:
            file_count = 0
            for file in dirfiles:
                path_check = os.path.join(self.curr_dir, file)
                if os.path.isdir(path_check):
                    continue
                file_count += 1
                self.dir_files.append(file)
                self.listbox.insert(tk.END, file)
            msg = "Files found in that directory: %s" % (file_count)
            self.msg_label['text'] = msg
            self.msg_label['fg'] = "green"
            self.listbox.configure(state=tk.DISABLED)
            self.discover_butt.configure(state=tk.NORMAL)

    def getmovies(self):
        self.listbox2.delete(0, tk.END)
        self.lookup_butt.configure(state=tk.DISABLED)
        match_str = self.regex.get()
        self.msg_label2['fg'] = "blue"
        self.msg_label2['text'] = "Checking TheMovieDB.org for matches.."
        self.msg_label2.update()
        skip = False
        self.files_to_change = []
        for file in self.dir_files:
            self.listbox2.update()
            movie_year = re.search(r'%s' % match_str, file,flags=re.IGNORECASE)
            if movie_year:
                movie_year = movie_year.groups()
            if not movie_year:
                skip = True
                msg = "No Regex Matches >> %s" % file
                self.listbox2.insert(tk.END, msg)
                continue
            movie = movie_year[0]
            movie = re.sub(r'\W+',' ', movie)
            movie = movie.rstrip()
            year = movie_year[1]
            results = self.mvdbapi.SearchMovies(movie,year=int(year))
            if not results['results']:
                results = self.mvdbapi.SearchMovies(movie)
                if not results['results']:
                    skip = True
                    msg = "No Movie Matches >> %s" % file
                    self.listbox2.insert(tk.END, msg)
                    continue
            movie_title = results['results'][0]['title']
            movie_year = results['results'][0]['release_date'][:4]
            movie_genres = results['results'][0]['genre_ids']
            curr_genre = self.genres[self.popupvar.get()]
            self.genre_folder = self.popupvar.get()
            if curr_genre not in movie_genres:
                skip = True
                msg = "Genre doesnt match >> %s" % file
                self.listbox2.insert(tk.END, msg)
                continue
            msg = "Match Found >> %s (%s)" % (movie_title,movie_year)
            self.listbox2.insert(tk.END, msg)
            self.files_to_change.append(file)

        if skip:
          self.msg_label4['fg'] = "red"
          self.msg_label4['text'] = "Not all files matched genre, those files are being skipped"

        self.listbox2.configure(state=tk.DISABLED)
        if self.files_to_change:
            self.discover_butt.configure(state=tk.DISABLED)
            self.select_butt.configure(state=tk.NORMAL)
            self.genre_popup.configure(state=tk.DISABLED)

    def changefiles(self):
        self.msg_label4['fg'] = "green"
        self.msg_label4['text'] = "Generating new file locations.."
        self.msg_label4.update()
        self.rename_butt.configure(state=tk.DISABLED)
        if self.files_to_change:
            for file in self.files_to_change:
                newline = "New Location:  %s/%s" % (self.genre_folder,file)
                blankline = ""
                self.listbox3.insert(tk.END, newline)
                self.listbox3.insert(tk.END, blankline)
            self.rename_butt.configure(state=tk.NORMAL)
            self.select_butt.configure(state=tk.DISABLED)
            self.listbox3.configure(state=tk.DISABLED)
        if not self.files_to_change:
            self.msg_label4['fg'] = "red"
            self.msg_label4['text'] = "No files to process!"

    def loadfindclient(self):
        #gui elements
        self.dir_label = tk.Label(self.root,text="Directory")
        self.directory = tk.Entry(self.root,width=100)
        self.lookup_butt = tk.Button(self.root,text='GetFiles', command=self.getfiles)
        self.browse_butt = tk.Button(self.root,text='Browse', command=self.filebrowser)
        self.file_label = tk.Label(self.root,text="Files")
        self.listbox = tk.Listbox(self.root, width=100, height=15)
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.msg_label = tk.Label(self.root)
        self.blank_label = tk.Label(self.root, text="-" * 120, fg="purple")
        self.regex_label = tk.Label(self.root, text="File Regex")
        self.regex_label2 = tk.Label(self.root, text="Enter regex to determine movie title and year.  Must be two regex groups.  Ex:  ^(.+?)(\d\d\d\d)", fg="green")
        self.msg_label2 = tk.Label(self.root,fg="blue")
        self.genre_label = tk.Label(self.root, text="Choose Genre")
        self.popupvar = tk.StringVar(self.root)
        self.genres = self.mvdbapi.GetGenres()
        self.popupvar.set('Action')
        self.genre_popup = tk.OptionMenu(self.root, self.popupvar, *self.genres.keys())
        self.genre_popup.config(width=50)
        self.blank_label2 = tk.Label(self.root, text="-" * 120, fg="purple")
        self.discover_butt = tk.Button(self.root, text='Discover', command=self.getmovies, state=tk.DISABLED)
        self.mvdb_label = tk.Label(self.root,text="Movies")
        self.listbox2 = tk.Listbox(self.root, width=100, height=5)
        self.scrollbar2 = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.listbox2.config(yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.listbox2.yview)
        self.select_butt = tk.Button(self.root, text='Generate', command=self.changefiles, state=tk.DISABLED)
        self.blank_label3 = tk.Label(self.root, text="-" * 120, fg="purple")
        self.msg_label4 = tk.Label(self.root,fg="red")
        self.listbox3 = tk.Listbox(self.root, width=100, height=10)
        self.scrollbar3 = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.listbox3.config(yscrollcommand=self.scrollbar3.set)
        self.scrollbar3.config(command=self.listbox3.yview)
        self.rename_butt = tk.Button(self.root, text='Make Changes', command=self.renamefiles, state=tk.DISABLED)
        self.msg_label3 = tk.Label(self.root,fg="green")
        self.revert_butt = tk.Button(self.root, text='Undo Changes', command=self.revertfiles, state=tk.DISABLED)
        self.startover_butt = tk.Button(self.root, text='Start Over', command=self.resetmenus)
        #

        # Entry items
        self.regex = tk.Entry(self.root, width=100)
        self.regex.insert(0, "^(.+?)(\d\d\d\d)")
        #

        # Grid locations
        self.dir_label.grid(row=0, sticky=tk.E)
        self.directory.grid(row=0,column=1)
        self.browse_butt.grid(row=0,column=2)
        self.lookup_butt.grid(row=0,column=3)
        self.file_label.grid(row=2,column=0, sticky=tk.E)
        self.listbox.grid(row=2, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.scrollbar.grid(row=2, column=2, sticky=tk.N + tk.S + tk.W)
        self.blank_label.grid(row=3, column=1)
        self.msg_label.grid(row=1, column=1)
        self.regex_label.grid(row=6, sticky=tk.E)
        self.regex.grid(row=6, column=1)
        self.regex_label2.grid(row=7,column=1,sticky=tk.W)
        self.discover_butt.grid(row=8, column=2)
        self.genre_label.grid(row=8,column=0)
        self.genre_popup.grid(row=8,column=1,sticky=tk.W)
        self.blank_label2.grid(row=9, column=1)
        self.msg_label2.grid(row=10, column=1)
        self.mvdb_label.grid(row=11,column=0, sticky=tk.E)
        self.listbox2.grid(row=11, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.scrollbar2.grid(row=11, column=2, sticky=tk.N + tk.S + tk.W)
        self.select_butt.grid(row=12, column=2,sticky=tk.W)
        self.msg_label4.grid(row=12,column=1)
        self.blank_label3.grid(row=13, column=1)
        self.listbox3.grid(row=14, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.scrollbar3.grid(row=14, column=2, sticky=tk.N + tk.S + tk.W)
        self.rename_butt.grid(row=15, column=1)
        self.msg_label3.grid(row=18, column=1)
        self.revert_butt.grid(row=16, column=1)
        self.startover_butt.grid(row=17,column=1)
        #
        self.loaded = True

    def destroyelements(self):
        self.dir_label.destroy()
        self.directory.destroy()
        self.browse_butt.destroy()
        self.lookup_butt.destroy()
        self.file_label.destroy()
        self.listbox.destroy()
        self.scrollbar.destroy()
        self.blank_label.destroy()
        self.msg_label.destroy()
        self.regex_label.destroy()
        self.regex.destroy()
        self.regex_label2.destroy()
        self.discover_butt.destroy()
        self.genre_label.destroy()
        self.genre_popup.destroy()
        self.blank_label2.destroy()
        self.msg_label2.destroy()
        self.mvdb_label.destroy()
        self.listbox2.destroy()
        self.scrollbar2.destroy()
        self.select_butt.destroy()
        self.msg_label4.destroy()
        self.blank_label3.destroy()
        self.listbox3.destroy()
        self.scrollbar3.destroy()
        self.rename_butt.destroy()
        self.msg_label3.destroy()
        self.revert_butt.destroy()
        self.startover_butt.destroy()
        #
        self.loaded = False

