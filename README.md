# RandomHentai
Just a script to get a random Doujin from Nhentai.

# Usage
start the exe (from Release) or the python file

Enter Tags (this is Required)

Enter Exluded tags (tags you dont wan't)

Enter Maximum Pages (if you only want the short ones and not the effing 400 pages collections)

and select the Language. (afaik there is only English, japanese and chinese.)

Click search. Wait a moment and bam you get a doujin. you can click the "show cover" checkmark to see the cover and click the title or the cover to open a browser.

yeah thats pretty much it. :V

# Requirements
Python 3.9

Pillow

PySimpleGUI

hentai (yes its literally called that https://pypi.org/project/hentai/)

PyInstaller (if you want to make a exe)

# Create Exe
install all the requirements and PyInstaller and download the script.

Pyinstaller ./RandomHentai.py --onefile --noconsole
