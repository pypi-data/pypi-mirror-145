if not __name__ == "__main__":
    print("Started <Pycraft_MapGUI>")
    class GenerateMapGUI:
        def __init__(self):
            pass

        def GetMapPos(self):
            x = 0
            z = 0
            if self.X == 0:
                x = 640
            if self.Z == 0:
                z = 360
            x -= 6
            z -= 19
            return (x,z)


        def MapGUI(self):
            try:
                Message = self.mod_DisplayUtils__.DisplayUtils.SetDisplay(self)
                self.Display.fill(self.BackgroundCol)
                self.mod_Pygame__.display.update()

                if self.platform == "Linux":
                    MapPIL =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png")))
                else:
                    MapPIL =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png")))
                Map0 = self.mod_Pygame__.image.fromstring(MapPIL.tobytes(), MapPIL.size, MapPIL.mode)
                if self.platform == "Linux":
                    MapIcon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Marker.jpg"))).convert()
                else:
                    MapIcon = self.mod_Pygame__.image.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Marker.jpg"))).convert()
                zoom = 0
                self.mod_Pygame__.display.set_caption(f"Pycraft: v{self.version}: Playing | Map")

                X,Y = 0, 0
                key = ""
                Mx, My = self.realWidth/2, self.realHeight/2
                
                if self.platform == "Linux":
                    MapPIL0 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((self.realWidth, self.realHeight),  self.mod_PIL_Image_.ANTIALIAS)
                else:
                    MapPIL0 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((self.realWidth, self.realHeight),  self.mod_PIL_Image_.ANTIALIAS)
                Map0 = self.mod_Pygame__.image.fromstring(MapPIL0.tobytes(), MapPIL0.size, MapPIL0.mode)

                if self.platform == "Linux":
                    MapPIL1 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((int(self.realWidth*1.75), int(self.realHeight*1.75)),  self.mod_PIL_Image_.ANTIALIAS) 
                else:
                    MapPIL1 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((int(self.realWidth*1.75), int(self.realHeight*1.75)),  self.mod_PIL_Image_.ANTIALIAS) 
                Map1 = self.mod_Pygame__.image.fromstring(MapPIL1.tobytes(), MapPIL1.size, MapPIL1.mode)

                if self.platform == "Linux":
                    MapPIL2 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((int(self.realWidth*2), int(self.realHeight*2)),  self.mod_PIL_Image_.ANTIALIAS) 
                else:
                    MapPIL2 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((int(self.realWidth*2), int(self.realHeight*2)),  self.mod_PIL_Image_.ANTIALIAS) 
                Map2 = self.mod_Pygame__.image.fromstring(MapPIL2.tobytes(), MapPIL2.size, MapPIL2.mode)
                    
                while True:
                    if self.UseMouseInput == False:
                        Mx, My = Mx+self.JoystickMouse[0], My+self.JoystickMouse[1]
                        self.mod_Pygame__.mouse.set_pos(Mx, My)
                    else:
                        self.JoystickConfirm = False
                        
                    self.realWidth, self.realHeight = self.mod_Pygame__.display.get_window_size()
                    
                    tempFPS = self.mod_DisplayUtils__.DisplayUtils.GetPlayStatus(self)
                    
                    if self.realWidth < 1280:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, 1280, self.SavedHeight)
                    if self.realHeight < 720:
                        self.mod_DisplayUtils__.DisplayUtils.GenerateMinDisplay(self, self.SavedWidth, 720)
                    
                    self.Display.fill(self.BackgroundCol)
                    for event in self.mod_Pygame__.event.get():
                        if event.type == self.mod_Pygame__.QUIT or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_ESCAPE) or (event.type == self.mod_Pygame__.KEYDOWN and event.key == self.mod_Pygame__.K_r):
                            self.Load3D = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                        if event.type == self.mod_Pygame__.WINDOWSIZECHANGED:
                            if self.platform == "Linux":
                                MapPIL0 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((self.realWidth, self.realHeight),  self.mod_PIL_Image_.ANTIALIAS)
                            else:
                                MapPIL0 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((self.realWidth, self.realHeight),  self.mod_PIL_Image_.ANTIALIAS)
                            Map0 = self.mod_Pygame__.image.fromstring(MapPIL0.tobytes(), MapPIL0.size, MapPIL0.mode)

                            if self.platform == "Linux":
                                MapPIL1 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((int(self.realWidth*1.75), int(self.realHeight*1.75)),  self.mod_PIL_Image_.ANTIALIAS) 
                            else:
                                MapPIL1 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((int(self.realWidth*1.75), int(self.realHeight*1.75)),  self.mod_PIL_Image_.ANTIALIAS) 
                            Map1 = self.mod_Pygame__.image.fromstring(MapPIL1.tobytes(), MapPIL1.size, MapPIL1.mode)

                            if self.platform == "Linux":
                                MapPIL2 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources//Map_Resources//Full_Map.png"))).resize((int(self.realWidth*2), int(self.realHeight*2)),  self.mod_PIL_Image_.ANTIALIAS) 
                            else:
                                MapPIL2 =  self.mod_PIL_Image_.open(self.mod_OS__.path.join(self.base_folder, ("Resources\\Map_Resources\\Full_Map.png"))).resize((int(self.realWidth*2), int(self.realHeight*2)),  self.mod_PIL_Image_.ANTIALIAS) 
                            Map2 = self.mod_Pygame__.image.fromstring(MapPIL2.tobytes(), MapPIL2.size, MapPIL2.mode)
                                
                        if event.type == self.mod_Pygame__.KEYDOWN:
                            if event.key == self.mod_Pygame__.K_SPACE:
                                zoom = 0
                            if event.key == self.mod_Pygame__.K_w:
                                key = "w"
                            if event.key == self.mod_Pygame__.K_s:
                                key = "s"
                            if event.key == self.mod_Pygame__.K_d:
                                key = "d"
                            if event.key == self.mod_Pygame__.K_a:
                                key = "a"
                            if event.key == self.mod_Pygame__.K_F11:
                                self.mod_DisplayUtils__.DisplayUtils.UpdateDisplay(self)
                        if event.type == self.mod_Pygame__.KEYUP:
                            key = ""
                        if event.type == self.mod_Pygame__.MOUSEWHEEL:
                            if str(event.y)[0] == "-":
                                zoom -= 1
                            else:
                                zoom += 1
                                
                    if self.UseMouseInput == False:
                        if self.JoystickExit == True:
                            self.JoystickExit = False
                            if self.sound == True:
                                self.mod_SoundUtils__.PlaySound.PlayClickSound(self)
                            return
                        
                    if zoom >= 2:
                        zoom = 2
                    if zoom <= 0:
                        zoom = 0
                        
                    if key == "w":
                        if zoom == 1:
                            Y -= 5
                        elif zoom == 2:
                            Y -= 10
                    if key == "s":
                        if zoom == 1:
                            Y += 5
                        elif zoom == 2:
                            Y += 10
                    if key == "d":
                        if zoom == 1:
                            X += 5
                        elif zoom == 2:
                            X += 10
                    if key == "a":
                        if zoom == 1:
                            X -= 5
                        elif zoom == 2:
                            X -= 10

                    if zoom == 1:
                        self.Display.blit(Map1, (X,Y))
                        self.Display.blit(MapIcon, GenerateMapGUI.GetMapPos(self))
                        if X <= -955:
                            X = -955
                        if Y <= -535:
                            Y = -535
                        if X >= -5:
                            X = -5
                        if Y >= -5:
                            Y = -5
                    elif zoom == 2:
                        self.Display.blit(Map2, (X,Y))
                        self.Display.blit(MapIcon, GenerateMapGUI.GetMapPos(self))
                        if X <= -1590:
                            X = -1590
                        if Y <= -890:
                            Y = -890
                        if X >= -10:
                            X = -10
                        if Y >= -10:
                            Y = -10
                    else:
                        self.Display.blit(Map0, (0, 0))
                        self.Display.blit(MapIcon, GenerateMapGUI.GetMapPos(self))
                        x, y = 0, 0
                        
                    self.mod_Pygame__.display.update()
                    self.clock.tick(tempFPS)
            except Exception as Message:
                print(''.join(self.mod_Traceback__.format_exception(None, Message, Message.__traceback__)))
                self.ErrorMessage = "MapGUI > GenerateMapGUI > MapGUI: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()