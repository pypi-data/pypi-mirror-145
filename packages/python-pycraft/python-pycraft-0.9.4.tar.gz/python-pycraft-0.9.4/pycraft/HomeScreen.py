if not __name__ == "__main__":
    print("Started <Pycraft_HomeScreen>")
    class GenerateHomeScreen:
        def __init__(self):
            pass
        
        def DisplayMessage(self, MessageFont, Message, Colour):
            try:
                StartTime = self.mod_Time__.perf_counter()
                MessageText = MessageFont.render(Message, self.aa, Colour, self.BackgroundCol)
                MessageTextWidth = MessageText.get_width()
                MessageTextHeight = MessageText.get_height()
                while self.mod_Time__.perf_counter()-StartTime < 3:
                    if self.Command == None:
                        pos = (self.realWidth-MessageTextWidth)/2, (self.realHeight-MessageTextHeight)
                        self.Display.blit(MessageText, (pos))
                        self.mod_Pygame__.display.update(pos, (MessageTextWidth, MessageTextHeight))
                        self.mod_Time__.sleep(1)
                    else:
                        break
                
                try:
                    if self.mod_Pygame__.display.get_init() == True:
                        self.Display.fill(self.BackgroundCol)
                        pos = (self.realWidth-MessageTextWidth)/2, (self.realHeight-MessageTextHeight)
                        self.mod_Pygame__.display.update(pos, (MessageTextWidth, MessageTextHeight))
                except:
                    pass
                self.CurrentlyDisplayingMessage = False
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                if not Message == "display Surface quit":
                    self.ErrorMessage = "HomeScreen > GenerateHomeScreen > DisplayMessage (thread): "+ str(Message)
                    

        def Home_Screen(self):
            try:
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.flip()
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Home screen")
                if self.platform == "Linux":
                    Selector = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, (f"Resources//General_Resources//selectorICON{self.theme}.jpg"))).convert()
                else:
                    Selector = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, (f"Resources\\General_Resources\\selectorICON{self.theme}.jpg"))).convert()
                
                SelectorWidth = Selector.get_width()
                hover1 = False
                hover2 = False
                hover3 = False
                hover4 = False
                hover5 = False
                hover6 = False
                hover7 = False
                mousebuttondown = False
                
                PycraftTitle = self.TitleFont.render("Pycraft", self.aa, self.FontCol)
                TitleWidth = PycraftTitle.get_width()
                self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                self.Display.blit(PycraftTitle, ((self.realWidth-TitleWidth)/2, 0))
                self.mod_Pygame__.display.flip()

                if self.platform == "Linux":
                    SideFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 20) 
                    VersionFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 20) 
                    ButtonFont1 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30) 
                    ButtonFont2 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30) 
                    ButtonFont3 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30) 
                    ButtonFont4 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30) 
                    ButtonFont5 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)
                    ButtonFont6 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)
                    ButtonFont7 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 30)
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    MessageFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 20)
                else:
                    SideFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20) 
                    VersionFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20) 
                    ButtonFont1 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30) 
                    ButtonFont2 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30) 
                    ButtonFont3 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30) 
                    ButtonFont4 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30) 
                    ButtonFont5 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)
                    ButtonFont6 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)
                    ButtonFont7 = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 30)
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    MessageFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 20)
                oldTHEME = self.theme
                tempFPS = self.FPS
                coloursARRAY = []

                anim = False

                special = [30, 30, 30]
                TargetARRAY = []

                ColourDisplacement = 80

                increment = False
                
                Mx, My = self.realWidth/2, self.realHeight/2
                
                self.CurrentlyDisplayingMessage = False
                
                Outdated = self.Outdated
                
                self.MovementSpeed = 3
                                
                UpdateWholeDisplay = True
                
                self.Updated = True # cheese
                
                while True:
                    if self.GetOutdated == [True, False]:
                        self.GetOutdated = [True, True]
                        Outdated = self.Outdated
                        
                    if self.UseMouseInput == False:
                        Mx, My = Mx+self.JoystickMouse[0], My+self.JoystickMouse[1]
                        self.mod_Pygame__.mouse.set_pos(Mx, My)
                    else:
                        self.JoystickConfirm = False

                    if self.FancyGraphics == True:
                        coloursARRAY = []
                        if anim == True:
                            anim = False
                            TargetARRAY = []
                            for a in range(self.mod_Random__.randint(0, 32)):
                                TargetARRAY.append(a)
                                        
                        if len(TargetARRAY) == 0:
                            TargetARRAY = [33]
                        for i in range(32):
                            for j in range(len(TargetARRAY)):
                                if i == TargetARRAY[j]:
                                    coloursARRAY.append(special)
                                else:
                                    coloursARRAY.append(self.ShapeCol)

                        if increment == False:
                            if self.aFPS == 0 or self.Iteration == 0:
                                ColourDisplacement -= (self.mod_Random__.randint(0,10)/((self.FPS)/4))
                            else:
                                ColourDisplacement -= (self.mod_Random__.randint(0,10)/((self.aFPS/self.Iteration)/4))
                            special[0], special[1], special[2] = ColourDisplacement, ColourDisplacement, ColourDisplacement
                        if increment == True:
                            if self.aFPS == 0 or self.Iteration == 0:
                                ColourDisplacement += (self.mod_Random__.randint(0,10)/((self.FPS)/4))
                            else:
                                ColourDisplacement += (self.mod_Random__.randint(0,10)/((self.aFPS/self.Iteration)/4))
                            special[0], special[1], special[2] = ColourDisplacement, ColourDisplacement, ColourDisplacement
                        if special[0] <= 30:
                            increment = True
                            special[0], special[1], special[2] = 30, 30, 30
                        if special[0] >= 80:
                            increment = False
                            anim = True
                            special[0], special[1], special[2] = 80, 80, 80
                    else:
                        coloursARRAY = self.FancyGraphics

                    if self.mod_Pygame__.mixer.Channel(3).get_busy() == 1:
                        self.mod_Pygame__.mixer.Channel(3).stop()

                    if str(self.Display) == "<Surface(Dead Display)>":
                        if self.Fullscreen == False:
                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                        elif self.Fullscreen == True:
                            self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)

                    self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                    if not (self.realWidth == self.FullscreenX and self.realHeight == self.FullscreenY):
                        self.SavedWidth, self.SavedHeight = self.mod_Pygame__.display.get_window_size()

                    if self.SavedWidth == self.FullscreenX:
                        self.SavedWidth = 1280
                    if self.SavedHeight == self.FullscreenY:
                        self.SavedHeight = 720

                    if self.realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if self.realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)

                    yScaleFact = self.realHeight/720
                    xScaleFact = self.realWidth/1280
                    
                    if not oldTHEME == self.theme:
                        Selector = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, (f"Resources\\General_Resources\\selectorICON{self.theme}.jpg"))).convert()
                        SelectorWidth = Selector.get_width()
                        oldTHEME = self.theme

                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)

                    self.Display.fill(self.BackgroundCol)
                    self.Display.fill([255, 0, 0])
                    self.eFPS = self.clock.get_fps()
                    self.aFPS += self.eFPS
                    self.Iteration += 1
                    if self.UseMouseInput == True:
                        Mx, My = self.mod_Pygame__.mouse.get_pos() 
                    PycraftTitle = self.TitleFont.render("Pycraft", self.aa, self.FontCol)
                    TitleWidth = PycraftTitle.get_width()
                    TitleHeight = PycraftTitle.get_height()

                    Name = SideFont.render("By Tom Jebbo", self.aa, self.FontCol)
                    NameHeight = Name.get_height()

                    Version = VersionFont.render(f"Version: {self.version}", self.aa, self.FontCol) 
                    VersionWidth = Version.get_width()
                    VersionHeight = Version.get_height()

                    Play = ButtonFont1.render("Play", self.aa, self.FontCol)
                    PlayWidth = Play.get_width()

                    SettingsText = ButtonFont2.render("Settings", self.aa, self.FontCol)
                    SettingsWidth = SettingsText.get_width()

                    Character_DesignerText = ButtonFont3.render("Character Designer", self.aa, self.FontCol)
                    CharDesignerWidth = Character_DesignerText.get_width()

                    AchievementsText = ButtonFont4.render("Achievements", self.aa, self.FontCol)
                    AchievementsWidth = AchievementsText.get_width()

                    Credits_and_Change_Log_Text = ButtonFont5.render("Credits", self.aa, self.FontCol)
                    CreditsWidth = Credits_and_Change_Log_Text.get_width()

                    BenchmarkText = ButtonFont6.render("Benchmark", self.aa, self.FontCol)
                    BenchmarkWidth = BenchmarkText.get_width()
                    
                    InstallerText = ButtonFont7.render("Installer", self.aa, self.FontCol)
                    InstallerWidth = InstallerText.get_width()

                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "saveANDexit"
                        if event.type == self.mod_Pygame__.KEYDOWN: 
                            if event.key == self.mod_Pygame__.K_SPACE and self.Devmode < 10: 
                                self.Devmode += 1
                            if event.key == self.mod_Pygame__.K_q:
                                self.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(self)
                            if event.key == self.mod_Pygame__.K_F11:
                                UpdateWholeDisplay = True
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)
                            if event.key == self.mod_Pygame__.K_x:
                                self.Devmode = 1 
                        if event.type == self.mod_Pygame__.MOUSEBUTTONDOWN or self.mod_Pygame__.mouse.get_pressed()[0]:
                            mousebuttondown = True
                        else:
                            mousebuttondown = False
                        if event.type == self.mod_Pygame__.WINDOWSIZECHANGED or self.Project_Sleeping == True:
                            UpdateWholeDisplay = True

                    if self.UseMouseInput == False:
                        if self.JoystickExit == True:
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "saveANDexit"
                        
                        if self.JoystickConfirm == True:
                            mousebuttondown = True
                            self.JoystickConfirm = False
                            
                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Home screen")
                    
                    ButtonFont1.set_underline(hover1) 
                    ButtonFont2.set_underline(hover2) 
                    ButtonFont3.set_underline(hover3)
                    ButtonFont4.set_underline(hover4)
                    ButtonFont5.set_underline(hover5)
                    ButtonFont6.set_underline(hover6)
                    ButtonFont7.set_underline(hover7)
                    
                    if My >= 202*yScaleFact and My <= 247*yScaleFact and Mx >= (self.realWidth-(PlayWidth+SelectorWidth))-2:
                        hover1 = True
                        if mousebuttondown == True:
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Play"
                    else:
                        hover1 = False

                    if My >= 252*yScaleFact and My <= 297*yScaleFact and Mx >= (self.realWidth-(SettingsWidth+SelectorWidth))-2: 
                        hover2 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Settings"
                    else:
                        hover2 = False

                    if My >= 302*yScaleFact and My <= 347*yScaleFact and Mx >= (self.realWidth-(CharDesignerWidth+SelectorWidth)-2):
                        hover3 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "CharacterDesigner"
                    else:
                        hover3 = False

                    if My >= 402*yScaleFact and My <= 447*yScaleFact and Mx >= (self.realWidth-(AchievementsWidth+SelectorWidth)-2):
                        hover4 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Achievements"
                    else:
                        hover4 = False

                    if My >= 352*yScaleFact and My <= 397*yScaleFact and Mx >= (self.realWidth-(CreditsWidth+SelectorWidth)-2):
                        hover5 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Credits"
                    else:
                        hover5 = False

                    if My >= 452*yScaleFact and My <= 497*yScaleFact and Mx >= (self.realWidth-(BenchmarkWidth+SelectorWidth)-2):
                        hover6 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Benchmark"
                    else:
                        hover6 = False
                        
                    if My >= 502*yScaleFact and My <= 547*yScaleFact and Mx >= (self.realWidth-(InstallerWidth+SelectorWidth))-2:
                        hover7 = True
                        if mousebuttondown == True:
                            self.Display.fill(self.BackgroundCol)
                            self.mod_Pygame__.display.flip()
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return "Installer"
                    else:
                        hover7 = False

                    self.Display.fill(self.BackgroundCol)
                    
                    if self.CurrentlyDisplayingMessage == False:
                        if self.FromPlay == True:
                            self.FromPlay = False
                            self.CurrentlyDisplayingMessage = True
                            MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, "Loading", self.AccentCol,))
                            MessageThread.start()
                        else:
                            if self.Updated == True:
                                self.Updated = False
                                self.CurrentlyDisplayingMessage = True
                                MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, f"Successfully updated Pycraft to v{self.version}", (0, 255, 0),))
                                MessageThread.start()
                            else:
                                if Outdated == True and self.TotalNumUpdate >= 2:
                                    Outdated = False
                                    self.CurrentlyDisplayingMessage = True
                                    MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, f"There are {self.TotalNumUpdate} updates available!", (0, 255, 0),))
                                    MessageThread.start()
                                elif Outdated == True and self.TotalNumUpdate == 1:
                                    Outdated = False
                                    self.CurrentlyDisplayingMessage = True
                                    MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, "There is an update available!", (0, 255, 0),))
                                else:
                                    if self.DeviceConnected_Update == True:
                                        self.CurrentlyDisplayingMessage = True
                                        if self.DeviceConnected == True:
                                            MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, "There is a new input device available! You can change input modes in settings", (0, 255, 0),))
                                        else:
                                            if self.UseMouseInput == True:
                                                MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, "Terminated connection to an input device", self.FontCol,))
                                            else:
                                                MessageThread = self.mod_Threading__.Thread(target=self.mod_HomeScreen__.GenerateHomeScreen.DisplayMessage, args=(self, MessageFont, "Terminated connection to current input device, returning to default setting", (255, 0, 0),))
                                                self.UseMouseInput = False
                                        MessageThread.start()
                                        self.DeviceConnected_Update = False
                        
                        
                    self.Display.blit(PycraftTitle, ((self.realWidth-TitleWidth)/2, 0))

                    self.Display.blit(Name, (0, (self.realHeight-NameHeight)))
                    self.Display.blit(Version, ((self.realWidth-VersionWidth)-2, (self.realHeight-VersionHeight)))

                    self.Display.blit(Play, ((self.realWidth-PlayWidth)-2, 200*yScaleFact))
                    self.Display.blit(SettingsText, ((self.realWidth-SettingsWidth)-2, 250*yScaleFact))
                    self.Display.blit(Character_DesignerText, ((self.realWidth-CharDesignerWidth)-2, 300*yScaleFact))
                    self.Display.blit(Credits_and_Change_Log_Text, ((self.realWidth-CreditsWidth)-2, 350*yScaleFact))
                    self.Display.blit(AchievementsText, ((self.realWidth-AchievementsWidth)-2, 400*yScaleFact))
                    self.Display.blit(BenchmarkText, ((self.realWidth-BenchmarkWidth)-2, 450*yScaleFact))
                    self.Display.blit(InstallerText, ((self.realWidth-InstallerWidth)-2, 500*yScaleFact))

                    if hover1 == True:
                        self.Display.blit(Selector, (self.realWidth-(PlayWidth+SelectorWidth)-2, 200*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover2 == True:
                        self.Display.blit(Selector, (self.realWidth-(SettingsWidth+SelectorWidth)-2, 250*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover3 == True:
                        self.Display.blit(Selector, (self.realWidth-(CharDesignerWidth+SelectorWidth)-2, 300*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover5 == True:
                        self.Display.blit(Selector, (self.realWidth-(CreditsWidth+SelectorWidth)-2, 350*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover4 == True:
                        self.Display.blit(Selector, (self.realWidth-(AchievementsWidth+SelectorWidth)-2, 400*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover6 == True:
                        self.Display.blit(Selector, (self.realWidth-(BenchmarkWidth+SelectorWidth)-2, 450*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    elif hover7 == True:
                        self.Display.blit(Selector, (self.realWidth-(InstallerWidth+SelectorWidth)-2, 500*yScaleFact))
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                    else:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_ARROW)

                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(self, DataFont)

                    self.mod_DrawingUtils__.DrawRose.CreateRose(self, xScaleFact, yScaleFact, coloursARRAY)
                    
                    if UpdateWholeDisplay == True:
                        self.mod_Pygame__.display.flip()
                        UpdateWholeDisplay = False
                    else:
                        self.mod_Pygame__.display.update(0, 0, self.realWidth, self.realHeight-40)

                    self.clock.tick(tempFPS)
                    
                    if not self.ErrorMessage == None:
                        self.ErrorMessage = "HomeScreen: "+str(self.ErrorMessage)
                        return

            except Exception as Message:
                self.ErrorMessage = "HomeScreen > GenerateHomeScreen > Home_Screen: "+ str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()
