if not __name__ == "_main_":
    print("Started <Pycraft_StartupAnimation>")
    class GenerateStartupScreen:
        def _init_(self):
            pass

        def Start(self):
            try:
                if self.platform == "Linux":
                    PresentsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)
                    PycraftFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 60)
                    NameFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 45)
                else:
                    PresentsFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                    PycraftFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)
                    NameFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 45)

                NameText = NameFont.render("Tom Jebbo", True, self.FontCol)
                NameTextWidth = NameText.get_width()
                NameTextHeight = NameText.get_height()

                self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()

                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.flip()
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version} | Welcome")

                PresentsText = PresentsFont.render("presents", True, self.FontCol)
                presentOffSet = 100

                PycraftText = PycraftFont.render("Pycraft", True, self.FontCol)
                TitleTextWidth = PycraftText.get_width()
                PycraftStartPos = self.mod_Pygame__.Vector2(((self.realWidth-TitleTextWidth)/2, self.realHeight/2 - NameTextHeight))

                PycraftEndPos = self.mod_Pygame__.Vector2(PycraftStartPos.x, 0)

                self.clock = self.mod_Pygame__.time.Clock()

                InterpolateSpeed = 0.02

                timer = 2
                deltaTime = 0
                
                if not self.currentDate == self.lastRun or self.crash == True or self.RunFullStartup == True:
                    self.AnimateLogo = False
                else:
                    self.AnimateLogo = True
                
                while timer > 0 and self.RunFullStartup == True:
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit()
                            
                    self.Display.fill(self.BackgroundCol)
                    timer -= deltaTime
                    self.Display.blit(NameText, ((self.realWidth-NameTextWidth)/2, self.realHeight/2 - NameTextHeight))
                    
                    if timer <= 1:
                        self.Display.blit(PresentsText, ((self.realWidth-NameTextWidth)/2 + presentOffSet, self.realHeight/2 + NameTextHeight - 70))

                    deltaTime = self.clock.tick(self.FPS) / 1000
                    self.mod_Pygame__.display.flip()

                self.mod_Threading__.Thread(target=self.mod_PycraftStartupTest__.StartupTest.PycraftResourceTest, args=(self,)).start()
                runTimer = 0
                Progress_Line = [(100, self.realHeight-100), (100, self.realHeight-100)]
                
                while True:
                    if not self.ResourceCheckTime[1] == 0:
                        calculation = (((self.realWidth-200)/self.ResourceCheckTime[1])*runTimer)+100
                        if calculation > self.realWidth-100:
                            calculation = self.realWidth-100

                        Progress_Line.append((calculation, self.realHeight-100))

                    RefreshTime = self.mod_Time__.perf_counter()
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit()

                    if self.UseMouseInput == False:
                        if self.JoystickExit == True:
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            self.mod_Pygame__.quit()
                            self.mod_Sys__.exit()
                            
                    if self.realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if self.realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)
                    
                    self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                    self.Display.fill(self.BackgroundCol)

                    if self.AnimateLogo == True or self.ResourceCheckTime[0] <= 0:
                        PycraftStartPos = self.mod_Pygame__.math.Vector2.lerp(PycraftStartPos, PycraftEndPos, InterpolateSpeed)
                    else:
                        self.mod_Pygame__.draw.lines(self.Display, (self.ShapeCol), self.aa, [(100, self.realHeight-100), (self.realWidth-100, self.realHeight-100)], 3)
                        self.mod_Pygame__.draw.lines(self.Display, (self.AccentCol), self.aa, Progress_Line)
                        
                    self.Display.blit(PycraftText, (PycraftStartPos.x, PycraftStartPos.y))

                    self.mod_Pygame__.display.flip()
                    self.clock.tick(self.FPS)
                    if PycraftStartPos.y <= 1:
                        PycraftStartPos = PycraftEndPos
                        self.RunFullStartup = False
                        break
                    runTimer += self.mod_Time__.perf_counter()-RefreshTime
                
                if not self.currentDate == self.lastRun or self.crash == True or self.RunFullStartup == True:
                    self.ResourceCheckTime[0] += 1
                    self.ResourceCheckTime[1] += self.CurrentResourceCheckTime
                    self.ResourceCheckTime[1] = self.ResourceCheckTime[1]/self.ResourceCheckTime[0]
            except Exception as Message:
                self.ErrorMessage = "StartupAnimation > GenerateStartupScreen > Start: "+str(Message)
                return Message

else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()