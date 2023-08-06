<p align="center">
  <a href="https://github.com/PycraftDeveloper" target="_blank" rel="noreferrer"><img src="https://user-images.githubusercontent.com/81379254/154152710-694ce1f7-44e0-47fd-bbca-988093628e70.svg" alt="my banner"></a>
</p>

Pycraft is an OpenGL, open world, video game made entirely with Python. This project is a game to shed some light on OpenGL programming in Python as it is a seldom touched area of Python's vast amount of uses. Feel free to give this project a run, and message us if you have any feedback! <br />
Made with Python 3 64-bit and Microsoft Visual Studio Code.

_Please note; all previous versions of Pycraft, with the exception of the most recent, have been moved to the releases section; Please consult the releases section of this README for more information_

[![](https://img.shields.io/badge/python-3.10-blue.svg)](www.python.org/downloads/release/python-3100) [![](https://img.shields.io/badge/python-3.9-blue.svg)](www.python.org/downloads/release/python-390) [![](https://img.shields.io/badge/python-3.8-blue.svg)](www.python.org/downloads/release/python-380) [![](https://img.shields.io/badge/python-3.7-blue.svg)](www.python.org/downloads/release/python-370) <br />
![](https://img.shields.io/github/license/PycraftDeveloper/Pycraft) ![](https://img.shields.io/github/stars/PycraftDeveloper/Pycraft) ![](https://img.shields.io/github/forks/PycraftDeveloper/Pycraft) ![](https://img.shields.io/github/issues/PycraftDeveloper/Pycraft) ![GitHub all releases](https://img.shields.io/github/downloads/PycraftDeveloper/Pycraft/total) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/PycraftDeveloper/Pycraft) ![](https://img.shields.io/pypi/wheel/python-pycraft) ![GitHub repo size](https://img.shields.io/github/repo-size/PycraftDeveloper/Pycraft) ![Discord](https://img.shields.io/discord/929750166255321138)

## Contents
This is a guide of where some of the sections of this README have gone, as well as useful links to other documents.

> * [About](https://github.com/PycraftDeveloper/Pycraft#about)
> * [Preview Video](https://youtu.be/shAprkrcaiI)
> * [Setup](https://github.com/PycraftDeveloper/Pycraft#setup)
> * * [Installing the project from GitHub (Method 1)](https://github.com/PycraftDeveloper/Pycraft#installing-the-project-from-github-method-1)
> * * [Installing the project from GitHub (Method 2)](https://github.com/PycraftDeveloper/Pycraft#installing-the-project-from-github-method-2)
> * * [Installing from PyPi (preferred)](https://github.com/PycraftDeveloper/Pycraft#installing-from-pypi-preferred)
> * * [Installing using Pipenv](https://github.com/PycraftDeveloper/Pycraft#installing-using-pipenv)
> * [Running The Program](https://github.com/PycraftDeveloper/Pycraft#running-the-program)
> * [Credits](https://github.com/PycraftDeveloper/Pycraft#credits)
> * [Uncompiled Pycraft Dependancies](https://github.com/PycraftDeveloper/Pycraft#uncompiled-pycraft-dependencies-)
> * [Changes](https://github.com/PycraftDeveloper/Pycraft#changes)
> * [Our Update Policy](https://github.com/PycraftDeveloper/Pycraft#our-update-policy)
> * [Version Naming](https://github.com/PycraftDeveloper/Pycraft#version-naming)
> * [Releases](https://github.com/PycraftDeveloper/Pycraft#releases)
> * [Other Sources](https://github.com/PycraftDeveloper/Pycraft#other-sources)
> * [Final Notices](https://github.com/PycraftDeveloper/Pycraft#final-notices)

> * [Update Timeline](https://github.com/PycraftDeveloper/Pycraft/blob/Pycraft-v0.9.4/Update_Timeline.md#update-timeline)
> * [The Planned Storyline](https://github.com/PycraftDeveloper/Pycraft/blob/Pycraft-v0.9.4/Planned_Storyline.md#the-planned-storyline)
> * [Sound Preview](https://github.com/PycraftDeveloper/Pycraft/blob/Pycraft-v0.9.4/Sound_Preview.md#pycrafts-sound-files---preview-1)

> * [The Documentation for Pycraft (Read-The-Docs)](https://python-pycraft.readthedocs.io/en/latest/)
> * [The Documentation for Pycraft (GitHub Wikis)](https://github.com/PycraftDeveloper/Pycraft/wiki)
> * [The project's PyPi page](https://pypi.org/project/Python-Pycraft/)

> * [Contact me on Twitter](https://twitter.com/PycraftDev)
> * [Contact me on Dev](https://dev.to/pycraftdev)
> * [Pycraft's Discord Server Invite](https://discord.gg/83EBntQqpf)

## About
Pycraft is a 3D open-source, open-world video game made in Python. For a long time attempts to make large 3D games in python has been ignored, I believe there are two reasons: one; People use Python primarily for data handling and processing and not graphics and, two; there is little to no documentation out there to do anything more than make a 3D rotating cube in Python. Making a 3D game in Python for me hasn’t been an easy experience, far from it but I have decided to share my project, complete with tutorials, explanations, articles and code explanations in the hope that 3D game development in Python can be seen as a more easily attainable target, and to fill that gap in documentation. Pycraft then is a trial project, as I learn and experiment on what goes best where and how thing go together, this is why development can sometimes appear to have stopped, because I’m learning and testing what I've learned, so hopefully for people in the future it will be an easier experience. Also, don’t forget there is more to game development than just graphics, there is AI, sound, physics and all the other GUIs that go with it, and as I learn the quality of the overall program will improve. Pycraft is not going to be the final name of the game, however until something better becomes available, we shall stick to it.

## Setup
### Installing the project from GitHub (Method 1)
The project will download as a (.zip) compressed file. Please make sure you have the project decompressed before use. Next make sure that any folders and files outside of the 'Pycraft' folder are removed and that the 'Pycraft' file is in the intended place for the file to be run from. This file can be freely moved around, transported between drives, computers and folders in this form. A video guide to this will be uploaded here and in YouTube in the coming months.

When running the program please make sure you have a minimum of 1GB of free space on the drive and also have Python 3 installed on your device. This can be found here: (www.python.org/downloads). The sub version of Python isn't too important in this circumstance however the project has been tested in Python 3.9.5 and is known to work. In addition to all this please make sure you have the following modules installed on your device:
Pygame, Numpy, PyOpenGL, Pillow, PyAutoGUI, Psutil, PyWaveFront, CPUinfo and Ctypes. 
For those not familiar they can be found here: (pypi.org) and you can use the following syntax to install, update and remove these modules:

``pip install <module>``
``pip uninstall <module>``

Here is a short video tutorial walk you through all this: (https://youtu.be/DG5YbE-umw0)

### Installing the project from GitHub (Method 2)
If you are installing the project from the GitHub releases page, then this will be relevant for you.
After you have selected your preferred file type (it'll be either a compiled (.exe) file or a (.zip) file, those that download the (.zip) file will find the information above more relevant.

If you, however, download the (.exe) type file, then this will be more relevant for you. If you locate the file in your file explorer and double click it, then this will run the project. You do not need Python, or any of the projects required modules, as they come built-in with this method. This method does also not install anything extra to your devise, to remove the project, simply delete the (.exe) file in your file explorer. Please note that it can take a few moments for everything in the (.exe) file to load and initialise, so nothing might not appear to happen at first. Also, you can only run one instance of Pycraft at any time (even if you are using another method).

### Installing from PyPi (preferred)
If you are installing the project from PyPi, then you will need an up-to-date build of Python (3.7 or greater ideally) and also permission to install additional files to your device. Then you need to open a command-line interface (or CLI), or this we recommend Terminal on Apple based devises, and Command Prompt on Windows based machines. You install the latest version of Pycraft, and all its needed files though this command:
``pip install Python-Pycraft``
and you can also uninstall the project using the command:
``pip uninstall Python-Pycraft``
And now you can run the project as normal.
Please note that at present it can be a bit tricky to locate the files that have downloaded, you can import the project into another python file using:
``import Pycraft``
But there is a better solution on its way!

### Installing using Pipenv
You can alternatively run these commands in the directory containing a file called `Pipfile`:

``pip install pipenv`` then: ``pipenv install python-pycraft``

And to start the game: ``pipenv run python <PATH to 'main.py'>``

## Running The Program
When running the program, you will either have a (.exe) file, downloaded from the releases page, or you will have the developer preview, if you have the developer preview, which can be found in the files section of this repository then this is how you run that program. Pycraft has recently undergone some large structural redesigning, so to run the program the advice is now different:

Now you have the program properly installed hopefully (you’ll find out if you haven’t promptly!) you need to locate the file "main.py" basically all this program does is run the right modules, initiates the main program, and catches any errors that might arise in the program in a nicely rendered error screen, if it crashes on your first run then chances are you haven’t installed the program correctly, if it still doesn’t work then you can drop me an email @ "ThomasJebbo@gmail.com" or comment here on the repository, I do hope however that it works alright for you and you have a pleasant experience. I might also add this program has been developed on a Windows 64-bit computer however should run fine on a 32-bit Windows machine (uncompiled) or through MacOS although they remain untested for now. 

We recommend creating a shortcut for the "main.py" file too so it’s easier to locate.

## Credits
### With thanks to; <br />
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![OpenGL](https://img.shields.io/badge/OpenGL-%23FFFFFF.svg?style=for-the-badge&logo=opengl) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) ![Blender](https://img.shields.io/badge/blender-%23F5792A.svg?style=for-the-badge&logo=blender&logoColor=white) ![Canva](https://img.shields.io/badge/Canva-%2300C4CC.svg?style=for-the-badge&logo=Canva&logoColor=white) ![Figma](https://img.shields.io/badge/figma-%23F24E1E.svg?style=for-the-badge&logo=figma&logoColor=white) ![Gimp Gnu Image Manipulation Program](https://img.shields.io/badge/Gimp-657D8B?style=for-the-badge&logo=gimp&logoColor=FFFFFF) ![Inkscape](https://img.shields.io/badge/Inkscape-e0e0e0?style=for-the-badge&logo=inkscape&logoColor=080A13) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Visual Studio](https://img.shields.io/badge/Visual%20Studio-5C2D91.svg?style=for-the-badge&logo=visual-studio&logoColor=white) 	![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white) ![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) 	![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) ![Edge](https://img.shields.io/badge/Edge-0078D7?style=for-the-badge&logo=Microsoft-edge&logoColor=white) 
- Thomas Jebbo (PycraftDeveloper) @ www.github.com/PycraftDeveloper <br />
- Count of Freshness Traversal @ https://twitter.com/DmitryChunikhinn <br />
- Dogukan Demir (demirdogukan) @ https://github.com/demirdogukan <br />
- Henri Post (HenryFBP) @ https://github.com/HenryFBP <br />
- PyPi @ www.pypi.org <br />
- PIL (Pillow or Python Imaging Library) @ www.github.com/python-pillow/Pillow <br />
- Pygame @ www.github.com/pygame/pygame <br />
- Numpy @ www.github.com/numpy/numpy <br />
- PyOpenGL (and its counterpart PyOpenGL-accelerate) @ www.github.com/mcfletch/pyopengl <br />
- PyAutoGUI @ www.github.com/asweigart/pyautogui <br />
- Psutil @ www.github.com/giampaolo/psutil <br />
- PyWaveFront @ www.github.com/pywavefront/PyWavefront <br />
- Py-CPUinfo @ www.github.com/pytorch/cpuinfo <br />
- GPUtil @ www.github.com/anderskm/gputil <br />
- Tabulate @ www.github.com/p-ranav/tabulate <br />
- Moderngl @ https://github.com/moderngl/moderngl <br />
- Moderngl_window @ https://github.com/moderngl/moderngl-window <br />
- PyJoystick @ https://github.com/justengel/pyjoystick <br />
- Freedsound: - Erokia's "ambient wave compilation" @ www.freesound.org/s/473545 <br />
- Freedsound: - Soundholder's "ambient meadow near forest" @ www.freesound.org/s/425368 <br />
- Freedsound: - monte32's "Footsteps_6_Dirt_shoe" @ www.freesound.org/people/monte32/sounds/353799 <br />

## Uncompiled Pycraft Dependencies
When you’re installing the uncompiled Pycraft variant from here you need to install the following 'modules', which can be done through your Control Panel in Windows (First; press <windows key + r> then type "cmd" then run the below syntax) or on Apple systems in Terminal.

```
pip install <module>
pip uninstall <module>
```
pip is usually installed by default when installing Python with most versions.

- PIL (Pillow or Python Imaging Library) @ www.github.com/python-pillow/Pillow <br />
- Pygame @ www.github.com/pygame/pygame <br />
- Numpy @ www.github.com/numpy/numpy <br />
- PyAutoGUI @ www.github.com/asweigart/pyautogui <br />
- Psutil @ www.github.com/giampaolo/psutil <br />
- PyWaveFront @ www.github.com/pywavefront/PyWavefront <br />
- Py-CPUinfo @ www.github.com/pytorch/cpuinfo <br />
- GPUtil @ www.github.com/anderskm/gputil <br />
- Tabulate @ www.github.com/p-ranav/tabulate <br />
- Moderngl @ https://github.com/moderngl/moderngl <br />
- Moderngl_window @ https://github.com/moderngl/moderngl-window <br />
- PyJoystick @ https://github.com/justengel/pyjoystick <br />

_Disclaimer; unfortunately, lots of these python modules (first and third party) can require some external modules that will be installed during the installing process of the above modules, unfortunately this makes it really difficult to give credit to those modules, if you have any recommendations, please contact me appropriately._

## Changes
Pycraft v0.9.4 is now live! Here is a list of all the added features to this major update: <br />

* Feature: Full Linux compatibility has been added to Pycraft and will be supported in all future versions of Pycraft.
* Feature: The update section of the installer has been added; this connects to both the installer and uninstaller for an optimised method of downloading the latest version of Pycraft.
* Feature: Message functions have been improved with some errors and issues there getting ironed out.
* Feature: The entire installer has been restructured and mostly reprogrammed from the preview releases, this improves readability and follows a similar structure to the rest of the project now.
* Bug Fix: All known issues with the installer and project have been fixed that were known in the developer releases and older versions of Pycraft.
* Feature: The way music is loaded has changed to make the project friendlier on storage space and RAM.
* Performance Improvements: There have been numerous improvements to the installer and game to make it perform better with more optimisations still to arrive.
* Bug Fix: The benchmark section of the project has had some fundamental changes and now works fine with the changed game engine.

* Feature - The program can now detect when you are connected to the internet, if permission is given, this is to detect updates.
* Feature - Pycraft now can detect updates to itself and its required modules, this is displayed on the home screen.
* Feature - Pycraft's home screen has been updated to include access to the new installer.
* Bug-fix - Issues with sound playback in game when navigating between GUI's quickly has been addressed.

* Feature - The error screen has been re-designed, with more features coming in the next snapshot.
* Feature - Most of the errors in Pycraft now have been given more information so that debugging is easier.
* Feature - Devmode captions have been added into the 3D game-engine.
* Feature - Work on the documentation.
* Feature - The benchmark GUI has had some processing optimisations and the file for the read test has been tweaked from 'Mebibytes' to 'Megabytes'.
* Bug-fix - The delays with transitioning between the 2D and 3D games engine have been fixed.

* Feature: Section 1 of 3 on the installer has been added, you can now download and install Pycraft through this method, although currently I would not advise it, past versions of Pycraft available to the installer where not build for the Installer so an amount of messy file transfer has to go on to set everything up properly. Installing versions of Pycraft greater than v0.9.3 I’ll be a much smoother experience. The installer will receive a lot of work by the time of the release of this version of Pycraft and will also see a change to the README to accommodate this change.
* Bug-fix: There have been numerous bug-fixes in this version of Pycraft, many of the changes also include shortening the length of existing code, however the installer is very long and will have a lot of work done on it to get it to the standard of the rest of the modules in Pycraft.
* Documentation: There have been tweaks to the documentation for Pycraft v0.9.3 with a big change planned when it is finished (each file will have documentation separately) however the documentation for Pycraft v0.9.4 will not start until its release.

* Feature: 2 of the 5 sections of the installer are now complete; the modify and install sections are now finished, with the uninstall, update and repair menus still to be completed (although the process will be accelerated). This update also saw tweaks to the install section, which won’t work fully until the release of Pycraft v0.9.4.
* Feature: ``PyOpenGL (and PyOpenGL_accelerate)`` have been removed entirely from the project, due to a more Pythonic, easier to install and faster alternative called ``ModernGL`` and its separate window counterpart taking its place, this should help make the project much easier to install.
* Feature: As a result of ``PyOpenGL`` being removed, the ``PycraftStartupTest`` module as well as the 3D test in ``ExBenchmark`` have been redesigned, both are now faster and better optimised.
* Feature: The ``Credits`` menu has had some tweaks to the text engine making it easier to add accreditation to contributors and update in the future, with a new accelerated text wrapping engine for Pygame text rendering added, this supports wrapping large bodies of text a well as colouring individual words, which will be made use of in later versions. Currently it is used primarily in the ``Credits`` menu, but will also be used later in the ``Benchmark`` GUI and the ``GameEngine`` modules.
* Feature: 3 axis movement in the ``GameEngine`` module has been tweaked, with movement speed no longer being frame rate dependant and more representative of real speed, and the jump animation also being tweaked for the same reasons (although still a linear movement, this will be tweaked in a later version).
* Feature: Joystick/Controller support has been added to Pycraft, now you can choose between keyboard and mouse or controller (although keyboard and controller both work together, controller and mouse do not work in combo), this support is wide ranging and there are likely to be bugs, but the ones known to me have been removed.
* Feature: The ``Inventory`` and ``MapGUI`` modules have been heavily optimised, now images aren’t loaded every frame and are only tweaked when the window resizes, which is detected now differently on those GUIs (with more support coming soon for other GUIs). The ``MapGUI`` module has also been brought into the same structure as the rest of the project and now works much better, although will still need to be updated graphically.
* Feature: The ``Fancy Sky`` setting has been swapped for ``Fancy Graphics`` which now toggles some of the new on-screen elements of the display, improving performance, although it should be noted, toggling the ``anti-aliasing`` setting will likely make a bigger change. ``anti-aliasing`` has not yet been added into the ``GameEngine``, with support coming soon there.
* Feature: The ``installer`` can now be reached directly through Pycraft.
* Feature: The 'tool-tips' text that appears on the new load screen has been updated with key changes as well as to showcase some of the project’s new features.
* Feature: The old load screen menu has been re-added and improved greatly.
* Feature: Object caching has been added to Pycraft, so now the ``GameEngine`` module will load quicker (with more support coming at a later date).
* Feature: Some files in the game are now loaded once centrally, notably the window icon and title font, which are used throughout Pycraft, so the total read/write count when running Pycraft has been significantly reduced (Especially in the ``Inventory`` and ``MapGUI`` modules).
* Feature: The project's caption has now been changed to have rounded corners using alpha, this is in light of the design changes as a part of Windows 11, and as a general aesthetic feature.

* Feature: 3 of the 5 sections of the installer utility is now complete, you can now - in addition to its previous functions - uninstall the project with 3 customisable options:
* * Uninstall both Pycraft and all additional files
* * Uninstall both Pycraft and all additional files but keep save data
* * Uninstall only Pycraft and leave all additional files
* Additionally, a large amount of the bugs and issues with the other aspects of the installer have also been corrected although any more bug reports will always help to make any aspect of the project better.
* The theme section menu has been entirely re-designed to support screen resizing and greatly improved graphics.
* The entire project has seen changes to the controller engine so now the performance there has been heavily improved.
* The entire project has had performance improvements.
* The first section of the benchmark GUI has seen changes to the text structure to make the menu easy to modify and now has updated instructions (with more improvements there coming soon!)
* There have been changes made to the messaging system on the home screen to further improve performance and allow for multiple messages to be properly handled.

Again, feedback would be much appreciated this update was released on; 03/04/2022 (UK date; DD/MM/YYYY). As always, we hope you enjoy this new release and feel free to leave feedback.

## Our Update Policy
New releases will be introduced regularly, it is likely that there will be some form of error or bug, therefore unless you intend to use this project for development and feedback purposes (Thank you all!) we recommend you use the latest stable release; below is how to identify the stable releases.

## Version Naming
Versions have changed pretty dramatically the past few days, don’t panic I'm here to help! In short, the new version naming system more closely follows the Semantic Naming system:
For example; Pycraft v0.9.2.1 The first number is relevant to if the project is in a finished state. The second number relates to the number of updates Pycraft has had. The third number relates to smaller sub-updates (that likely will not feature a (.exe) release). The last number there is rarely used, this is typically for PyPi releases only, as we can't edit uploaded version of the project, we use this number if there is an important change to the project description, those updates will not include any code changing!

## Releases
All past versions of Pycraft are available under the releases section of Pycraft, this is a new change, but just as before, major releases like Pycraft v0.9 and Pycraft v0.8 will have (.exe) releases, but smaller sub-releases will not, this is in light of a change coming to Pycraft, this should help with the confusion behind releases, and be more accommodating to the installer that's being worked on as a part of Pycraft v0.9.4. This brings me on to another point, all past updates to Pycraft will be located at the releases page (Thats all versions), and the previous section on the home-page with branches will change. The default branch will be the most recent release, then there will be branches for all the sub-releases to Pycraft there too; and the sister program; Pycraft-Insider-Preview will be deprecated and all data moved to relevant places in this repository, this should hopefully cut down on the confusion and make the project more user-friendly.

## Other Sources
I have started writing an article on medium which is released at the start of every month, this compliments the weekly updates that are posted on my twitter profile, it would be greatly appreciated if you wanted to check it out here at this link: (https://medium.com/@PycraftDev), these articles are also uploaded to my other account on Dev here: (https://dev.to/pycraftdev). Any recommendations and feedback are, as always, greatly appreciated, a lot of time and work goes into making this happen!

## Final Notices
Thank you greatly for supporting this project simply by running it, I am sorry in advance for any spelling mistakes. The programs will be updated frequently and I shall do my best to keep this up to date too. I also want to add that you are welcome to view and change the program and share it with your friends however please may I have some credit, just a name would do and if you find any bugs or errors, please feel free to comment in the comments section any feedback so I can improve my program, it will all be much appreciated and give as much detail as you wish to give out.
