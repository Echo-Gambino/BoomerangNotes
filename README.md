# BoomerangNotes
Hing Yue (Henry) Lam

` ----- Boomerang ---- < `

Reminders that pops up from your screen at a set time. Perfect for reminding yourself of important information!

Purpose:
 1. A first attempt to make something that I would use on a day to day basis
 2. A test and exercise for programming in python3
 3. A pilot project to begin something from scratch and have it reach a logical conclusion (since most of my personal projects have no set 'end')

Deliverables:
 * Let the user input title, description, and time.
 * Pops up a text editor (mousepad for linux) to input the description.
 * Pops up a webbrowser to notify you of your set reminder.
 * Able to run in the background (after you are done setting up the reminder of course).
 * Able to import and parse a .txt file as a means to set up a reminder.
 * Display a small transaction 'receipt' of what the user had just inputted for their reminder (via command-line or importing

Compatibility:
 * Importing .txt files can be done on ALL operating systems (Windows, MacOS, Linux) that runs Python3
 * Command-line interface can only be used in Linux (because it uses a texteditor called 'mousepad', will add support for 'notepad' for Windows compatibility)

Requirements:
1. mousepad (a text editor for linux)
2. Python3
3. PIP
4. Python3 libraries within `requirements.txt`, execute `pip install -r requirements.txt` for easy setup

Usage:
1. Executing `python3 boomerang.py` will guide the user through the text interface to enter these fields
	* Title (input this directly into the terminal or command prompt window)
	* Description (will pop up the program called 'mousepad' for easy copy and pasting along with on the fly formatting)
	* Datetime (input this directly into the terminal or command prompt window)
2. Executing `python3 boomerang.py -I <filename>.txt` will automatically set up the reminder based on the contents of the text file
	* `#` (hashtags) on the first character of a new line will automatically be omitted from the description (essentally commenting out lines)
	* `#title: <title_name>` will set the reminder's title to the value of `<title_name>`
	* `#time: YYYY-MM-DD hh:mm:ss` will set the reminder's time to the value of YYYY-MM-DD hh:mm:ss

Acknowledgements:
 * Application structure (mainly the app folder and importing 'app' in boomerang) from Miguel Grinberg's [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

