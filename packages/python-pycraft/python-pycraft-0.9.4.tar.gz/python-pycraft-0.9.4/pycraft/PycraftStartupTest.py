if not __name__ == "__main__":
    print("Started <Pycraft_PycraftStartupTest>")
    class StartupTest:
        def __init__(self):
            pass

        def PycraftSelfTest(self):
            try:
                self.mod_Pygame__.display.set_icon(self.WindowIcon)

                SDLversion = self.mod_Pygame__.get_sdl_version()[0]
                RAM = (((self.mod_Psutil__.virtual_memory().available)/1000)/1000) # expressed in MB
                
                OpenGLversion = self.mod_ModernGL_window_.conf.settings.WINDOW['gl_version']

                if OpenGLversion[0] < 2 and OpenGLversion[1] >= 8:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror("Invalid OpenGL version", f"OpenGL version: {OpenGLversion[0]}.{ OpenGLversion[1]} is not supported; try a version greater than 2.7")
                    quit()
                if SDLversion < 2:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror("Invalid SDL version", f"SDL version: {SDLversion} is not supported; try a version greater than or equal to 2")
                    quit()
                if RAM < 200:
                    root = self.mod_Tkinter__tk.Tk()
                    root.withdraw()
                    self.mod_Tkinter_messagebox_.showerror("Minimum system requirements not met", f"Your system does not meet the minimum 100mb free memory specification needed to play this game")
                    quit()
                    
                if self.mod_Sys__.platform == "win32" or self.mod_Sys__.platform == "win64":
                    self.mod_OS__.environ["SDL_VIDEO_CENTERED"] = "1"
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                self.ErrorMessage = "PycraftStartupTest > StartupTest > PycraftSelfTest: "+str(Message)
                    
                    
        def PycraftResourceTest(self):
            try:
                if not self.currentDate == self.lastRun or self.crash == True or self.RunFullStartup == True:
                    if self.ResourceCheckTime[0] >= 25:
                        self.ResourceCheckTime = [-1, 0]
                    StartTime = self.mod_Time__.perf_counter()
                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//front.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\front.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//back.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\back.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//left.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\left.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//right.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\right.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//top.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\top.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//skybox//bottom.jpg"))).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\skybox\\bottom.jpg"))).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, f"Resources//General_Resources//selectorICONlight.jpg")).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, f"Resources\\General_Resources\\selectorICONlight.jpg")).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, f"Resources//General_Resources//selectorICONdark.jpg")).convert()
                    else:
                        self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, f"Resources\\General_Resources\\selectorICONdark.jpg")).convert()

                    if self.platform == "Linux":
                        self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources//General_Resources//InventoryGeneral.ogg")))
                    else:
                        self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\InventoryGeneral.ogg")))

                    if self.platform == "Linux":
                        self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources//General_Resources//Click.wav")))
                    else:
                        self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Click.wav")))
                        
                    self.AnimateLogo = True
                    self.CurrentResourceCheckTime = self.mod_Time__.perf_counter()-StartTime
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                self.ErrorMessage = "PycraftStartupTest > StartupTest > PycraftResourceTest: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()