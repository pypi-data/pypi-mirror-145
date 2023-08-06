if not __name__ == "__main__":
    print("Started <Pycraft_SoundUtils>")
    class PlaySound:
        def __init__(self):
            pass

        def PlayClickSound(self):
            try:
                channel1 = self.mod_Pygame__.mixer.Channel(0)
                if self.platform == "Linux":
                    clickMUSIC = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources//General_Resources//Click.wav")))
                else:
                    clickMUSIC = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\Click.wav")))
                channel1.set_volume(self.soundVOL/100)
                channel1.play(clickMUSIC)
                self.mod_Pygame__.time.wait(40)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayClickSound: "+str(Message)

        def PlayFootstepsSound(self):
            try:
                channel2 = self.mod_Pygame__.mixer.Channel(1)
                if self.platform == "Linux":
                    Footsteps = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, (f"Resources//G3_Resources//GameSounds//footsteps{self.mod_Random__.randint(0, 5)}.wav")))
                else:
                    Footsteps = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, (f"Resources\\G3_Resources\\GameSounds\\footsteps{self.mod_Random__.randint(0, 5)}.wav")))
                channel2.set_volume(self.soundVOL/100)
                channel2.play(Footsteps)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayFootstepsSound: "+str(Message)


        def PlayInvSound(self):
            try:
                if self.platform == "Linux":
                    self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources//General_Resources//InventoryGeneral.ogg")))
                else:
                    self.mod_Pygame__.mixer.music.load(self.mod_OS__.path.join(self.base_folder, ("Resources\\General_Resources\\InventoryGeneral.ogg")))
                self.mod_Pygame__.mixer.music.set_volume(self.musicVOL/100)
                self.mod_Pygame__.mixer.music.play(-1)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayInvSound: "+str(Message)


        def PlayAmbientSound(self):
            try:
                channel4 = self.mod_Pygame__.mixer.Channel(3)
                if self.platform == "Linux":
                    LoadAmb = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources//G3_Resources//GameSounds//FieldAmb.wav")))
                else:
                    LoadAmb = self.mod_Pygame__.mixer.Sound(self.mod_OS__.path.join(self.base_folder, ("Resources\\G3_Resources\\GameSounds\\FieldAmb.wav")))
                channel4.set_volume(self.soundVOL/100)
                channel4.play(LoadAmb)
            except Exception as Message:
                if not self.Stop_Thread_Event.is_set():
                    self.ErrorMessage = "SoundUtils > PlaySound > PlayAmbientSound: "+str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()