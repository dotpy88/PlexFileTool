# PlexFileTool

This program is NOT affiliated with Plex or it's partners.   

The is a Python program using tkinter to create the GUI.  PyInstaller was used to create the EXE inside the dist folder.  I've included the spec file used to create this EXE.  You can run this program with the EXE provided or by cloning the repository and running the python file "PlexFileTool.py".  

Keep in mind that if you wish to run this program from Python then you will need to provide your own TVDB and MVDB API credentials.  The EXE already has API credentials and is ready to use.  

The program currently has four main options:

    Movies - This is used for renaming movies
    TV Shows - This is used for renaming tv show episodes
    Find Genre - This is used for finding a specific genre inside a folder of movies
    Dig - This is used for extracting all video and subtitle files from nested folders

The renaming feature of this tool follows the Plex standard listed on their website

Shows and their subtitles will follow this format:

    show name - SXEXX - episode name
    Ex.  Game of Thrones - S01E01 - Winter Is Coming
    
Movies and their subtitles will follow format:

    movie name (movie year)
    Ex.  Christmas Vacation (1989)

This program has a UNDO button to revert any unwanted changes.  It also writes a log file of changes inside the working directory called "file_changes" and "file_errors".  

Lastly, I created this program to help organize MY library.  It's possible that it won't do everything you need.  I'm open to making changes if you have ideas.  