if not __name__ == "__main__":
    print("Started <Pycraft_IntegratedInstaller>")
    class IntegInstaller:
        def __init__(self):
            pass

        def CheckVersions(self):
            try:
                if (not self.mod_urllib_request_ == None) and self.ConnectionPermission == True and self.ConnectionStatus == True:
                    List = self.mod_Subprocess__.check_output([self.mod_Sys__.executable, "-m","pip","list","--outdated"], False)

                    for i in range(len(List)):
                        if List[i:i+14] == b"Python-Pycraft":
                            self.Outdated = True
                            self.TotalNumUpdate = 1
                    self.GetOutdated = [True, False]
            except Exception as Message:
                self.ErrorMessage = "IntegratedInstaller > IntegInstaller > CheckVersions: "+str(Message)
                    
                        
    class CheckConnection:
        def __init__(self):
            pass
        
        def test(self):
            try:
                self.mod_urllib_request_.urlopen('https://www.google.com', timeout=1)
                return True
            except Exception as Error:
                return False
                
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()