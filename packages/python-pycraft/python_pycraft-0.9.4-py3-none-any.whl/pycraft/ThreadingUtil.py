if not __name__ == "__main__":
    print("Started <Pycraft_ThreadingUtils>")
    class ThreadingUtils:
        def __init__(self):
            pass

        def StartVariableChecking(self):
            while True:
                if self.Iteration > 1000:
                    self.aFPS = (self.aFPS/self.Iteration)
                    self.Iteration = 1
                if self.FPS < 15 or self.FPS > 500:
                    print(f"ThreadingUtil > ThreadingUtils > StartVariableChecking: 'self.FPS' variable contained an invalid value, this has been reset to 60 from {self.FPS} previously")
                    self.FPS = 60
                else:
                    self.FPS = int(self.FPS)
                self.eFPS = int(self.eFPS)

                if self.Command == "Settings":
                    self.MovementSpeed = 1
                else:
                    self.MovementSpeed = 3
                    
                self.mod_Time__.sleep(1)
            
            print("'Thread_StartLongThread' has stopped")
        
        def StartCPUlogging(self):
            while True:
                if self.Devmode == 10:
                    if self.Timer >= 2:
                        CPUPercent = self.mod_Psutil__.cpu_percent(0.2)
                        if CPUPercent > self.Data_CPUUsE_Max:
                            self.Data_CPUUsE_Max = CPUPercent

                        self.Data_CPUUsE.append([((self.realWidth/2)+100)+(self.Timer), 200-(2)*CPUPercent])
                    else:
                        self.mod_Time__.sleep(0.2)
                else:
                    self.mod_Time__.sleep(1)
                    
            print("'Thread_GetCPUMetrics' has stopped")


        def AdaptiveMode(self):
            while True:
                if self.SettingsPreference == "Adaptive":
                    CPUPercent = self.mod_Psutil__.cpu_percent()
                    CoreCount = self.mod_Psutil__.cpu_count()

                    try:
                        gpus = self.mod_GPUtil__.getGPUs()

                        GPUPercent = 0
                        NumOfGPUs = 0

                        for gpu in gpus:
                            NumOfGPUs += 1
                            GPUPercent += gpu.load*100

                        GPUPercent = GPUPercent/NumOfGPUs
                    
                    except:
                        GPUPercent = CPUPercent

                    if (CPUPercent >= (100/CoreCount)) and (GPUPercent >= (100/CoreCount)):
                        self.FPS -= 10
                    else:
                        if self.FPS < self.RecommendedFPS:
                            self.FPS += 10
                        else:
                            if not (self.FPS == self.RecommendedFPS):
                                self.FPS -= 1
                    
                    self.mod_Time__.sleep(0.2)
                else:
                    self.mod_Time__.sleep(1)
                    
            print("'Thread_AdaptiveMode' has stopped")


else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()