if not __name__ == "__main__":
    print("Started <Pycraft_JoystickUtils>")
    class EstablishJoystickConnection:
        def __init__(self):
            pass
                
        def JoystickEvents(self):
            def print_add(joy):
                self.DeviceConnected = True
                self.DeviceConnected_Update = True

            def print_remove(joy):
                self.DeviceConnected = False
                self.DeviceConnected_Update = True

            def key_received(key):
                if self.UseMouseInput == False:
                    if self.Command == "Play":
                        if "Button" in str(key) or "Hat" in str(key):
                            self.JoystickConfirm_toggle = not self.JoystickConfirm_toggle
                            if self.JoystickConfirm_toggle == True:
                                if "Button 3" in str(key):
                                    self.GameEngine_Control[3][0] = True
                                else:
                                    self.GameEngine_Control[3][0] = False
                                if "Hat" in str(key):
                                    self.JoystickExit = True
                                else:
                                    self.JoystickExit = False
                                    if "Button 7" in str(key):
                                        self.GameEngine_Control[0][0] = True
                                    elif "Button 6" in str(key):
                                        self.GameEngine_Control[0][1] = True
                                    else:
                                        self.JoystickConfirm = True
                            else:
                                self.JoystickConfirm = False
                            
                        if "Axis" in str(key):
                            if "Axis 3" in str(key):
                                self.GameEngine_Control[1][0] = round(self.mod_pyjoystick__.Key.get_value(key), 2)
                            if "Axis 4" in str(key):
                                self.GameEngine_Control[1][1] = round(self.mod_pyjoystick__.Key.get_value(key), 2)
                            if "Axis 1" in str(key):
                                self.GameEngine_Control[2][0] = round(self.mod_pyjoystick__.Key.get_value(key), 2)
                            if "Axis 0" in str(key):
                                self.GameEngine_Control[2][1] = round(self.mod_pyjoystick__.Key.get_value(key), 2)
                        self.mod_Globals__.Share.initialize_controller(self.GameEngine_Control)
                    else:
                        self.JoystickMouse = [0, 0]
                        if "Button" in str(key):
                            self.JoystickConfirm_toggle = not self.JoystickConfirm_toggle
                            if self.JoystickConfirm_toggle == True:
                                if "Button 3" in str(key):
                                    self.JoystickExit = True
                                else:
                                    self.JoystickExit = False
                                    self.JoystickConfirm = True
                            else:
                                self.JoystickConfirm = False
                        
                        if "Hat" in str(key):
                            self.JoystickMouse = [0, 0]
                            if "Right" in str(key):
                                self.JoystickMouse[0] = self.MovementSpeed
                            if "Left" in str(key):
                                self.JoystickMouse[0] = -self.MovementSpeed
                                
                            if  "Up" in str(key):
                                self.JoystickMouse[1] = -self.MovementSpeed
                            if  "Down" in str(key):
                                self.JoystickMouse[1] = self.MovementSpeed
                    
            try:
                self.mod_pyjoystick_run_event_loop_(print_add, print_remove, key_received)
            except Exception as Message:
                self.ErrorMessage = "JoystickUtils > GenerateHomeScreen > JoystickEvents: "+ str(Message)
else:
    print("You need to run this as part of Pycraft")
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Startup Fail", "You need to run this as part of Pycraft, please run the 'main.py' file")
    quit()