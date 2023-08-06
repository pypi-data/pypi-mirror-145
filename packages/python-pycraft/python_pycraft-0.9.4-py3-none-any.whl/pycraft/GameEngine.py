if not __name__ == "__main__":
    print("Started <Pycraft_GameEngine>")
    
    import os
    if "site-packages" in os.path.dirname(__file__) or "dist-packages" in os.path.dirname(__file__):
        from pycraft.ShareDataUtil import Class_Startup_variables as SharedData
    else:
        from ShareDataUtil import Class_Startup_variables as SharedData
    
    SharedData.mod_ModernGL_window_.setup_basic_logging(0)
    
    
    class Cubemap(SharedData.mod_Base__.CameraWindow):
        SharedData.mod_Base__.CameraWindow.title = f"Pycraft: v{SharedData.version}: Playing"
        SharedData.mod_Base__.CameraWindow.resource_dir = SharedData.base_folder
        SharedData.mod_Base__.CameraWindow.vsync = False
        SharedData.mod_Base__.CameraWindow.resizable = False
                
        def Exit(self, SharedData, Command):
            try:
                if SharedData.mod_Pygame__.mixer.Channel(3).get_busy() == True: 
                    SharedData.mod_Pygame__.mixer.Channel(3).stop()
                    SharedData.mod_Pygame__.quit()
                    
                self.wnd.mouse_exclusivity = False
            except Exception as Message:
                print("GameEngine > Cubemap > Exit: " + str(Message))

            SharedData.mod_Pygame__.init()
            if SharedData.platform == "Linux":
                SharedData.TitleFont = SharedData.mod_Pygame__.font.Font(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Fonts//Book Antiqua.ttf")), 60)
                SharedData.WindowIcon = SharedData.mod_Pygame__.image.load(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//General_Resources//Icon.png")))
            else:
                SharedData.TitleFont = SharedData.mod_Pygame__.font.Font(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)
                SharedData.WindowIcon = SharedData.mod_Pygame__.image.load(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\General_Resources\\Icon.png")))
            self.wnd._set_fullscreen(False)
            self.wnd.close()
            self.wnd.destroy()
            SharedData.CurrentlyPlaying = None
            SharedData.JoystickExit = False
            SharedData.LoadMusic = True
            SharedData.Command = Command
            
            SharedData.GameEngine_Control[0][0] = False
            SharedData.GameEngine_Control[0][1] = False
            
            if self.wnd.fullscreen == True:
                SharedData.Fullscreen = False
            else:
                SharedData.Fullscreen = True
                
            self.cube.release()
            self.obj.release()
            self.SkyBox_texture.release()
            del self


        def __init__(self, **kwargs):
            try:
                SharedData.mod_Globals__.Share.initialize_controller([[False, False], [False, False], [False, False], [False, False]])
                SharedData.mod_Pygame__.init()
                global Global_Save_and_QUIT
                Global_Save_and_QUIT = False
                if SharedData.FromGameGUI == False:
                    StartLoading = SharedData.mod_Time__.perf_counter()
                global GameEngine_Initialisation
                global GameEngine_Initialisation_percentage
                GameEngine_Initialisation_percentage = 10
                GameEngine_Initialisation = True
                CreateLoadScreen = SharedData.mod_Threading__.Thread(target=CreateEngine.RenderLoadDisplay, args=(SharedData, ))
                CreateLoadScreen.start()
                CreateLoadScreen.name = "Thread_CreateLoadScreen"
                
                GameEngine_Initialisation_percentage = 20
                super().__init__(**kwargs)
                                    
                WindowSize = SharedData.realWidth, SharedData.realHeight
                CurrentWindowSize = WindowSize
                
                self.wnd.position = (-WindowSize[0], -WindowSize[1])
                
                self.wnd.size = WindowSize
                self.wnd.mouse_exclusivity = False
                                
                self.camera.projection.update(near=0.1, far=2000.0, fov=70)
                
                GameEngine_Initialisation_percentage = 20
                
                if SharedData.platform == "Linux":
                    self.obj = self.load_scene(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//Map//map.obj")), cache=True)
                else:
                    self.obj = self.load_scene(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\Map\\map.obj")), cache=True)
                
                GameEngine_Initialisation_percentage = 30
                            
                self.cube = SharedData.mod_ModernGL_window_.geometry.cube(size=(2000, 2000, 2000))
                
                GameEngine_Initialisation_percentage = 40
                if SharedData.platform == "Linux":
                    self.prog = self.load_program(SharedData.mod_OS__.path.join(SharedData.base_folder, ("programs//cubemap.glsl")))
                else:
                    self.prog = self.load_program(SharedData.mod_OS__.path.join(SharedData.base_folder, ("programs\\cubemap.glsl")))

                GameEngine_Initialisation_percentage = 45
                
                if SharedData.platform == "Linux":
                    self.SkyBox_texture = self.load_texture_cube(
                        neg_x=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//back.jpg")),
                        neg_y=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//bottom.jpg")),
                        neg_z=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//left.jpg")),
                        pos_x=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//front.jpg")),
                        pos_y=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//top.jpg")),
                        pos_z=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//G3_Resources//skybox//right.jpg")),
                        flip_x=True,
                    )
                else:
                    self.SkyBox_texture = self.load_texture_cube(
                        neg_x=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\back.jpg")),
                        neg_y=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\bottom.jpg")),
                        neg_z=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\left.jpg")),
                        pos_x=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\front.jpg")),
                        pos_y=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\top.jpg")),
                        pos_z=SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\G3_Resources\\skybox\\right.jpg")),
                        flip_x=True,
                    )
                
                GameEngine_Initialisation_percentage = 50
        
                Prev_Mouse_Pos = (0,0)
                Mouse_Pos = (0,0)
                DeltaX, DeltaY = 0, 0
                
                self.wnd.exit_key = None
                
                GameEngine_Initialisation_percentage = 60
                
                MouseUnlock = True
                
                Jump = False
                JumpUP = True
                
                self.camera.position.y += 0.7
                
                GameEngine_Initialisation_percentage = 70
                
                WkeydownTimer = 0
                AkeydownTimer = 0
                SkeydownTimer = 0
                DkeydownTimer = 0
                
                GameEngine_Initialisation_percentage = 80
                
                RunForwardTimer = 0
                
                Jump_Start_FPS = 0
                
                GameEngine_Initialisation_percentage = 90
                
                Collision = False
                
                GameEngine_Initialisation_percentage = 100
                                
                if SharedData.Fullscreen == False:
                    self.wnd.fullscreen = True
                else:
                    try:
                        DisplayPosition = SharedData.mod_DisplayUtils__.DisplayUtils.GetDisplayLocation(SharedData)
                    except Exception as Message:
                        print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                        self.wnd.fixed_aspect_ratio = SharedData.realWidth / SharedData.realHeight
                        self.wnd.window_size = SharedData.realWidth, SharedData.realHeight
                        CurrentWindowSize = self.window_size
                        DisplayPosition = (int((SharedData.FullscreenX-CurrentWindowSize[0])/2), int((SharedData.FullscreenY-CurrentWindowSize[1])/2))
                    finally:
                        self.wnd.position = DisplayPosition
                
                
                OnStart = True
                
                while True:
                    if "site-packages" in os.path.dirname(__file__) or "dist-packages" in os.path.dirname(__file__):
                        from pycraft.ShareDataUtil import Controller
                    else:
                        from ShareDataUtil import Controller
                    
                    start = SharedData.mod_Time__.perf_counter()
                    SharedData.aFPS += SharedData.eFPS
                    SharedData.mod_CaptionUtils__.GenerateCaptions.GetOpenGLCaption(SharedData, self)
                    try:
                        if SharedData.mod_Pygame__.mixer.get_busy() == False:
                            SharedData.mod_SoundUtils__.PlaySound.PlayAmbientSound(SharedData)
                    except Exception as Message:
                        print("GameEngine > Cubemap: "+str(Message))
                    
                    self.ctx.clear(1.0, 1.0, 1.0)
                    
                    CurrentWindowSize = self.window_size

                    Prev_Mouse_Pos = Mouse_Pos 
                    Mouse_Pos = SharedData.mod_Pyautogui__.position()
                    DeltaX, DeltaY = Mouse_Pos[0]-Prev_Mouse_Pos[0], Mouse_Pos[1]-Prev_Mouse_Pos[1]
                        
                    if self.wnd.is_key_pressed(self.wnd.keys.ESCAPE) or Global_Save_and_QUIT == True or SharedData.JoystickExit == True:
                        Cubemap.Exit(self, SharedData, "Undefined")
                        return
                    
                    if self.wnd.is_key_pressed(self.wnd.keys.W) or Controller[2][0] < 0:
                        RunForwardTimer += (1/SharedData.eFPS)
                        if RunForwardTimer <= 10:
                            if SharedData.sound == True: 
                                WkeydownTimer += (1/SharedData.eFPS)
                                if WkeydownTimer >= (SharedData.mod_Random__.randint(50, 100)/100):
                                    SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(SharedData)
                                    WkeydownTimer = 0
                            self.camera.position.x += 1.42/SharedData.eFPS
                        else:
                            if SharedData.sound == True:
                                WkeydownTimer += (1/SharedData.eFPS)
                                if WkeydownTimer >= (SharedData.mod_Random__.randint(25, 75)/100):
                                    SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(SharedData)
                                    WkeydownTimer = 0
                            self.camera.projection.update(near=0.1, far=2000.0, fov=80)
                            self.camera.position.x += 2.2352/SharedData.eFPS
                    else:
                        self.camera.projection.update(near=0.1, far=2000.0, fov=70)
                        RunForwardTimer = 0
                    
                    if self.wnd.is_key_pressed(self.wnd.keys.A) or Controller[2][1] > 0:
                        if SharedData.sound == True: 
                            AkeydownTimer += (1/SharedData.eFPS)
                            if AkeydownTimer >= (SharedData.mod_Random__.randint(50, 100)/100):
                                SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(SharedData)
                                AkeydownTimer = 0
                        self.camera.position.z += 1.42/SharedData.eFPS
                        
                    if self.wnd.is_key_pressed(self.wnd.keys.S) or Controller[2][0] > 0:
                        if SharedData.sound == True: 
                            SkeydownTimer += (1/SharedData.eFPS)
                            if SkeydownTimer >= (SharedData.mod_Random__.randint(50, 100)/100):
                                SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(SharedData)
                                SkeydownTimer = 0
                        self.camera.position.x -= 1.42/SharedData.eFPS
                        
                    if self.wnd.is_key_pressed(self.wnd.keys.D) or Controller[2][1] < 0:
                        if SharedData.sound == True: 
                            DkeydownTimer += (1/SharedData.eFPS)
                            if DkeydownTimer >= (SharedData.mod_Random__.randint(50, 100)/100):
                                SharedData.mod_SoundUtils__.PlaySound.PlayFootstepsSound(SharedData)
                                DkeydownTimer = 0
                        self.camera.position.z -= 1.42/SharedData.eFPS
                        
                    if self.wnd.is_key_pressed(self.wnd.keys.E) or Controller[0][0]:
                        SharedData.FromGameGUI = True
                        if self.wnd._fullscreen == True:
                            myScreenshot = SharedData.mod_Pyautogui__.screenshot(region=((0, 0, SharedData.FullscreenX, SharedData.FullscreenY)))
                            if SharedData.platform == "Linux":
                                myScreenshot.save(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//General_Resources//PauseIMG.png")))
                            else:
                                myScreenshot.save(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\General_Resources\\PauseIMG.png")))
                        else:
                            PosX, PosY = self.wnd.position
                            myScreenshot = SharedData.mod_Pyautogui__.screenshot(region=((PosX, PosY, SharedData.realWidth, SharedData.realHeight)))
                            if SharedData.platform == "Linux":
                                myScreenshot.save(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//General_Resources//PauseIMG.png")))
                            else:
                                myScreenshot.save(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\General_Resources\\PauseIMG.png")))
                        Cubemap.Exit(self, SharedData, "Inventory")
                        return
                    
                    if self.wnd.is_key_pressed(self.wnd.keys.R) or Controller[0][1]:
                        Cubemap.Exit(self, SharedData, "MapGUI")
                        return
                    
                    if self.wnd.is_key_pressed(self.wnd.keys.L):
                        if Keydown == False:
                            MouseUnlock = not MouseUnlock
                            Keydown = True
                    else:
                        Keydown = False
                        
                    if (self.wnd.is_key_pressed(self.wnd.keys.SPACE) or Controller[3][0] == True) and Jump == False:
                        Jump = True
                        JumpUP = True
                        StartYposition = self.camera.position.y
                        Jump_Start_FPS = SharedData.eFPS
                        Controller[3][0] = False
                        
                    if Jump == True:
                        if JumpUP == True:
                            self.camera.position.y += (1/Jump_Start_FPS)
                            if self.camera.position.y >= StartYposition+0.5:
                                JumpUP = False
                        else:
                            self.camera.position.y -= 1/Jump_Start_FPS
                            if self.camera.position.y <= StartYposition:
                                Jump = False
                                if Collision == False:
                                    self.camera.position.y = StartYposition
                        
                        
                    self.ctx.enable(SharedData.mod_ModernGL__.CULL_FACE | SharedData.mod_ModernGL__.DEPTH_TEST)

                    cam = self.camera.matrix
                    SharedData.X = round(float(str(self.camera.position.x)), 2)
                    SharedData.Y = round(float(str(self.camera.position.y)), 2)
                    SharedData.Z = round(float(str(self.camera.position.z)), 2)
                    
                    cam[3][0] = 0
                    cam[3][1] = 0
                    cam[3][2] = 0

                    self.SkyBox_texture.use(location=0)
                    self.prog['m_proj'].write(self.camera.projection.matrix)
                    self.prog['m_camera'].write(cam)
                    
                    if SharedData.UseMouseInput == False:
                        DeltaX = Controller[1][0]*SharedData.cameraANGspeed
                        DeltaY = Controller[1][1]*SharedData.cameraANGspeed
                    try:
                        if MouseUnlock == True:
                            self.camera.rot_state(-DeltaX, -DeltaY)
                            self.wnd.mouse_exclusivity = True
                        else:
                            self.wnd.mouse_exclusivity = False
                    except Exception as Message:
                        print("GameEngine > Cubemap: " + Message)
                    
                    self.ctx.front_face = 'cw'
                    self.cube.render(self.prog)
                    
                    self.ctx.front_face = 'ccw'
                    self.obj.draw(projection_matrix=self.camera.projection.matrix, camera_matrix=self.camera.matrix)
                    
                    try:
                        self.wnd.swap_buffers()
                    except Exception as Message:
                        print("GameEngine > Cubemap: " + Message)
                        
                    SharedData.mod_Time__.sleep(1/SharedData.FPS)
                    
                    SharedData.eFPS = 1/(SharedData.mod_Time__.perf_counter()-start)
                    SharedData.Iteration += 1
                    if OnStart == True:
                        OnStart = False
                        GameEngine_Initialisation = False
                        if SharedData.FromGameGUI == False:
                            SharedData.LoadTime = [SharedData.LoadTime[0] + SharedData.mod_Time__.perf_counter()-StartLoading, SharedData.LoadTime[1] + 1]
                        else:
                            SharedData.FromGameGUI = False
            except Exception as Message:
                print("GameEngine > Cubemap: " + str(Message))
                print(''.join(SharedData.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                Cubemap.Exit(self, SharedData, "Undefined")
                SharedData.GameError = "GameEngine > Cubemap: " + str(Message)
                
                
    class CreateEngine:
        def __init__(self):
            pass
        
        
        def RenderLoadDisplay(self):
            try:
                self.mod_CaptionUtils__.GenerateCaptions.GetNormalCaption(self, "Loading Pycraft")
                self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                
                if self.platform == "Linux":
                    SecondaryFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 35)
                    LoadingFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                    LoadingTextFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 15)
                else:
                    SecondaryFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 35)
                    LoadingFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                    LoadingTextFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 15)
                
                global GameEngine_Initialisation
                global GameEngine_Initialisation_percentage
                            
                time = 0
                
                self.clock = self.mod_Pygame__.time.Clock()
                
                self.ProgressMessageText = self.mod_TextUtils__.GenerateText.LoadQuickText(self)
                
                Completion_Percentage = 0
                        
                while GameEngine_Initialisation == True:
                    eFPS = self.clock.get_fps()
                    if not self.LoadTime[0] == 0:
                        if eFPS > 0:
                            time += 1/eFPS
                        GameEngine_Initialisation_percentage_calculated = (self.realWidth/(self.LoadTime[0]/self.LoadTime[1]))*time

                    if GameEngine_Initialisation_percentage <= 10:
                        text = "Initializing"
                    elif GameEngine_Initialisation_percentage <= 20:
                        text = "Creating viewport"
                    elif GameEngine_Initialisation_percentage <= 30:
                        text = "Loading in-game objects: Map"
                    elif GameEngine_Initialisation_percentage <= 40:
                        text = "Loading in-game programs: Cubemap"
                    elif GameEngine_Initialisation_percentage <= 45:
                        text = "Loading in-game textures: Skybox"
                    else:
                        text = "Making final touches"
                                            
                    self.Progress_Line = [(100, self.realHeight-100), (100, self.realHeight-100)]
                    
                    if not self.LoadTime[0] == 0:
                        if GameEngine_Initialisation_percentage_calculated > self.realWidth-200:
                            GameEngine_Initialisation_percentage_calculated = self.realWidth-200
                            
                        self.Progress_Line.append((100+GameEngine_Initialisation_percentage_calculated, self.realHeight-100))
                        Completion_Percentage = (100/(self.LoadTime[0]/self.LoadTime[1]))*time
                        if Completion_Percentage > 100:
                            Completion_Percentage = 100
                    else:
                        self.Progress_Line.append((((self.realWidth/100)*GameEngine_Initialisation_percentage)-100, self.realHeight-100))
                        Completion_Percentage = GameEngine_Initialisation_percentage
                        
                    CreateEngine.GenerateLoadDisplay(self, LoadingFont, text, SecondaryFont, LoadingTextFont, Completion_Percentage)
                    
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE):
                            global Global_Save_and_QUIT
                            Global_Save_and_QUIT = True
                            quit()
                            
                    self.mod_Pygame__.display.flip()
                    
                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)
                    
                    self.clock.tick(tempFPS)
                    
                if self.LoadTime[1] >= 25:
                    self.LoadTime = [0, 1]
                    
                self.mod_Pygame__.display.quit()
                self.mod_Pygame__.display.init()
            except Exception as Message:
                print("GameEngine > CreateEngine > RenderLoadDisplay: "+str(Message))
                            
            
        def GenerateLoadDisplay(self, LoadingFont, text, SecondaryFont, LoadingTextFont, Completion_Percentage):
            try:
                self.Display.fill(self.BackgroundCol)

                self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()

                PycraftTitle = self.TitleFont.render("Pycraft", self.aa, self.FontCol)
                TitleWidth = PycraftTitle.get_width()
                self.Display.blit(PycraftTitle, ((self.realWidth-TitleWidth)/2, 0))

                LoadingTitle = SecondaryFont.render("Loading", self.aa, self.SecondFontCol)
                self.Display.blit(LoadingTitle, (((self.realWidth-TitleWidth)/2)+55, 50))

                self.mod_Pygame__.draw.lines(self.Display, (self.ShapeCol), self.aa, [(100, self.realHeight-100), (self.realWidth-100, self.realHeight-100)], 3)
                self.mod_Pygame__.draw.lines(self.Display, (self.AccentCol), self.aa, self.Progress_Line)

                DisplayMessage = LoadingFont.render(self.ProgressMessageText, self.aa, self.FontCol)
                DisplayMessageWidth = DisplayMessage.get_width()
                self.Display.blit(DisplayMessage, ((self.realWidth-DisplayMessageWidth)/2, self.realHeight-120))

                TextFontRendered = LoadingTextFont.render(f"{text}", self.aa, self.FontCol)
                TextFontRenderedWidth = TextFontRendered.get_width()
                self.Display.blit(TextFontRendered, ((self.realWidth-TextFontRenderedWidth)/2, self.realHeight-100))
                
                ProgressText = LoadingTextFont.render(f"{round(Completion_Percentage)}% complete", self.aa, self.FontCol)
                ProgressTextWidth = ProgressText.get_width()
                self.Display.blit(ProgressText, ((self.realWidth-ProgressTextWidth)/2, self.realHeight-80))
            except Exception as Message:
                print("GameEngine > CreateEngine > GenerateLoadDisplay: "+str(Message))
                self.ErrorMessage = "GameEngine > CreateEngine > GenerateLoadDisplay: " + str(Message)

        def Play(self):
            try:
                self.mod_Pygame__.mixer.music.fadeout(500)
                
                self.mod_Pygame__.mouse.set_cursor(self.mod_Pygame__.SYSTEM_CURSOR_WAIT)
                self.mod_Pygame__.quit()
                self.mod_Pygame__.init()
                if self.platform == "Linux":
                    self.TitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts//Book Antiqua.ttf")), 60)
                    self.WindowIcon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//General_Resources//Icon.png")))
                else:
                    self.TitleFont = self.mod_Pygame__.font.Font(self.mod_OS__.path.join(self.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)
                    self.WindowIcon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Icon.png")))
                self.mod_Globals__.Share.initialize(self)
                
                try:
                    self.mod_ModernGL_window_.run_window_config(Cubemap)
                except Exception as Message:
                    if not (str(Message) == "argument 2: <class 'TypeError'>: wrong type" or str(Message) == "'NoneType' object has no attribute 'flip'"):
                        self.ErrorMessage = "GameEngine > CreateEngine > Play: " + str(Message) 
                        SharedData.Command = "Undefined"
                return SharedData.Command
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                self.ErrorMessage = "GameEngine > CreateEngine > Play: " + str(Message)         
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()