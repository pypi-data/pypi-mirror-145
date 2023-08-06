print("Started <Pycraft_InstallerUtil>")
class GetInstallerData:
    def __init__():
        pass
    
    def GetData(InstallerImportData):
        try:
            if InstallerImportData.platform == "Linux":
                with open(InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Data_Files//InstallerConfig.json")), 'r') as openFile:
                    SavedData = InstallerImportData.mod_Json__.load(openFile)
            else:
                with open(InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Data_Files\\InstallerConfig.json")), 'r') as openFile:
                    SavedData = InstallerImportData.mod_Json__.load(openFile)

        except Exception as Message:
            PycPath = None
            Repair = {"PATH":None}
            
            if InstallerImportData.platform == "Linux":
                with open(InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Data_Files//InstallerConfig.json")), 'w') as openFile:
                    InstallerImportData.mod_Json__.dump(Repair, openFile)
            else:
                with open(InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Data_Files\\InstallerConfig.json")), 'w') as openFile:
                    InstallerImportData.mod_Json__.dump(Repair, openFile)

        else:
            PycPath = SavedData["PATH"]
            
        return PycPath
    

class CoreInstallerFunctionality:
    def __init__():
        pass
    
    
    def Close(InstallerImportData):
        if InstallerImportData.mod_Tkinter_messagebox_.askokcancel("Pycraft Setup Wizard", "Are you sure you want to cancel the install?"):
            InstallerImportData.mod_Sys__.exit()
            
            
    def Home(InstallerImportData, root, PycPath, ChooseBETA, Choice):
        InstallerImportData.mod_Installer_HomeScreen_.Installer_Home.Start(InstallerImportData, root, PycPath, ChooseBETA, Choice)
        
        
    def OutdatedDetector(InstallerImportData):
        try:
            import urllib.request as urlOpener
            urlOpener.urlopen('https://www.google.com', timeout=1)
            
            List = InstallerImportData.mod_Subprocess__.check_output([InstallerImportData.mod_Sys__.executable, "-m","pip","list","--outdated"], False)
            global Outdated
            if b"Python-Pycraft" in List:
                Outdated =  True
            else:
                Outdated = False
        except Exception as Message:
            InstallerImportData.mod_Tkinter_messagebox_.showerror("An error has occurred",
                                                                  f"We were unable to check for updates to Pycraft, the most likely reason for this is a faulty internet connection.\n\nFull Error Message:\n{Message}")
            InstallerImportData.mod_Sys__.exit()
        
class FileManipulation:
    def __init__():
        pass
        
        
    def MoveFiles(InstallerImportData, Dir):
        global CurrentLocation
        try:
            temp = str(CurrentLocation.decode('UTF-8'))[:-1]
        except Exception as Message:
            temp = InstallerImportData.mod_Site__.getusersitepackages()
            
        try:
            InstallerImportData.mod_shutil__.copytree(fr"{temp}\\pycraft", fr"{Dir}\\pycraft")
        except Exception as Message:
            InstallerImportData.mod_Tkinter_messagebox_.showerror("An error has occurred",
                                                                  f"We were unable to move Pycraft to the requested install location.\n\nFull Error Message:\n{Message}")
            InstallerImportData.mod_Sys__.exit()
        
        
    def DownloadandInstall(InstallerImportData, choice):
        try:
            if choice == "Latest":
                InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft"], False) # InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft"], False)
            else: #["none", "Pycraft-v0.9.1", "Pycraft-v0.9.2", "Pycraft-v0.9.3"]
                if choice == "Pycraft-v0.9.1":
                    InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft==0.9.1"], False)
                elif choice == "Pycraft-v0.9.2":
                    InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft==0.9.2"], False)
                elif choice == "Pycraft-v0.9.3":
                    InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft==0.9.3"], False)
                else:
                    InstallerImportData.mod_Subprocess__.check_call([InstallerImportData.mod_Sys__.executable, "-m","pip","install","python-pycraft"], False)
        except Exception as Message:
            InstallerImportData.mod_Tkinter_messagebox_.showerror("An error ocurred",
                                                                  f"We were unable to install the additional files Pycraft needs in-order to install.\n\nFull Error Message: {Message}")
            InstallerImportData.mod_Sys__.exit()
            
            
    def search_files(InstallerImportData, directory):
        arr = []
        print(f"Scanning {directory}")
        for dirpath, dirnames, files in InstallerImportData.mod_Os__.walk(directory):
            for name in files:
                arr.append(f"{dirpath}\{name}")
        return arr
    
    
    def remove_files(InstallerImportData, FileArray, keep_save=False):
        try:
            for i in range(len(FileArray)):
                try:
                    if keep_save == True:
                        if not ("Data_Files" in FileArray[i] or "distutils" in FileArray[i] or "pip" in FileArray[i] or "setuptools" in FileArray[i] or "pkg_resources" in FileArray[i] or "README" in FileArray[i] or "win32" in FileArray[i] or "wheel" in FileArray[i]):
                            InstallerImportData.mod_Os__.remove(FileArray[i])
                    else:
                        if not ("distutils" in FileArray[i] or "pip" in FileArray[i] or "setuptools" in FileArray[i] or "pkg_resources" in FileArray[i] or "README" in FileArray[i] or "win32" in FileArray[i] or "wheel" in FileArray[i]):
                            InstallerImportData.mod_Os__.remove(FileArray[i])

                except Exception as Message:
                    print(Message)
        except Exception as Message:
            InstallerImportData.mod_Tkinter_messagebox_.showerror("An error ocurred", f"We were unable to remove some files for Pycraft from your PC.\n\nFull Error Message: {Message}")
            InstallerImportData.mod_Sys__.exit()