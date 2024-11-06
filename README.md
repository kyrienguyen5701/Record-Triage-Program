# Record Triage Program

Below are the details for V1.0 and V2.0 of the Record Triage Program. Most of the design decisions remain the same so the first section is still highly relevant, but V2.0 has a different structure and introduces new functionality which is explained here.


Brief setup and operation instructions can be found [here](https://docs.google.com/document/d/1WY9ovJvOJYdkLxjbK4AQgESZnYK_E-sft7o4BKskDjg/edit?usp=sharing)

<details>
<summary><b><u><font size="+5">V1.0 05/22 - 05/23</font></u></b></summary>

<br>

June 7, 2022
Lilah Kelly

This work is originally by one coder, and has been briefly modified by a second (me). This second coder modified some
aspects of the code but mainly worked on making the code more legible and easy for the next coder to know what's
happening.

I have included notes throughout of things to look at and that need improving still (I ran out of time). I also have
two file types for each class; one as a CLASS file which is the unmodified original code without comments. The JAVA
versions of these classes are the modified and commented ones. The CLASS files are there to be looked at and
compare with the JAVA files for debugging ONLY.

***Please remove these CLASS files when running the program as they have issues that have since been fixed.***
These CLASS files are:
APIutilities.class
ReadWriteToExcel.class
Triage.class
WriteOutputToExistingExcelFile.class
WriteOutputToNewExcelFile.class

DO NOT remove Bib.class or any other classes not explicitly listed above. These are used as libraries and need no modifications.

March 23, 2023
Son (Kyrie) Nguyen  
According to the previous developer,

> DO NOT remove Bib.class or any other classes not explicitly listed above. These are used as libraries and need no modifications.

This means that the program REQUIRES external libraries in order to run correctly. As software applications are usually built upon previous ones, external libraries serve as the foundation work so that software developers don't have to develop everything from scratch. These libraries were missing in the second iteration for some unidentified reasons. Based on the work of the first iteration, I copy those libraries from the first iteration and put them in the second iteration, under `jar` and `exlibrisgroup` folders.

For the CLASS files that the previous developer used for debugging only, I have re-compiled them using that developer's JAVA files. Therefore, DO NOT remove these CLASS files as they are necessary. They are NOT the same with those in the first iteration and will have different behaviour.

I also bring back and slightly modify the `.cmd` files to run natively on Windows without using any specific software and to get the correct path to run the API. In line 4 of each file,

```cmd
cd "%~dp0"\java --> cd "%~dp0"\src
```

March 28, 2023
Son (Kyrie) Nguyen  
Finish the first version for Python program.  
If your computer does not have Python, you need to run `install.cmd` and follow the Python Installer to install Python. Once Python is installed, you can run `setup.cmd` to install extra packages and folders for the program.

There is still one last thing - this program requires an API key from Ex Libris for data fetching. Please contact [Joanna DiPasquale](https://www.union.edu/schaffer-library/faculty-staff/joanna-dipasquale) for further information. Once you get the API key, you can change the value in `sample.env` and rename the file to `.env`

A big improvement of the main program `main.cmd` is that the user can name the output file. If no extension is detected in that name, the file extension is set to `.xlsx`. If no input is detected, the default output file will be in the same folder as the input file, with the suffix `_triaged`.

Note that there **MUST BE NO SPACE** in both the input file path and output file path, as they can cause reading problems for the program (blame Windows on this). If you put your input files in a folder with SPACE in its name, please kindly move them to another folder.

There is also a Python script for debugging, where user can open the command line and run as follows:

```cmd
py debug.py -ids mms_id1 mms_id2 ...
```

Eg: `py debug.py -ids 991004787783604651`

The purpose of the debugging program is for quickly testing a short list MMS IDs, with **colorized** messages.

There is also the interactive mode that allows user to enter one MMS ID at a time. To run this mode, simpy run `py debug.py -i` or double click on `debug_interactive.cmd`.

For more options on using `debug.py`, user can run `py debug.py -h` to get a more detailed description.

Note that `debug.py` is a WIP so please let me know about your feedback.

April 17, 2023
Son (Kyrie) Nguyen  
Debug or logging files are now under `./logs`.

April 25, 2023
Son (Kyrie) Nguyen  
Add script `scripts\update.cmd` to download newest code from Github. This is still **WIP** so unless you know what you are doing, **DON'T** run this until a developer tells you to.

Re-structuralize the whole project to better separate contents:

- Scripts to modify/update the project is in `scripts` (unless you are a developer, you don't really touch this folder)
- The main applications are now under `app` to separate end-users from Python modules.
- Triaged outputs are now in `app\outputs`.
- Logging outputs are now in `app\logs`.

June 2, 2023
Son (Kyrie) Nguyen  
Update `scripts\update.cmd` to create backups. It is less scarier to run this now I guess.

Project structure:

```bash
📦app
 ┣ 📂logs
 ┣ 📂outputs
 ┣ 📂src
 ┃ ┣ 📜.env
 ┃ ┣ 📜bib.py
 ┃ ┣ 📜config.py
 ┃ ┣ 📜debug.py
 ┃ ┣ 📜logger.py
 ┃ ┣ 📜main.py
 ┃ ┣ 📜rule.py
 ┃ ┣ 📜test.py
 ┃ ┗ 📜triage.py
 ┣ 📜debug_interactive.cmd
 ┗ 📜main.cmd <-- The main program 

📦scripts
 ┣ 📜install.cmd
 ┣ 📜setup.cmd
 ┗ 📜update.cmd

📜requirements.txt
```

</details>

<details>
<summary><b><u><font size="+5">V2.0 10/24 - Present</font></u></b></summary>

<br>

Oct 4, 2024 
James Gaskell

Added an evaluation for the OCLC number which is now output to the Triage spreadsheet

Added an evaluation of the 008 field to ensure it matches the main record which should help shorten final review. The 008 field does not have indicators or subfield codes, instead it is an *UP TO* 40 character string where the position of each character indicates the element it belongs to. This element of the program will require maintenance should Alma decide to change the order or elements in the 008. A current explanation of the characters' significance can be found [here](https://www.loc.gov/marc/bibliographic/bd008a.html)

Added an operating system evaluation that changes the filepath to be in the correct format for windows and MacOS (windows uses // Mac uses \ to separate directories). The project can now be run on Mac. Caveat - the project can only be run on Mac through main.py not main.cmd (meaning the config file must be changed) since this is written for windows. A future developer may add a Mac batch file to run the program from terminal

Oct 15, 2024 
James Gaskell

Added a comparison of data fields and the 008 field for Illustrations, Bibliogaphies, Indexes and Publication Locations. Added any issues found with the records to the output file under new headers.

Updated the order of the output file and added expand_columns.py to change the column widths of the spreadsheet upon output, thus saving the user time for every Triage spreadsheet produced.

Added an inputs folder to the project to make it clearer and easier when testing using the default configuration.

Oct 18, 2024 
James Gaskell

Cleaned up the Triage spreadsheet by removing any columns that were not necessary for evaluation

Changed main.cmd to output the triage spreadsheet into the outputs folder contained within the project

Note: to test the project using default files, the coder should manually create an inputs folder which will be ignored by github. default configuration assumes input files are within this folder but it is not needed for the program to run

Oct 25, 2024 
James Gaskell

Added functionality to the setup.cmd file to input and write out the API key to the required environment file. Also deletes the sample.env file to make clean up the src folder without the user having to go into it.

Added automatic shortcut creation to the setup file. The shortcut has a descriptive icon and will make it easier for most users to access main without traversing the project folders

Added a Triage Outputs folder to the desktop that holds all the triaged documents. This folder is automatically generated when running the Setup.cmd file and is created again if it is accidentally deleted outside of the program.

Nov 1, 2024 
James Gaskell

Now allows the user to choose where the output file and program icon are created. This should be desktop in most cases but allows for funkier file structures and personal preference. A text file is now created in assets to store the location of outputs and the shortcut.

Added assets folder to the file structure shown below to store the icon and shortcut directory information.

<br>

Project structure:

```bash
📦app
 ┣ 📂inputs (only to debug)
 ┣ 📂logs
 ┣ 📂outputs
 ┣ 📂src
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📜icon.ico
 ┃ ┃ ┣ 📜homeDir.txt
 ┃ ┣ 📜.env
 ┃ ┣ 📜bib.py
 ┃ ┣ 📜config.py
 ┃ ┣ 📜debug.py
 ┃ ┣ 📜expand_columns.py
 ┃ ┣ 📜logger.py
 ┃ ┣ 📜main.py
 ┃ ┣ 📜rule.py
 ┃ ┣ 📜test.py
 ┃ ┗ 📜triage.py
 ┣ 📜debug_interactive.cmd
 ┗ 📜main.cmd <-- The main program 

📦scripts
 ┣ 📂src
 ┃ ┣ 📜.select_dir.py
 ┣ 📜install.cmd
 ┣ 📜setup.cmd
 ┗ 📜update.cmd

📜requirements.txt
```
</details>
