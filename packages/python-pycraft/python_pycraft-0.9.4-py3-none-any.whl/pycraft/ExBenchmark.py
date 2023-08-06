if not __name__ == "__main__":
    print("Started <Pycraft_ExBenchmark>")
    class LoadBenchmark:
        def __init__(self):
            pass

        def run(self):
            try:
                FPSlistX = []
                FPSlistY = []

                FPSlistX2 = []
                FPSlistY2 = []
                
                global SetFPS, SetFPSlength

                SetFPS = [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 200, 250, 300, 350, 500]
                SetFPSlength = len(SetFPS)

                self.Display = self.mod_Pygame__.display.set_mode((1280, 720))

                iteration = 0
                FPScounter = 0
                MaxIteration = 500
                
                while iteration < (500*SetFPSlength):
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Benchmark | Running Blank Window Benchmark @ {SetFPS[FPScounter]} FPS")
                    while not iteration == MaxIteration:
                        if not self.clock.get_fps() == 0:
                            FPSlistX.append(iteration)
                            FPSlistY.append(self.clock.get_fps())
                        self.Display.fill(self.BackgroundCol)
                        for event in self.mod_Pygame__.event.get():
                            if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and (not event.key == self.mod_Pygame__.K_SPACE)):
                                return False

                        self.mod_Pygame__.display.flip()
                        iteration += 1
                        self.clock.tick(SetFPS[FPScounter])
                    FPScounter += 1
                    MaxIteration += 500

                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Benchmark | Preparing Animated Benchmark")

                iteration = 0
                FPScounter = 0
                MaxIteration = 500

                while not iteration == 60:
                    self.Display.fill(self.BackgroundCol)
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and (not event.key == self.mod_Pygame__.K_SPACE)):
                            return False

                    self.mod_Pygame__.display.flip()
                    iteration += 1
                    self.clock.tick(60)

                        
                iteration = 0
                FPScounter = 0
                MaxIteration = 500

                while iteration < (500*SetFPSlength):
                    self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Benchmark | Running Animated Window Benchmark @ {SetFPS[FPScounter]} FPS")
                    while not iteration == MaxIteration:
                        if not self.clock.get_fps() == 0:
                            FPSlistX2.append(iteration)
                            FPSlistY2.append(self.clock.get_fps())
                        self.Display.fill(self.BackgroundCol)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        self.mod_DrawingUtils__.DrawRose.CreateRose(self, 1, 1, False)
                        for event in self.mod_Pygame__.event.get():
                            if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and (not event.key == self.mod_Pygame__.K_SPACE)):
                                return False

                        self.mod_Pygame__.display.flip()
                        iteration += 1
                        self.clock.tick(SetFPS[FPScounter])
                    FPScounter += 1
                    MaxIteration += 500

                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Benchmark | Preparing OpenGL Benchmark")

                iteration = 0
                FPScounter = 0
                MaxIteration = 500
                
                while not iteration == 60:
                    self.Display.fill(self.BackgroundCol)
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and (not event.key == self.mod_Pygame__.K_SPACE)):
                            return False

                    self.mod_Pygame__.display.flip()
                    iteration += 1
                    self.clock.tick(60)

                self.mod_Pygame__.display.quit()
                self.mod_Pygame__.display.init()
                
                import os
                if "site-packages" in os.path.dirname(__file__) or "dist-packages" in os.path.dirname(__file__):
                    from pycraft.ShareDataUtil import Class_Startup_variables as SharedData
                else:
                    from ShareDataUtil import Class_Startup_variables as SharedData
                
                self.mod_Globals__.Share.initialize(self)
                
                global FPSlistX3, FPSlistY3
                
                FPSlistX3 = []
                FPSlistY3 = []

                class Create3Dbenchmark(self.mod_Base__.CameraWindow):
                    self.mod_Base__.title = "Crate"
                    self.mod_Base__.vsync = False

                    def __init__(self, **kwargs):
                        super().__init__(**kwargs)
                        if SharedData.platform == "Linux":
                            self.prog = self.load_program(SharedData.mod_OS__.path.join(SharedData.base_folder, ("programs//benchmark.glsl")))
                            self.scene = self.load_scene(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//Benchmark_Resources//Crate.obj")))
                            self.texture = self.load_texture_2d(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources//Benchmark_Resources//Crate.png")))
                        else:
                            self.prog = self.load_program(SharedData.mod_OS__.path.join(SharedData.base_folder, ("programs\\benchmark.glsl")))
                            self.scene = self.load_scene(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\Benchmark_Resources\\Crate.obj")))
                            self.texture = self.load_texture_2d(SharedData.mod_OS__.path.join(SharedData.base_folder, ("Resources\\Benchmark_Resources\\Crate.png")))
                            
                        self.mvp = self.prog['Mvp']
                        self.light = self.prog['Light']
                        
                        self.vao = self.scene.root_nodes[0].mesh.vao.instance(self.prog)
                        
                        self.iteration = 0
                        self.FPScounter = 0
                        self.MaxIteration = 500
                        
                        self.wnd.title = f"Pycraft: v{SharedData.version}: Benchmark | Running OpenGL Benchmark @ {SetFPS[self.FPScounter]} FPS"
                        
                        self.PreviousFPS = 15
                        
                        self.aFPS = 15
                        
                    def render(self, time, frame_time):
                        try:
                            global FPSlistX3, FPSlistY3, SetFPS, SetFPSlength
                            
                            if self.iteration <= 500*SetFPSlength:
                                if self.iteration == self.MaxIteration:
                                    self.FPScounter += 1
                                    self.MaxIteration += 500
                                    if self.FPScounter <= SetFPSlength:
                                        self.wnd.title = f"Pycraft: v{SharedData.version}: Benchmark | Running OpenGL Benchmark @ {SetFPS[self.FPScounter]} FPS"
                                    
                                StartTime = SharedData.mod_Time__.perf_counter()
                                
                                angle = time
                                self.ctx.clear(0.0, 0.0, 0.0)
                                self.ctx.enable(SharedData.mod_ModernGL__.DEPTH_TEST)

                                camera_pos = (SharedData.mod_Numpy__.cos(angle) * 3.0, SharedData.mod_Numpy__.sin(angle) * 3.0, 2.0)

                                proj = SharedData.mod_Pyrr_Matrix44_.perspective_projection(45.0, self.aspect_ratio, 0.1, 100.0)
                                lookat = SharedData.mod_Pyrr_Matrix44_.look_at(
                                    camera_pos,
                                    (0.0, 0.0, 0.5),
                                    (0.0, 0.0, 1.0),
                                )

                                self.mvp.write((proj * lookat).astype('f4'))
                                self.light.value = camera_pos
                                self.texture.use()
                                self.vao.render()
                                SharedData.mod_Time__.sleep(1/(SetFPS[self.FPScounter]))
                        
                                eFPS = 1/(SharedData.mod_Time__.perf_counter()-StartTime)
                                self.aFPS = (eFPS+self.PreviousFPS)/2
                                self.PreviousFPS = eFPS

                                if not eFPS == 0 and len(FPSlistX3) < 7500:
                                    FPSlistX3.append(self.iteration)
                                    FPSlistY3.append(self.aFPS)
                                
                                self.iteration += 1
                            else:
                                self.wnd.close()
                                self.wnd.destroy()
                                self.wnd._close = True
                        except Exception as Message:
                            self.ErrorMessage = "ExBenchmark > Create3Dbenchmark > render: "+str(Message)
                            try:
                                self.wnd.close()
                                self.wnd.destroy()
                                self.wnd._close = True
                            except:
                                pass

                Create3Dbenchmark.run()
                self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
            except Exception as Message:
                print(Message)
                self.ErrorMessage = "ExBenchmark > LoadBenchmark > run: "+str(Message)
            else:
                return FPSlistX, FPSlistY, FPSlistX2, FPSlistY2, FPSlistX3, FPSlistY3
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()