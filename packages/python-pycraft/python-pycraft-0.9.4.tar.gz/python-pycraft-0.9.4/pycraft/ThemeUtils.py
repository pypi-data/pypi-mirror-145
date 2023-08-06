if not __name__ == "__main__":
    print("Started <Pycraft_ThemeUtils>")
    class DetermineThemeColours:
        def __init__(self):
            pass

        def GetColours(self):
            try:
                self.themeArray = [[(255, 255, 255), [30, 30, 30], (80, 80, 80), (237, 125, 49), (255, 255, 255)], [(0, 0, 0), [255, 255, 255], (80, 80, 80), (237, 125, 49), (100, 100, 100)]]
                if self.theme == "dark":
                    self.FontCol = self.themeArray[0][0]
                    self.BackgroundCol = self.themeArray[0][1]
                    self.ShapeCol = self.themeArray[0][2]
                    self.AccentCol = self.themeArray[0][3]
                    self.SecondFontCol = self.themeArray[0][4]
                elif self.theme == "light":
                    self.FontCol = self.themeArray[1][0]
                    self.BackgroundCol = self.themeArray[1][1]
                    self.ShapeCol = self.themeArray[1][2]
                    self.AccentCol = self.themeArray[1][3]
                    self.SecondFontCol = self.themeArray[1][4]
            except Exception as Message:
                self.ErrorMessage = "ThemeUtils > DetermineThemeColours > GetColours: "+str(Message)


        def GetThemeGUI(self):
            try:
                Title = self.TitleFont.render("Pycraft", True, self.FontCol)
                TitleWidth = Title.get_width()
                
                MiddleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)

                SideFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20) 
                
                mousebuttondown = False
                
                Name = SideFont.render("By Tom Jebbo", self.aa, self.FontCol)
                NameHeight = Name.get_height()

                Version = SideFont.render(f"Version: {self.version}", self.aa, self.FontCol) 
                VersionWidth = Version.get_width()
                VersionHeight = Version.get_height()
                
                DarkModeFont = MiddleFont.render("Dark", True, self.FontCol)
                DarkModeFont_Width = DarkModeFont.get_width()
                DarkModeFont_Height = DarkModeFont.get_height()
                
                LightModeFont = MiddleFont.render("Light", True, self.FontCol)
                LightModeFont_Width = LightModeFont.get_width()
                LightModeFont_Height = LightModeFont.get_height()
                
                Mx, My = self.realWidth/2, self.realHeight/2

                while True:
                    if self.UseMouseInput == False:
                        JoyMouseMovementX, JoyMouseMovementY = self.mod_JoystickUtil__.MoveCursor.UpdateMousePos(self, 3)
                        Mx, My = Mx+JoyMouseMovementX, My+JoyMouseMovementY
                        self.mod_Pygame__.mouse.set_pos(Mx, My)
                    else:
                        self.JoystickConfirm = False
                        
                    if self.UseMouseInput == True:
                        Mx, My = self.mod_Pygame__.mouse.get_pos()
                        
                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Theme Selector")
                    self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                    
                    LightRect = self.mod_Pygame__.Rect(0, 100, self.realWidth/2, self.realHeight-200)
                    DarkRect = self.mod_Pygame__.Rect(self.realWidth/2, 100, self.realWidth/2, self.realHeight-200)
                    
                    self.Display.fill(self.BackgroundCol)
                    
                    Name = SideFont.render("By Tom Jebbo", self.aa, self.FontCol)
                    NameHeight = Name.get_height()

                    Version = SideFont.render(f"Version: {self.version}", self.aa, self.FontCol) 
                    VersionWidth = Version.get_width()
                    VersionHeight = Version.get_height()
                    
                    Title = self.TitleFont.render("Pycraft", True, self.FontCol)
                    TitleWidth = Title.get_width()
                    
                    self.Display.blit(Title, ((self.realWidth-TitleWidth)/2, 0))
                    self.Display.blit(Name, (0, (self.realHeight-NameHeight)))
                    self.Display.blit(Version, ((self.realWidth-VersionWidth)-2, (self.realHeight-VersionHeight)))
                    
                    self.theme = "light"
                    self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                    self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), LightRect)
                    self.mod_Pygame__.draw.rect(self.Display, (self.ShapeCol), LightRect, 3)
                    LightModeFont = MiddleFont.render("Light", True, self.FontCol)
                    LightModeFont_Width = LightModeFont.get_width()
                    LightModeFont_Height = LightModeFont.get_height()
                    self.Display.blit(LightModeFont, (((self.realWidth/2)-LightModeFont_Width)/2, (self.realHeight-LightModeFont_Height)/2))
                    
                    self.theme = "dark"
                    self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                    self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), DarkRect)
                    self.mod_Pygame__.draw.rect(self.Display, (self.ShapeCol), DarkRect, 3)
                    DarkModeFont = MiddleFont.render("Dark", True, self.FontCol)
                    DarkModeFont_Width = DarkModeFont.get_width()
                    DarkModeFont_Height = DarkModeFont.get_height()
                    self.Display.blit(DarkModeFont, (((self.realWidth+(self.realWidth/2))-DarkModeFont_Width)/2, (self.realHeight-DarkModeFont_Height)/2))
                    
                    if My >= 100 and My <= self.realHeight-100:
                        if Mx <= self.realWidth/2:
                            self.mod_Pygame__.draw.rect(self.Display, (self.AccentCol), LightRect, 1)
                            self.theme = "light"
                            if mousebuttondown == True:
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                break
                        elif Mx >= self.realWidth/2:
                            self.mod_Pygame__.draw.rect(self.Display, (self.AccentCol), DarkRect, 1)
                            self.theme = "dark"
                            if mousebuttondown == True:
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                break
                            
                        self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                    
                    Choice = SideFont.render(f"You have selected the {self.theme} theme, you can change this later in settings", self.aa, self.FontCol) 
                    ChoiceWidth = Choice.get_width()
                    ChoiceHeight = Choice.get_height()
                    self.Display.blit(Choice, ((self.realWidth-ChoiceWidth)/2, (self.realHeight-NameHeight)))
                    
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT:
                            self.Stop_Thread_Event.set()

                            self.Thread_StartLongThread.join()
                            self.Thread_AdaptiveMode.join()
                            self.Thread_StartLongThread.join()
                            
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit()
                        if event.type == self.mod_Pygame__.MOUSEBUTTONDOWN:
                            mousebuttondown = True
                        if event.type == self.mod_Pygame__.MOUSEBUTTONUP:
                            mousebuttondown = False
                            
                    self.mod_Pygame__.display.update()
                    self.clock.tick(self.FPS)
            except Exception as Message:
                self.ErrorMessage = "ThemeUtils > DetermineThemeColours > GetThemeGUI: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()