if not __name__ == "__main__":
    print("Started <Pycraft_GetSavedData>")
    class FixInstaller:
        def __init__(self):
            pass
        
        def SetInstallLocation(self):
            try:
                Repair = {"PATH":self.base_folder}
                if self.platform == "Linux":
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files//InstallerConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(Repair, openFile)
                else:
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\InstallerConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(Repair, openFile)
            except Exception as Message:
                self.ErrorMessage = "GetSavedData > FixInstaller > SetInstallLocation: "+str(Message)
                
        def GetInstallLocation(self):
            try:
                if self.platform == "Linux":
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files//InstallerConfig.json")), 'r') as openFile:
                        StoredData = self.mod_JSON__.load(openFile)
                else:
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\InstallerConfig.json")), 'r') as openFile:
                        StoredData = self.mod_JSON__.load(openFile)
                self.InstallLocation = StoredData["PATH"]
            except Exception as Message:
                print("Message:", Message)
                self.InstallLocation = None
                
    class LoadSaveFiles: 
        def __init__(self):
            pass
                        
        def ReadMainSave(self):
            if self.platform == "Linux":
                with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files//SaveGameConfig.json")), 'r') as openFile:
                    save = self.mod_JSON__.load(openFile)
            else:
                with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'r') as openFile:
                    save = self.mod_JSON__.load(openFile)

            self.theme = save["theme"]
            self.RunFullStartup = save["startup"]
            self.crash = save["crash"]
            self.Fullscreen = save["WindowStatus"]
            self.RecommendedFPS = save["AdaptiveFPS"]
            self.Devmode = save["Devmode"]
            self.SettingsPreference = save["profile"]
            self.FPS = save["FPS"]
            self.aFPS = save["aFPS"]
            self.Iteration = save["Iteration"]
            self.FOV = save["FOV"]
            self.cameraANGspeed = save["cameraANGspeed"]
            self.RenderFOG = save["RenderFOG"]
            self.aa = save["aa"]
            self.X = save["X"]
            self.Y = save["Y"]
            self.Z = save["Z"]
            self.FancyGraphics = save["FancyGraphics"]
            self.FanPart = save["FanPart"]
            self.sound = save["sound"]
            self.soundVOL = save["soundVOL"]
            self.music = save["music"]
            self.musicVOL = save["musicVOL"]
            self.lastRun = save["lastRun"]
            self.SavedWidth = save["DisplayWidth"]
            self.SavedHeight = save["DisplayHeight"]
            self.ConnectionPermission = save["ConnectionPermission"]
            self.Total_Vertices = save["Total_Vertices"]
            self.Updated = save["Updated"]
            self.ResourceCheckTime = save["ResourceLoadTime"]
            self.LoadTime = save["LoadTime"]
            if self.Total_Vertices == 0:
                self.Total_Vertices = 1


        def RepairLostSave(self):
            try:
                SavedData = {"Total_Vertices":0, "theme":False, "profile":"Medium", "Devmode":0, "AdaptiveFPS": 60, "FPS":60, "aFPS":60, "Iteration":1, "FOV":75, "cameraANGspeed":3, "aa":True, "RenderFOG":True, "FancyGraphics":True, "FanPart":True, "sound":True, "soundVOL":75, "music":True, "musicVOL":50, "X":0, "Y":0, "Z":0, "lastRun":"29/09/2021", 'startup':True, 'crash': False, 'DisplayWidth':1280, 'DisplayHeight':720, 'WindowStatus':True, 'ConnectionPermission': None, 'Updated':True, 'LoadTime':[0, 1], "ResourceLoadTime":[0, 0]}
                if self.platform == "Linux":
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files//SaveGameConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(SavedData, openFile)
                else:
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(SavedData, openFile)

            except Exception as Message:
                print(Message)
                self.ErrorMessage = "GetSavedData > LoadSaveFiles > RepairLostSave: "+str(Message)
            
        def SaveTOconfigFILE(self):
            try:
                current_time = self.mod_Datetime__.datetime.now()
                currentDate = f"{current_time.day}/{current_time.month}/{current_time.year}"
                if self.Updated == True:
                    self.Updated = False
                SavedData = {"Total_Vertices":self.Total_Vertices, "theme":self.theme, "profile":self.SettingsPreference, "Devmode":self.Devmode, "AdaptiveFPS": self.RecommendedFPS, "FPS":self.FPS, "aFPS":self.aFPS, "Iteration":self.Iteration, "FOV":self.FOV, "cameraANGspeed":self.cameraANGspeed, "aa":self.aa, "RenderFOG":self.RenderFOG, "FancyGraphics":self.FancyGraphics, "FanPart":self.FanPart, "sound":self.sound, "soundVOL":self.soundVOL, "music":self.music, "musicVOL":self.musicVOL, "X":self.X, "Y":self.Y, "Z":self.Z, "lastRun":currentDate, 'startup':self.RunFullStartup, 'crash': False, 'DisplayWidth':self.SavedWidth, 'DisplayHeight':self.SavedHeight, 'WindowStatus':self.Fullscreen, "ConnectionPermission": self.ConnectionPermission, 'Updated':self.Updated, 'LoadTime':self.LoadTime, "ResourceLoadTime":[self.ResourceCheckTime[0], self.ResourceCheckTime[1]]}
                if self.platform == "Linux":
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files//SaveGameConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(SavedData, openFile)
                else:
                    with open(self.mod_OS__.path.join(self.base_folder, ("Data_Files\\SaveGameConfig.json")), 'w') as openFile:
                        self.mod_JSON__.dump(SavedData, openFile)
            except Exception as Message:
                self.ErrorMessage = "GetSavedData > LoadSaveFiles > SaveTOconfigFILE: "+str(Message)

else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()