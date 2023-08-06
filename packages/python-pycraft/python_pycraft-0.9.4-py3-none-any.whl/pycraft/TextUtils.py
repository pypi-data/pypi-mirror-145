if not __name__ == "__main__":
    print("Started <Pycraft_TextUtils>")
    class InstallerText:
        def __init__(self):
            pass
        
        def CreateText(InstallerImportData, root, OUTPUTtext):
            text = InstallerImportData.mod_Tkinter_tk_.Text(root, wrap=InstallerImportData.mod_Tkinter_tk_.WORD, relief=InstallerImportData.mod_Tkinter_tk_.FLAT, font=(None, 10))
            text.insert(InstallerImportData.mod_Tkinter_tk_.INSERT, OUTPUTtext)
            text["state"] = InstallerImportData.mod_Tkinter_tk_.DISABLED
            text.place(x=200, y=80)
            root.update_idletasks()
            
    class GenerateText:
        def __init__(self):
            pass

        def LoadQuickText(self):
            LoadingText = ["Use W,A,S,D to move",
                           "Use W to move forward",
                           "Use S to move backward",
                           "Use A to move left",
                           "Use D to move right",
                           "Access your inventory with E",
                           "Access your map with R",
                           "Use SPACE to jump",
                           "Did you know there is a light mode?",
                           "Did you know there is a dark mode?",
                           "Check us out on GitHub",
                           "Use ESC to exit",
                           "Hold W for 3 seconds to sprint",
                           "Did you know you can change the sound volume in settings?",
                           "Did you know you can change the music volume in settings?",
                           "Did you know you can use L to lock the camera",
                           "Did you know the project now supports controllers?",
                           f"This is Pycraft Version: {self.version}"]
            locat = self.mod_Random__.randint(0, (len(LoadingText)-1))
            text = LoadingText[locat]
            return text
        
    class TextWrap:
        def __init__(self):
            pass
        
        def blit_text(self, text, pos, font, color):
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = font.size(' ')[0]  # The width of a space.
            x, y = pos
            TextHeight = 0
            for line in words:
                for word in line:
                    word_surface = font.render(word, self.aa, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= self.realWidth:
                        TextHeight += word_height
                        x = pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    self.Display.blit(word_surface, (x, y))
                    x += word_width + space
                TextHeight += word_height
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            return TextHeight
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()