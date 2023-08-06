from ast import Return
from unittest.loader import VALID_MODULE_NAME


if not __name__ == "__main__":
    print("Started <Pycraft_Credits>")
    class GenerateCredits:
        def __init__(self):
            pass

        def Credits(self):
            try:
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.flip() 
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Credits")
                if self.platform == "Linux":
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    LargeCreditsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)
                    InfoTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)
                    SmallCreditsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                else:
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    LargeCreditsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)
                    InfoTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                    SmallCreditsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                TitleFont = self.TitleFont.render("Pycraft", self.aa, self.FontCol)
                TitleWidth = TitleFont.get_width()
                TitleHeight = TitleFont.get_height()
                CreditsFont = InfoTitleFont.render("Credits", self.aa, self.SecondFontCol)
                
                CreditsString = [f"Pycraft: v{self.version}",
                                    " ",
                                    " ",
                                    "Game Director: Tom Jebbo",
                                    " ",
                                    "Art and Music Lead: Tom Jebbo",
                                    " ",
                                    "Additional Music Credits:",
                                    "Freesound: - Erokia's 'ambient wave compilation' @ freesound.org/s/473545",
                                    "Freesound: - Soundholder's 'ambient meadow near forest' @ freesound.org/s/425368",
                                    "Freesound: - monte32's 'Footsteps_6_Dirt_shoe' @ freesound.org/people/monte32/sounds/353799",
                                    " ",
                                    "Pycraft was developed in collaboration with:",
                                    "Dogukan Demir (https://github.com/demirdogukan)",
                                    "Henry Post (https://github.com/HenryFBP)",
                                    "Count of Freshness Traversal (https://twitter.com/DmitryChunikhinn)",
                                    " ",
                                    "With thanks to the developers of:",
                                    "Pyrr",
                                    "Inputs",
                                    "PSutil",
                                    "Python",
                                    "Pygame",
                                    "Numpy",
                                    "Nuitka",
                                    "CPUinfo",
                                    "Tabulate",
                                    "ModernGL",
                                    "PyInstaller",
                                    "PyAutoGUI",
                                    "PyWaveFront",
                                    "ModernGL_window",
                                    "Microsoft Visual Studio Code",
                                    "PIL (Pillow/Python Imaging Library)",
                                    "For a more in depth accreditation please check Pycraft's GitHub Page here: github.com/PycraftDeveloper/Pycraft",
                                    " ",
                                    "With thanks to:",
                                    "All my Twitter followers, and you for installing this game, that's massively appreciated!",
                                    "For more information please visit Pycraft's GitHub repository",
                                    " ",
                                    "Final Comments:",
                                    "Thank you greatly for supporting this project simply by running it, I am sorry in advance for any spelling mistakes. The programs will be updated frequently and I shall do my best to keep this up to date too. I also want to add that you are welcome to view and change the program and share it with your friends however please may I have some credit, just a name would do and if you find any bugs or errors, please feel free to comment in the comments section any feedback so I can improve my program, it will all be much appreciated and give as much detail as you wish to give out.",
                                    " ",
                                    " ",
                                    "Thank You!"]

                self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                VisualYdisplacement = self.realHeight
                IntroYDisplacement = (self.realHeight-TitleHeight)/2
                timer = 5
                tempFPS = self.FPS

                EndClock = 0
                
                Mx, My = self.realWidth/2, self.realHeight/2
                
                HoldOnExit = False
                HoldTimer = 0
                
                LoadText = False
                while True:
                    if self.UseMouseInput == False:
                        Mx, My = Mx+self.JoystickMouse[0], My+self.JoystickMouse[1]
                        self.mod_Pygame__.mouse.set_pos(Mx, My)
                    else:
                        self.JoystickConfirm = False
                        
                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Credits")
                    self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()

                    if self.realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if self.realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)

                    self.eFPS = self.clock.get_fps()
                    self.aFPS += self.eFPS
                    self.Iteration += 1
                    
                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)

                    for event in self.mod_Pygame__.event.get(): 
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                        elif event.type == self.mod_Pygame__.KEYDOWN: 
                            if event.key == self.mod_Pygame__.K_SPACE and self.Devmode < 10: 
                                self.Devmode += 1 
                            if event.key == self.mod_Pygame__.K_q:
                                self.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(self)
                            if event.key == self.mod_Pygame__.K_F11:
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)
                            if event.key == self.mod_Pygame__.K_x: 
                                self.Devmode = 1 

                    if self.UseMouseInput == False:
                        if self.JoystickExit == True:
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                            
                    self.Display.fill(self.BackgroundCol)
                    
                    Ypos = 0
                    for i in range(len(CreditsString)):
                        if LoadText == True:
                            if i > 0:
                                if CreditsString[i-1] == " ":
                                    TextSurface = LargeCreditsFont.render(CreditsString[i], self.aa, self.FontCol)
                                else:
                                    TextSurface = SmallCreditsFont.render(CreditsString[i], self.aa, self.FontCol)
                            else:
                                TextSurface = LargeCreditsFont.render(CreditsString[i], self.aa, self.FontCol)
                                
                            TextSurfaceHeight = TextSurface.get_height()
                            TextSurfaceWidth = TextSurface.get_width()
                            
                            if TextSurfaceWidth > self.realWidth:
                                Ypos += self.mod_TextUtils__.TextWrap.blit_text(self, CreditsString[i], (3, Ypos+VisualYdisplacement), SmallCreditsFont, self.AccentCol)
                            else:
                                if i+1 == len(CreditsString) and HoldOnExit == True:
                                    self.Display.blit(TextSurface, ((self.realWidth-TextSurfaceWidth)/2, (self.realHeight-TextSurfaceHeight)/2))
                                else:
                                    if Ypos+VisualYdisplacement >= 0 and Ypos+VisualYdisplacement <= self.realHeight:
                                        self.Display.blit(TextSurface, ((self.realWidth-TextSurfaceWidth)/2, Ypos+VisualYdisplacement))
                            Ypos += TextSurfaceHeight
                        
                    if timer >= 1:
                        self.Display.blit(TitleFont, ((self.realWidth-TitleWidth)/2, 0+IntroYDisplacement))
                        timer -= 1/(self.aFPS/self.Iteration)
                        VisualYdisplacement = self.realHeight
                    else:
                        if IntroYDisplacement <= 0:
                            cover_Rect = self.mod_Pygame__.Rect(0, 0, self.realWidth, 90)
                            self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), cover_Rect)
                            self.Display.blit(TitleFont, ((self.realWidth-TitleWidth)/2, 0))
                            self.Display.blit(CreditsFont, (((self.realWidth-TitleWidth)/2)+65, 50))
                            VisualYdisplacement -= 60/(self.aFPS/self.Iteration)
                            LoadText = True
                            if Ypos+VisualYdisplacement <= 360:
                                HoldOnExit = True
                                HoldTimer += 1/(self.aFPS/self.Iteration)
                                if HoldTimer >= 6:
                                    return
                        else:
                            cover_Rect = self.mod_Pygame__.Rect(0, 0, 1280, 90)
                            self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), cover_Rect)
                            self.Display.blit(TitleFont, ((self.realWidth-TitleWidth)/2, 0+IntroYDisplacement))
                            self.Display.blit(CreditsFont, (((self.realWidth-TitleWidth)/2)+65, 50+IntroYDisplacement))
                            IntroYDisplacement -= 90/(self.aFPS/self.Iteration)
                            VisualYdisplacement = self.realHeight
                    
                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(self, DataFont)
                    
                    self.mod_Pygame__.display.flip() 
                    self.clock.tick(tempFPS)
                    
                    if not self.ErrorMessage == None:
                        self.ErrorMessage = "Credits > GenerateCredits > Credits: "+str(self.ErrorMessage)
                        return
                    
            except Exception as Message:
                self.ErrorMessage = "Credits > GenerateCredits > Credits: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()