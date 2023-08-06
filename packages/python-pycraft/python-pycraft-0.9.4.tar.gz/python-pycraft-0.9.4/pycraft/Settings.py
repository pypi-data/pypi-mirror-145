if not __name__ == "__main__":
    print("Started <Pycraft_Settings>")
    class GenerateSettings:
        def __init__(self):
            pass

        def settings(self):
            try:
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.flip()
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Settings")
                if self.platform == "Linux":
                    VersionFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    InfoTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)
                    LOWFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    MEDIUMFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    HIGHFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    ADAPTIVEFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    LightThemeFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    DarkThemeFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    SettingsInformationFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                else:
                    VersionFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    InfoTitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                    LOWFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    MEDIUMFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    HIGHFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    ADAPTIVEFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    LightThemeFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    DarkThemeFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    DataFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    SettingsInformationFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)

                TempMx = 0
                
                Mx, My = self.realWidth/2, self.realHeight/2
                mousebuttondown = False

                scroll = 50
                
                FocusedOn = [False, None]
                MoveToPosition = [False, False, False, False, False]
                ChangeLine = []
                self.MovementSpeed = 1
                while True:
                    TempMx = Mx
                    if self.UseMouseInput == False:
                        Mx, My = Mx+self.JoystickMouse[0], My+self.JoystickMouse[1]
                        self.mod_Pygame__.mouse.set_pos(Mx, My)
                    else:
                        self.JoystickConfirm = False
                        
                    realWidth, realHeight = self.mod_Pygame__.display.get_window_size()

                    if realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)

                    xScaleFact = realWidth/1280

                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)
                    self.Iteration += 1
                    if self.UseMouseInput == True:
                        Mx, My = self.mod_Pygame__.mouse.get_pos()
                        
                    self.eFPS = self.clock.get_fps()
                    self.aFPS += self.eFPS
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                        elif event.type == self.mod_Pygame__.KEYDOWN:
                            if event.key == self.mod_Pygame__.K_SPACE and self.Devmode < 10:
                                self.Devmode += 1
                            if event.key == self.mod_Pygame__.K_x:
                                self.Devmode = 1
                            if event.key == self.mod_Pygame__.K_q:
                                self.mod_TkinterUtils__.TkinterInfo.CreateTkinterWindow(self)
                            if event.key == self.mod_Pygame__.K_F11:
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)
                            if event.key == self.mod_Pygame__.K_x: 
                                self.Devmode = 1 
                        elif event.type == self.mod_Pygame__.MOUSEBUTTONDOWN or self.mod_Pygame__.mouse.get_pressed()[0] == True: 
                            mousebuttondown = True
                        elif event.type == self.mod_Pygame__.MOUSEBUTTONUP or self.mod_Pygame__.mouse.get_pressed()[0] == False: 
                            mousebuttondown = False
                        if event.type == self.mod_Pygame__.MOUSEWHEEL and realHeight <= 760:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_SIZENS)
                            if str(event.y)[0] == "-":
                                scroll -= 5
                            else:
                                scroll += 5
                        else:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_ARROW)

                    self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Settings")

                    if scroll > 35:
                        scroll = 35
                    elif scroll < -40:
                        scroll = -40

                    if self.UseMouseInput == False:
                        if self.JoystickExit == True:
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                        
                        if self.JoystickConfirm == True:
                            mousebuttondown = True
                            self.JoystickConfirm = False
                        else:
                            if self.JoystickConfirm_toggle == False:
                                mousebuttondown = False
                    titletFont = self.TitleFont.render("Pycraft", self.aa, self.FontCol)
                    TitleWidth = titletFont.get_width()

                    InfoFont = InfoTitleFont.render("Settings", self.aa, self.SecondFontCol)

                    FPSFont = VersionFont.render(f"FPS: Actual: {int(self.eFPS)} Max: {int(self.FPS)} Average: {int((self.aFPS/self.Iteration))}", self.aa, self.FontCol)
                    FOVFont = VersionFont.render(f"FOV: {self.FOV}", self.aa, self.FontCol)
                    CamRotFont = VersionFont.render(f"Camera Rotation Speed: {round(self.cameraANGspeed, 1)}", self.aa, self.FontCol) 
                    ModeFont = VersionFont.render("Mode;         ,                 ,            ,          .", self.aa, self.FontCol) 
                    AAFont = VersionFont.render(f"Anti-Aliasing: {self.aa}", self.aa, self.FontCol) 
                    RenderFogFont = VersionFont.render(f"Render Fog: {self.RenderFOG}", self.aa, self.FontCol)
                    FancySkyFont = VersionFont.render(f"Fancy Graphics: {self.FancyGraphics}", self.aa, self.FontCol)
                    FancyParticleFont = VersionFont.render(f"Fancy Partices: {self.FanPart}", self.aa, self.FontCol)
                    SoundFont = VersionFont.render(f"Sound: {self.sound}", self.aa, self.FontCol)
                    if self.sound == True:
                        SoundVoltFont = VersionFont.render(f"Sound Volume: {self.soundVOL}%", self.aa, self.FontCol)
                    else:
                        SoundVoltFont = VersionFont.render(f"Sound Volume: {self.soundVOL}%", self.aa, self.ShapeCol)
                    MusicFont = VersionFont.render(f"Music: {self.music}", self.aa, self.FontCol)
                    if self.music == True:
                        MusicVoltFont = VersionFont.render(f"Music Volume: {self.musicVOL}%", self.aa, self.FontCol)
                    else:
                        MusicVoltFont = VersionFont.render(f"Music Volume: {self.musicVOL}%", self.aa, self.ShapeCol)
                    ThemeFont = VersionFont.render(f"Theme:          ,          | Current Theme: {self.theme}", self.aa, self.FontCol)
                    ToggleControllerSupportFont = VersionFont.render(f"Enable controller support: {not self.UseMouseInput}", self.aa, self.FontCol)
                    ThemeInformationFont = SettingsInformationFont.render("Gives you control over which theme you can use", self.aa, self.AccentCol)
                    ModeInformationFont = SettingsInformationFont.render("Gives you 4 separate pre-sets for settings, Adaptive mode will automatically adjust your settings", self.aa, self.AccentCol)
                    FPSInformationFont = SettingsInformationFont.render("Controls the maximum frame rate the game will limit to, does not guarantee that FPS unfortunately", self.aa, self.AccentCol)
                    FOVInformationFont = SettingsInformationFont.render("Controls the FOV of the camera in-game", self.aa, self.AccentCol)
                    CameraRotationSpeedInformationFont = SettingsInformationFont.render("Controls the rotation speed of the camera in-game (1 is low, 5 is high)", self.aa, self.AccentCol)
                    AAInformationFont = SettingsInformationFont.render("Enables/Disables anti-aliasing in game and in the GUI, will give you a minor performance improvement, mainly for low powered devices", self.aa, self.AccentCol)
                    RenderFogInformationFont = SettingsInformationFont.render("Enables/Disables fog effects in game, for a small performance benefit", self.aa, self.AccentCol)
                    FancyGraphicsInformationFont = SettingsInformationFont.render("Enables/Disables some graphical features, this can result in better performace when turned off", self.aa, self.AccentCol)
                    FancyParticlesInformationFont = SettingsInformationFont.render("Enables/Disables particles in game as particles can have a significant performance decrease", self.aa, self.AccentCol)
                    SoundInformationFont = SettingsInformationFont.render("Enables/Disables sound effects in game, like for example the click sound and footsteps in game", self.aa, self.AccentCol)
                    SoundVolInformationFont = SettingsInformationFont.render("Controls the volume of the sound effects, where 100% is maximum and 0% is minimum volume", self.aa, self.AccentCol)
                    MusicInformationFont = SettingsInformationFont.render("Enables/Disables music in game, like for example the GUI music", self.aa, self.AccentCol)
                    MusicVolInformationFont = SettingsInformationFont.render("Controls the volume of the music, some effects may not apply until the game reloads", self.aa, self.AccentCol)
                    ToggleControllerSupportInformationFont = SettingsInformationFont.render("Toggles the use of either keyboard and mouse or a controller to control the mouse and interact with the GUI", self.aa, self.AccentCol)
                    
                    self.Display.fill(self.BackgroundCol)
                    
                    FPS_rect = self.mod_Pygame__.Rect(50, 180+scroll, 450*xScaleFact, 10)
                    FOV_rect = self.mod_Pygame__.Rect(50, 230+scroll, 450*xScaleFact, 10)
                    CAM_rect = self.mod_Pygame__.Rect(50, 280+scroll, 450*xScaleFact, 10)
                    sound_rect = self.mod_Pygame__.Rect(50, 580+scroll, 450*xScaleFact, 10)
                    music_rect = self.mod_Pygame__.Rect(50, 680+scroll, 450*xScaleFact, 10)
                    aa_rect = self.mod_Pygame__.Rect(50, 330+scroll, 50, 10)
                    RenderFOG_Rect = self.mod_Pygame__.Rect(50, 380+scroll, 50, 10)
                    Fansky_Rect = self.mod_Pygame__.Rect(50, 430+scroll, 50, 10)
                    FanPart_Rect = self.mod_Pygame__.Rect(50, 480+scroll, 50, 10)
                    sound_Rect = self.mod_Pygame__.Rect(50, 530+scroll, 50, 10)
                    music_Rect = self.mod_Pygame__.Rect(50, 630+scroll, 50, 10)
                    Controller_Rect = self.mod_Pygame__.Rect(50, 730+scroll, 50, 10)
                    slider_Rect = self.mod_Pygame__.Rect(realWidth-15, scroll, 10, 665)
                    
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, FPS_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, FOV_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, CAM_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, sound_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, music_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, aa_rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, RenderFOG_Rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, Fansky_Rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, FanPart_Rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, sound_Rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, music_Rect, 0)
                    self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, Controller_Rect, 0)
                    
                    if mousebuttondown == True:
                        if (My > 180+scroll and My < 190+scroll) or (FocusedOn[0] == True and FocusedOn[1] == "FPS"):
                            FocusedOn = [True, "FPS"]
                            My = 185+scroll
                        else:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (int(self.FPS+45)*xScaleFact, 185+scroll), 9)

                        if (My > 230+scroll and My < 240+scroll) or (FocusedOn[0] == True and FocusedOn[1] == "FOV"):
                            FocusedOn = [True, "FOV"]
                            My = 235+scroll
                        else:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (int(self.FOV*5)*xScaleFact, 235+scroll), 9)

                        if (My > 280+scroll and My < 290+scroll) or (FocusedOn[0] == True and FocusedOn[1] == "CAS"):
                            FocusedOn = [True, "CAS"] # CAS = Camera Angle Speed
                            My = 285+scroll
                        else:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.cameraANGspeed*89)+45)*xScaleFact, 285+scroll), 9)

                        if (My > 580+scroll and My < 590+scroll and self.sound == True) or (FocusedOn[0] == True and FocusedOn[1] == "SVL"):
                            FocusedOn = [True, "SVL"]
                            My = 585+scroll
                        else:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.soundVOL*4.4)+50)*xScaleFact, 585+scroll), 9)

                        if (My > 680+scroll and My < 690+scroll and self.music == True) or (FocusedOn[0] == True and FocusedOn[1] == "MVL"): 
                            FocusedOn = [True, "MVL"]
                            My = 685+scroll
                        else:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.musicVOL*4.4)+50)*xScaleFact, 685+scroll), 9)

                        if My > 330+scroll and My < 340+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.aa == True: 
                                self.aa = False 
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.aa == False: 
                                self.aa = True 
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.aa == True: 
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 335+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 335+scroll), 6)
                        elif self.aa == False: 
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 335+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 335+scroll), 6)

                        if My > 380+scroll and My < 390+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.RenderFOG == True:
                                self.RenderFOG = False
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.RenderFOG == False:
                                self.RenderFOG = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.RenderFOG == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 385+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 385+scroll), 6)
                        elif self.RenderFOG == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 385+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 385+scroll), 6)

                        if My > 430+scroll and My < 440+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.FancyGraphics == True:
                                self.FancyGraphics = False
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.FancyGraphics == False:
                                self.FancyGraphics = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.FancyGraphics == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 435+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 435+scroll), 6)
                        elif self.FancyGraphics == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 435+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 435+scroll), 6)

                        if My > 480+scroll and My < 490+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.FanPart == True:
                                self.FanPart = False
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.FanPart == False:
                                self.FanPart = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.FanPart == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 485+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 485+scroll), 6)
                        elif self.FanPart == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 485+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 485+scroll), 6)

                        if My > 530+scroll and My < 540+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.sound == True:
                                self.sound = False
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.sound == False:
                                self.sound = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.sound == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 535+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 535+scroll), 6)
                        elif self.sound == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 535+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 535+scroll), 6)

                        if My > 630+scroll and My < 640+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.music == True:
                                self.music = False
                                self.mod_Pygame__.mixer.music.fadeout(500)
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.music == False:
                                self.music = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if self.music == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 635+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 635+scroll), 6)
                        elif self.music == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 635+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 635+scroll), 6)
                            
                        if My > 730+scroll and My < 740+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.UseMouseInput == True:
                                self.UseMouseInput = False
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                            elif self.UseMouseInput == False:
                                self.UseMouseInput = True
                                if self.sound == True:
                                    self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                                mousebuttondown = False
                        if not self.UseMouseInput == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 735+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 735+scroll), 6)
                        elif not self.UseMouseInput == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 735+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 735+scroll), 6)
                    else:
                        FocusedOn = [False, None]
                        self.mod_Pygame__.mouse.set_visible(True)
                        self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.soundVOL*4.4)+50)*xScaleFact, 585+scroll), 9)
                        self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.FPS+45)*xScaleFact), 185+scroll), 9)
                        self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.cameraANGspeed*89)+45)*xScaleFact, 285+scroll), 9)
                        self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.FOV*5))*xScaleFact, 235+scroll), 9)
                        self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), ((int(self.musicVOL*4.4)+50)*xScaleFact, 685+scroll), 9)

                        if self.aa == True: 
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 335+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 335+scroll), 6)
                        elif self.aa == False: 
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 335+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 335+scroll), 6)

                        if self.RenderFOG == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 385+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 385+scroll), 6)
                        elif self.RenderFOG == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 385+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 385+scroll), 6)

                        if self.FancyGraphics == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 435+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 435+scroll), 6)
                        elif self.FancyGraphics == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 435+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 435+scroll), 6)

                        if self.FanPart == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 485+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 485+scroll), 6)
                        elif self.FanPart == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 485+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 485+scroll), 6)

                        if self.sound == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 535+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 535+scroll), 6)
                        elif self.sound == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 535+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 535+scroll), 6)

                        if self.music == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 635+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 635+scroll), 6)
                        elif self.music == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 635+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 635+scroll), 6)
                            
                        if not self.UseMouseInput == True:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 735+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 735+scroll), 6)
                        elif not self.UseMouseInput == False:
                            self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 735+scroll), 9)
                            self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 735+scroll), 6)

                        if My > 330+scroll and My < 340+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            self.Display.blit(AAInformationFont, (120, 325+scroll))
                            if self.aa == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 335+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 335+scroll), 6)
                            elif self.aa == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 335+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 335+scroll), 6)

                        if My > 380+scroll and My < 390+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            self.Display.blit(RenderFogInformationFont, (120, 375+scroll))
                            if self.RenderFOG == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 385+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 385+scroll), 6)
                            elif self.RenderFOG == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 385+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 385+scroll), 6)

                        if My > 430+scroll and My < 440+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            self.Display.blit(FancyGraphicsInformationFont, (120, 425+scroll))
                            if self.FancyGraphics == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 435+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 435+scroll), 6)
                            elif self.FancyGraphics == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 435+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 435+scroll), 6)

                        if My > 480+scroll and My < 490+scroll:
                            self.Display.blit(FancyParticlesInformationFont, (120, 475+scroll))
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.FanPart == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 485+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 485+scroll), 6)
                            elif self.FanPart == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 485+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 485+scroll), 6)

                        if My > 530+scroll and My < 540+scroll:
                            self.Display.blit(SoundInformationFont, (120, 525+scroll))
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            if self.sound == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 535+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 535+scroll), 6)
                            elif self.sound == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 535+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 535+scroll), 6)

                        if My > 630+scroll and My < 640+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            self.Display.blit(MusicInformationFont, (120, 625+scroll))
                            if self.music == True:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (90, 635+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 635+scroll), 6)
                            elif self.music == False:
                                self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (60, 635+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 635+scroll), 6)
                                
                        if My > 730+scroll and My < 740+scroll:
                            self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                            self.Display.blit(ToggleControllerSupportInformationFont, (120, 725+scroll))
                            if not self.UseMouseInput == True:
                                self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (90, 735+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (90, 735+scroll), 6)
                            elif not self.UseMouseInput == False:
                                self.mod_Pygame__.draw.circle(self.Display, (255, 255, 255), (60, 735+scroll), 9)
                                self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (60, 735+scroll), 6)

                    if My >= 65+scroll and My <= 75+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(ThemeInformationFont, (300, 67+scroll))

                    if My >= 65+scroll and My <= 75+scroll and Mx >= 55 and Mx <= 95:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        LightTheme = LightThemeFont.render("Light", self.aa, self.AccentCol)
                        LightThemeFont.set_underline(True)
                        if mousebuttondown == True:
                            self.theme = "light"
                            self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            mousebuttondown = False
                    else:
                        LightTheme = LightThemeFont.render("Light", self.aa, self.FontCol)
                        LightThemeFont.set_underline(False)

                    if My >= 65+scroll and My <= 75+scroll and Mx >= 95 and Mx <= 135:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        DarkTheme = DarkThemeFont.render("Dark", self.aa, self.AccentCol)
                        DarkThemeFont.set_underline(True)
                        if mousebuttondown == True:
                            self.theme = "dark"
                            self.mod_ThemeUtils__.DetermineThemeColours.GetColours(self)
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            mousebuttondown = False
                    else:
                        DarkTheme = DarkThemeFont.render("Dark", self.aa, self.FontCol)
                        DarkThemeFont.set_underline(False)

                    if My >= 85+scroll and My <= 95+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(ModeInformationFont, (300, 85+scroll))

                    if My > 680+scroll and My < 690+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(MusicVolInformationFont, (520*xScaleFact, 675+scroll))

                    if My > 580+scroll and My < 590+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(SoundVolInformationFont, (520*xScaleFact, 575+scroll))

                    if My > 280+scroll and My < 290+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(CameraRotationSpeedInformationFont, (520*xScaleFact, 275+scroll))

                    if My > 230+scroll and My < 240+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(FOVInformationFont, (520*xScaleFact, 225+scroll))

                    if My > 180+scroll and My < 190+scroll:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        self.Display.blit(FPSInformationFont, (520*xScaleFact, 175+scroll))

                    if My >= 85+scroll and My <= 95+scroll and Mx >= 40 and Mx <= 80:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        LOWtFont = LOWFont.render("Low", self.aa, self.AccentCol)
                        LOWFont.set_underline(True)
                        if mousebuttondown == True:
                            self.SettingsPreference = "Low"
                            self.FPS = 15
                            self.aa = False
                            self.RenderFOG = False
                            self.FancyGraphics = False
                            self.FanPart = False
                            mousebuttondown = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                    else:
                        LOWtFont = LOWFont.render("Low", self.aa, self.FontCol)
                        LOWFont.set_underline(False)

                    if My >= 85+scroll and My <= 95+scroll and Mx >= 90 and Mx <= 155:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        MEDIUMtFont = MEDIUMFont.render("Medium", self.aa, self.AccentCol)
                        MEDIUMFont.set_underline(True)
                        if mousebuttondown == True:
                            self.SettingsPreference = "Medium"
                            self.FPS = 30
                            self.aa = True
                            self.RenderFOG = False
                            self.FancyGraphics = True
                            self.FanPart = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            mousebuttondown = False
                    else:
                        MEDIUMtFont = MEDIUMFont.render("Medium", self.aa, self.FontCol)
                        MEDIUMFont.set_underline(False)

                    if My >= 85+scroll and My <= 95+scroll and Mx >= 165 and Mx <= 205:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        HIGHFontText = HIGHFont.render("High", self.aa, self.AccentCol)
                        HIGHFont.set_underline(True)
                        if mousebuttondown == True:
                            self.SettingsPreference = "High"
                            self.FPS = 60
                            self.aa = True
                            self.RenderFOG = True
                            self.FancyGraphics = True
                            self.FanPart = True
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            mousebuttondown = False
                    else:
                        HIGHFontText = HIGHFont.render("High", self.aa, self.FontCol)
                        HIGHFont.set_underline(False)

                    if My >= 85+scroll and My <= 95+scroll and Mx >= 215 and Mx <= 300:
                        self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_HAND)
                        ADAPTIVEtFont = ADAPTIVEFont.render("Adaptive", self.aa, self.AccentCol)
                        ADAPTIVEFont.set_underline(True)
                        if mousebuttondown == True:
                            self.SettingsPreference = "Adaptive"
                            self.FPS = (self.mod_Psutil__.cpu_freq(percpu=True)[0][2])/35
                            if (self.mod_Psutil__.cpu_freq(percpu=True)[0][2])/10 > 300 and self.mod_Psutil__.virtual_memory().total > 8589934592:
                                self.aa = True
                                self.RenderFog = True
                                self.FancyGraphics = True
                                self.FanPart = True
                            elif (self.mod_Psutil__.cpu_freq(percpu=True)[0][2]) > 200 and self.mod_Psutil__.virtual_memory().total > 4294967296:
                                self.aa = True
                                self.RenderFog = True
                                self.FancyGraphics = True
                                self.FanPart = False
                            elif (self.mod_Psutil__.cpu_freq(percpu=True)[0][2]) > 100 and self.mod_Psutil__.virtual_memory().total > 2147483648:
                                self.aa = False
                                self.RenderFog = False
                                self.FancyGraphics = True
                                self.FanPart = False
                            elif (self.mod_Psutil__.cpu.freq(percpu=True)[0][2]) < 100 and (self.mod_Psutil__.cpu.freq(percpu=True)[0][2]) > 75 and self.mod_Psutil__.virtual_memory().total > 1073741824:
                                self.aa = False
                                self.RenderFog = False
                                self.FancyGraphics = False
                                self.FanPart = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            mousebuttondown = False
                    else:
                        ADAPTIVEtFont = ADAPTIVEFont.render("Adaptive", self.aa, self.FontCol)
                        ADAPTIVEFont.set_underline(False)


                    if (FocusedOn[0] == True and FocusedOn[1] == "FPS"):
                        self.mod_Pygame__.mouse.set_visible(False)
                        if Mx > TempMx and self.FPS < 445:
                            self.FPS += 1
                        elif Mx < TempMx and self.FPS > 15:
                            self.FPS -= 1
                        if self.FPS < 15:
                            self.FPS = 16
                        elif self.FPS > 445:
                            self.FPS = 444
                        if self.FancyGraphics == True:
                            ChangeLine.append((int(self.FPS+45)*xScaleFact, 185+scroll))
                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(self.Display, self.AccentCol, False, ChangeLine)
                        self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (int(self.FPS+45)*xScaleFact, 185+scroll), 9)
                        MoveToPosition[0] = True
                    else:
                        if MoveToPosition[0] == True:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos((int(self.FPS+45)*xScaleFact), 185+scroll)
                            MoveToPosition[0] = False
                            
                    if (FocusedOn[0] == True and FocusedOn[1] == "FOV"):
                        self.mod_Pygame__.mouse.set_visible(False)
                        if Mx > TempMx and self.FOV < 98:
                            self.FOV += 1
                        elif Mx < TempMx and self.FOV > 12:
                            self.FOV -= 1
                        if self.FOV < 12:
                            self.FOV = 13
                        elif self.FOV > 98:
                            self.FOV = 97
                        if self.FancyGraphics == True:
                            ChangeLine.append((int(self.FOV*5)*xScaleFact, 235+scroll))
                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(self.Display, self.AccentCol, False, ChangeLine)
                        self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, (int(self.FOV*5)*xScaleFact, 235+scroll), 9)
                        MoveToPosition[1] = True
                    else:
                        if MoveToPosition[1] == True:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos((int(self.FOV*5)*xScaleFact), 235+scroll)
                            MoveToPosition[1] = False
                        
                    if (FocusedOn[0] == True and FocusedOn[1] == "CAS"):
                        self.mod_Pygame__.mouse.set_visible(False)
                        if Mx > TempMx and self.cameraANGspeed < 5.0:
                            self.cameraANGspeed += 0.1
                        elif Mx < TempMx and self.cameraANGspeed > 0.0:
                            self.cameraANGspeed -= 0.1
                        if self.cameraANGspeed > 5.0:
                            self.cameraANGspeed = 4.9
                        elif self.cameraANGspeed <= 0:
                            self.cameraANGspeed = 0.1
                        if self.FancyGraphics == True:
                            ChangeLine.append(((int(self.cameraANGspeed*89)+45)*xScaleFact, 285+scroll))
                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(self.Display, self.AccentCol, False, ChangeLine)
                        self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, ((int(self.cameraANGspeed*89)+45)*xScaleFact, 285+scroll), 9)
                        MoveToPosition[2] = True
                    else:
                        if MoveToPosition[2] == True:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(((int(self.cameraANGspeed*89)+45)*xScaleFact), 285+scroll)
                            MoveToPosition[2] = False
                            
                    if (FocusedOn[0] == True and FocusedOn[1] == "SVL"):
                        self.mod_Pygame__.mouse.set_visible(False)
                        if Mx > TempMx and self.soundVOL < 100:
                            self.soundVOL += 1
                        elif Mx < TempMx and self.soundVOL > 0:
                            self.soundVOL -= 1
                        if self.soundVOL > 100:
                            self.soundVOL = 100
                        elif self.soundVOL < 0:
                            self.soundVOL = 0
                        if self.FancyGraphics == True:
                            ChangeLine.append(((int(self.soundVOL*4.4)+50)*xScaleFact, 585+scroll))
                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(self.Display, self.AccentCol, False, ChangeLine)
                        self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, ((int(self.soundVOL*4.4)+50)*xScaleFact, 585+scroll), 9)
                        MoveToPosition[3] = True
                    else:
                        if MoveToPosition[3] == True:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(((int(self.soundVOL*4.4)+50)*xScaleFact), 585+scroll)
                            MoveToPosition[3] = False
                            
                            
                    if (FocusedOn[0] == True and FocusedOn[1] == "MVL"):
                        self.mod_Pygame__.mouse.set_visible(False)
                        if Mx > TempMx and self.musicVOL < 100:
                            self.musicVOL += 1
                        elif Mx < TempMx and self.musicVOL > 0:
                            self.musicVOL -= 1
                        if self.musicVOL > 100:
                            self.musicVOL = 100
                        elif self.musicVOL < 0:
                            self.musicVOL = 0
                        if self.FancyGraphics == True:
                            ChangeLine.append(((int(self.musicVOL*4.4)+50)*xScaleFact, 685+scroll))
                            if len(ChangeLine) >= 2:
                                self.mod_Pygame__.draw.lines(self.Display, self.AccentCol, False, ChangeLine)
                        self.mod_Pygame__.draw.circle(self.Display, self.AccentCol, ((int(self.musicVOL*4.4)+50)*xScaleFact, 685+scroll), 9)
                        MoveToPosition[4] = True
                    else:
                        if MoveToPosition[4] == True:
                            ChangeLine = []
                            self.mod_Pygame__.mouse.set_pos(((int(self.musicVOL*4.4)+50)*xScaleFact), 685+scroll)
                            MoveToPosition[4] = False
                            
                            
                    self.Display.blit(FPSFont, (0, 150+scroll))
                    self.Display.blit(FOVFont, (0, 200+scroll))
                    self.Display.blit(CamRotFont, (0, 250+scroll))
                    self.Display.blit(ModeFont, (0, 85+scroll)) 
                    self.Display.blit(LOWtFont, (48, 85+scroll))
                    self.Display.blit(MEDIUMtFont, (90, 85+scroll))
                    self.Display.blit(HIGHFontText, (165, 85+scroll))
                    self.Display.blit(ADAPTIVEtFont, (215, 85+scroll)) 
                    self.Display.blit(AAFont, (0, 300+scroll))
                    self.Display.blit(RenderFogFont, (0, 350+scroll))
                    self.Display.blit(FancySkyFont, (0, 400+scroll))
                    self.Display.blit(FancyParticleFont, (0, 450+scroll))
                    self.Display.blit(SoundFont, (0, 500+scroll))
                    self.Display.blit(SoundVoltFont, (0, 550+scroll))
                    self.Display.blit(MusicFont, (0, 600+scroll))
                    self.Display.blit(MusicVoltFont, (0, 650+scroll))
                    self.Display.blit(ToggleControllerSupportFont, (0, 700+scroll))
                    self.Display.blit(ThemeFont, (0, 65+scroll))
                    self.Display.blit(LightTheme, (55, 65+scroll))
                    self.Display.blit(DarkTheme, (95, 65+scroll))
                    self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (int(self.FPS+45)*xScaleFact, 185+scroll), 6)
                    self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, (int(self.FOV*5)*xScaleFact, 235+scroll), 6)
                    self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, ((int(self.cameraANGspeed*89)+45)*xScaleFact, 285+scroll), 6)
                    self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, ((int(self.soundVOL*4.4)+50)*xScaleFact, 585+scroll), 6)
                    self.mod_Pygame__.draw.circle(self.Display, self.ShapeCol, ((int(self.musicVOL*4.4)+50)*xScaleFact, 685+scroll), 6)
                    
                    cover_Rect = self.mod_Pygame__.Rect(0, 0, 1280, 100)
                    self.mod_Pygame__.draw.rect(self.Display, (self.BackgroundCol), cover_Rect)
                    self.Display.blit(titletFont, ((realWidth-TitleWidth)/2, 0))
                    self.Display.blit(InfoFont, (((realWidth-TitleWidth)/2)+55, 50))


                    if realHeight <= 760:
                        self.mod_Pygame__.draw.rect(self.Display, self.ShapeCol, slider_Rect, 0)
                    else:
                        scroll = 50

                    self.mod_DrawingUtils__.GenerateGraph.CreateDevmodeGraph(self, DataFont)

                    self.mod_Pygame__.display.flip() 
                    self.clock.tick(tempFPS)
                    
                    if not self.ErrorMessage == None:
                        self.ErrorMessage = "Settings > GenerateSettings > settings: "+str(self.ErrorMessage)
                        return
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                self.ErrorMessage = "Settings > GenerateSettings > settings: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()