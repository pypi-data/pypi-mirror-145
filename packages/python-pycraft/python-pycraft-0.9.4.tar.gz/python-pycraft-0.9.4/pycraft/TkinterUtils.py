if not __name__ == "__main__":
    print("Started <Pycraft_TkinterUtils>")
    class TkinterInfo:
        def __init__(self):
            pass
        
        def GetPermissions(self):
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            answer = messagebox.askquestion("Check Permission", "Can we have your permission to check the internet for updates to Pycraft?")
            if answer == "yes":
                self.ConnectionPermission = True
            else:
                self.ConnectionPermission = False

        def CreateTkinterWindow(self):
            DataWindow = self.mod_Tkinter__tk.Tk()
            DataWindow.title("Player Information")
            DataWindow.configure(width = 500, height = 300) 
            DataWindow.configure(bg="lightblue") 
            VersionData = f"Pycraft: v{self.version}"
            CoordinatesData = f"Coordinates: x: {self.X} y: {self.Y} z: {self.Z} Facing: 0.0, 0.0, 0.0" 
            FPSData = f"FPS: Actual: {self.eFPS} Max: {self.FPS}" 
            VersionData = self.mod_Tkinter__tk.Label(DataWindow, text=VersionData) 
            CoordinatesData = self.mod_Tkinter__tk.Label(DataWindow, text=CoordinatesData) 
            FPSData = self.mod_Tkinter__tk.Label(DataWindow, text=FPSData) 
            VersionData.grid(row = 0, column = 0, columnspan = 2) 
            CoordinatesData.grid(row = 1, column = 0, columnspan = 2)
            FPSData.grid(row = 2, column = 0, columnspan = 2)
            DataWindow.mainloop() 
            DataWindow.quit()
            
            
    class TkinterInstaller:
        def __init__():
            pass
        
        def CreateDisplay(InstallerImportData, root):
            try:
                geometry = root.winfo_geometry().split("+")
                Xpos, Ypos = geometry[1], geometry[2]
                root.destroy()
            except:
                Xpos, Ypos = 0, 0
                pass

            root = InstallerImportData.mod_Tkinter_tk_.Tk()

            root.title("Pycraft Setup Wizard")
            root.resizable(False, False)
            root.configure(bg='white')
            root.geometry(f"850x537+{int(Xpos)}+{int(Ypos)}")
            if InstallerImportData.platform == "Linux":
                ImageFileLocation = InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Resources//Installer_Resources//Banner.png"))
            else:
                ImageFileLocation = InstallerImportData.mod_Os__.path.join(InstallerImportData.base_folder, ("Resources\Installer_Resources\Banner.png"))
                
            InstallerImportData.mod_ImageUtils__.TkinterInstaller.open_img(InstallerImportData, root, ImageFileLocation)
            return root
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()