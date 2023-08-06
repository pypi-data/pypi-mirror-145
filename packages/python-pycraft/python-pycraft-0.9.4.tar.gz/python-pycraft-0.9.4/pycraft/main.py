print("Loaded <Pycraft_main>")
class Startup:
    def __init__(Class_Startup_variables):
        try:
            import tkinter as tk
            Class_Startup_variables.mod_Tkinter__tk = tk # [Class_Startup_variables] mod (module) (module name) (subsection of module) (name references)
            from tkinter import messagebox
            Class_Startup_variables.mod_Tkinter_messagebox_ = messagebox
            from PIL import Image, ImageFilter
            Class_Startup_variables.mod_PIL_Image_ = Image
            Class_Startup_variables.mod_PIL_ImageFilter_ = ImageFilter
            import pygame
            Class_Startup_variables.mod_Pygame__ = pygame
            import numpy
            Class_Startup_variables.mod_Numpy__ = numpy
            import os
            Class_Startup_variables.mod_OS__ = os
            import sys
            Class_Startup_variables.mod_Sys__ = sys
            import random
            Class_Startup_variables.mod_Random__ = random
            import time
            Class_Startup_variables.mod_Time__ = time
            import platform
            Class_Startup_variables.mod_Platform__ = platform
            import moderngl
            Class_Startup_variables.mod_ModernGL__ = moderngl
            import moderngl_window
            Class_Startup_variables.mod_ModernGL_window_ = moderngl_window
            import pyautogui
            Class_Startup_variables.mod_Pyautogui__ = pyautogui
            import psutil
            Class_Startup_variables.mod_Psutil__ = psutil
            import timeit
            Class_Startup_variables.mod_Timeit__ = timeit
            import subprocess
            Class_Startup_variables.mod_Subprocess__ = subprocess
            import traceback
            Class_Startup_variables.mod_Traceback__ = traceback
            import datetime
            Class_Startup_variables.mod_Datetime__ = datetime
            import ctypes
            Class_Startup_variables.mod_Ctypes__ = ctypes
            import json
            Class_Startup_variables.mod_JSON__ = json
            import threading
            Class_Startup_variables.mod_Threading__ = threading
            import cpuinfo
            Class_Startup_variables.mod_CPUinfo__ = cpuinfo
            import GPUtil
            Class_Startup_variables.mod_GPUtil__ = GPUtil
            from pyrr import Matrix44
            Class_Startup_variables.mod_Pyrr_Matrix44_ = Matrix44
            Class_Startup_variables.mod_urllib_request_ = None
            from pyjoystick.sdl2 import run_event_loop
            Class_Startup_variables.mod_pyjoystick_run_event_loop_ = run_event_loop
            import pyjoystick
            Class_Startup_variables.mod_pyjoystick__ = pyjoystick
            
            moderngl.create_standalone_context()
            
            os.environ['SDL_VIDEO_CENTERED'] = '1'

            Class_Startup_variables.mod_Pygame__.init()
            
            Class_Startup_variables.base_folder = os.path.dirname(__file__)
            
            if "site-packages" in Class_Startup_variables.base_folder or "dist-packages" in Class_Startup_variables.base_folder:
                from pycraft import PycraftStartupTest
                Class_Startup_variables.mod_PycraftStartupTest__ = PycraftStartupTest
                from pycraft import StartupAnimation
                Class_Startup_variables.mod_StartupAnimation__ = StartupAnimation
                from pycraft import DisplayUtils
                Class_Startup_variables.mod_DisplayUtils__ = DisplayUtils
                from pycraft import GetSavedData
                Class_Startup_variables.mod_GetSavedData__ = GetSavedData
                from pycraft import ThemeUtils
                Class_Startup_variables.mod_ThemeUtils__ = ThemeUtils
                from pycraft import HomeScreen
                Class_Startup_variables.mod_HomeScreen__ = HomeScreen
                from pycraft import SoundUtils
                Class_Startup_variables.mod_SoundUtils__ = SoundUtils
                from pycraft import DrawingUtils
                Class_Startup_variables.mod_DrawingUtils__ = DrawingUtils
                from pycraft import CaptionUtils
                Class_Startup_variables.mod_CaptionUtils__ = CaptionUtils
                from pycraft import Credits
                Class_Startup_variables.mod_Credits__ = Credits
                from pycraft import TkinterUtils
                Class_Startup_variables.mod_TkinterUtils__ = TkinterUtils
                from pycraft import Achievements
                Class_Startup_variables.mod_Achievements__ = Achievements
                from pycraft import CharacterDesigner
                Class_Startup_variables.mod_CharacterDesigner__ = CharacterDesigner
                from pycraft import Settings
                Class_Startup_variables.mod_Settings__ = Settings
                from pycraft import Benchmark
                Class_Startup_variables.mod_Benchmark__ = Benchmark
                from pycraft import ExBenchmark
                Class_Startup_variables.mod_ExBenchmark__ = ExBenchmark
                from pycraft import GLWindowUtils
                Class_Startup_variables.mod_Base__ = GLWindowUtils
                from pycraft import ShareDataUtil
                Class_Startup_variables.mod_Globals__ = ShareDataUtil
                from pycraft import TextUtils
                Class_Startup_variables.mod_TextUtils__ = TextUtils
                from pycraft import Inventory
                Class_Startup_variables.mod_Inventory__ = Inventory
                from pycraft import ImageUtils
                Class_Startup_variables.mod_ImageUtils__ = ImageUtils
                from pycraft import MapGUI
                Class_Startup_variables.mod_MapGUI__ = MapGUI
                from pycraft import ThreadingUtil
                Class_Startup_variables.mod_ThreadingUtil__ = ThreadingUtil
                from pycraft import IntegratedInstaller
                Class_Startup_variables.mod_IntegInstaller__ = IntegratedInstaller
                from pycraft import ErrorUtils
                Class_Startup_variables.mod_ErrorUtils__ = ErrorUtils
                from pycraft import Installer_main
                Class_Startup_variables.mod_Installer__ = Installer_main
                from pycraft import JoystickUtils
                Class_Startup_variables.mod_JoystickUtil__ = JoystickUtils
            else:
                import PycraftStartupTest
                Class_Startup_variables.mod_PycraftStartupTest__ = PycraftStartupTest
                import StartupAnimation
                Class_Startup_variables.mod_StartupAnimation__ = StartupAnimation
                import DisplayUtils
                Class_Startup_variables.mod_DisplayUtils__ = DisplayUtils
                import GetSavedData
                Class_Startup_variables.mod_GetSavedData__ = GetSavedData
                import ThemeUtils
                Class_Startup_variables.mod_ThemeUtils__ = ThemeUtils
                import HomeScreen
                Class_Startup_variables.mod_HomeScreen__ = HomeScreen
                import SoundUtils
                Class_Startup_variables.mod_SoundUtils__ = SoundUtils
                import DrawingUtils
                Class_Startup_variables.mod_DrawingUtils__ = DrawingUtils
                import CaptionUtils
                Class_Startup_variables.mod_CaptionUtils__ = CaptionUtils
                import Credits
                Class_Startup_variables.mod_Credits__ = Credits
                import TkinterUtils
                Class_Startup_variables.mod_TkinterUtils__ = TkinterUtils
                import Achievements
                Class_Startup_variables.mod_Achievements__ = Achievements
                import CharacterDesigner
                Class_Startup_variables.mod_CharacterDesigner__ = CharacterDesigner
                import Settings
                Class_Startup_variables.mod_Settings__ = Settings
                import Benchmark
                Class_Startup_variables.mod_Benchmark__ = Benchmark
                import ExBenchmark
                Class_Startup_variables.mod_ExBenchmark__ = ExBenchmark
                import GLWindowUtils
                Class_Startup_variables.mod_Base__ = GLWindowUtils
                import ShareDataUtil
                Class_Startup_variables.mod_Globals__ = ShareDataUtil
                import TextUtils
                Class_Startup_variables.mod_TextUtils__ = TextUtils
                import Inventory
                Class_Startup_variables.mod_Inventory__ = Inventory
                import ImageUtils
                Class_Startup_variables.mod_ImageUtils__ = ImageUtils
                import MapGUI
                Class_Startup_variables.mod_MapGUI__ = MapGUI
                import ThreadingUtil
                Class_Startup_variables.mod_ThreadingUtil__ = ThreadingUtil
                import IntegratedInstaller
                Class_Startup_variables.mod_IntegInstaller__ = IntegratedInstaller
                import ErrorUtils
                Class_Startup_variables.mod_ErrorUtils__ = ErrorUtils
                import Installer_main
                Class_Startup_variables.mod_Installer__ = Installer_main
                import JoystickUtils
                Class_Startup_variables.mod_JoystickUtil__ = JoystickUtils

            Class_Startup_variables.aa = True
            Class_Startup_variables.AccentCol = (237, 125, 49)
            Class_Startup_variables.AnimateLogo = False
            Class_Startup_variables.aFPS = 0
            Class_Startup_variables.BackgroundCol = [30, 30, 30]
            Class_Startup_variables.cameraANGspeed = 3.5
            Class_Startup_variables.clock = pygame.time.Clock()
            Class_Startup_variables.ctx = 0
            Class_Startup_variables.Command = None
            Class_Startup_variables.ConnectionPermission = None
            Class_Startup_variables.ConnectionStatus = False
            Class_Startup_variables.crash = False
            Class_Startup_variables.current_time = Class_Startup_variables.mod_Datetime__.datetime.now()
            Class_Startup_variables.currentDate = f"{Class_Startup_variables.current_time.day}/{Class_Startup_variables.current_time.month}/{Class_Startup_variables.current_time.year}"
            Class_Startup_variables.CurrentlyDisplayingMessage = False
            Class_Startup_variables.CurrentMemoryUsage = 0
            Class_Startup_variables.CurrentlyPlaying = None
            Class_Startup_variables.CurrentResourceCheckTime = 0

            Class_Startup_variables.Data_aFPS = []
            Class_Startup_variables.Data_aFPS_Max = 1

            Class_Startup_variables.Data_CPUUsE = []
            Class_Startup_variables.Data_CPUUsE_Max = 1

            Class_Startup_variables.Data_eFPS = []
            Class_Startup_variables.Data_eFPS_Max = 1

            Class_Startup_variables.Data_MemUsE = []
            Class_Startup_variables.Data_MemUsE_Max = 1
            
            Class_Startup_variables.Devmode = 0
            Class_Startup_variables.Display = 0
            Class_Startup_variables.DeviceConnected = False
            Class_Startup_variables.DeviceConnected_Update = False
            Class_Startup_variables.eFPS = 60
            Class_Startup_variables.ErrorMessage = None
            Class_Startup_variables.FancyGraphics = True
            Class_Startup_variables.FanPart = True
            Class_Startup_variables.FontCol = (255, 255, 255)
            Class_Startup_variables.FOV = 70
            Class_Startup_variables.FromPlay = False
            Class_Startup_variables.FromGameGUI = False
            Class_Startup_variables.Fullscreen = False
            Class_Startup_variables.FPS = 60
            Class_Startup_variables.FullscreenX, Class_Startup_variables.FullscreenY = pyautogui.size()
            Class_Startup_variables.GameEngine_Control = [[False, False], [False, False], [False, False], [False, False]]
            Class_Startup_variables.GameError = None
            Class_Startup_variables.GetOutdated = [False, False]
            Class_Startup_variables.Iteration = 1
            Class_Startup_variables.InstallLocation = None
            Class_Startup_variables.JoystickConfirm = False
            Class_Startup_variables.JoystickConfirm_toggle = False
            Class_Startup_variables.JoystickExit = False
            Class_Startup_variables.JoystickMouse = [0, 0]
            Class_Startup_variables.lastRun = "29/09/2021"
            Class_Startup_variables.Load3D = True
            Class_Startup_variables.LoadMusic = True
            Class_Startup_variables.LoadTime = [0, 1]
            Class_Startup_variables.MovementSpeed = 1
            Class_Startup_variables.music = True
            Class_Startup_variables.musicVOL = 5
            Class_Startup_variables.Outdated = False
            Class_Startup_variables.platform = Class_Startup_variables.mod_Platform__.system()
            Class_Startup_variables.Project_Sleeping = False
            Class_Startup_variables.Progress_Line = []
            Class_Startup_variables.ProgressMessageText = "Initiating"
            Class_Startup_variables.realHeight = 720
            Class_Startup_variables.realWidth = 1280
            Class_Startup_variables.RecommendedFPS = 60
            Class_Startup_variables.RenderFOG = True
            Class_Startup_variables.RunFullStartup = False
            Class_Startup_variables.ResourceCheckTime = [0, 0]
            Class_Startup_variables.SecondFontCol = (100, 100, 100)
            Class_Startup_variables.SavedWidth = 1280
            Class_Startup_variables.SavedHeight = 720
            Class_Startup_variables.ShapeCol = (80, 80, 80)
            Class_Startup_variables.sound = True
            Class_Startup_variables.soundVOL = 75
            Class_Startup_variables.Stop_Thread_Event = Class_Startup_variables.mod_Threading__.Event()
            Class_Startup_variables.SettingsPreference = "Medium"
            Class_Startup_variables.theme = False
            Class_Startup_variables.Timer = 0
            if Class_Startup_variables.platform == "Linux":
                Class_Startup_variables.TitleFont = Class_Startup_variables.mod_Pygame__.font.Font(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder, ("Fonts//Book Antiqua.ttf")), 60)
                Class_Startup_variables.WindowIcon = Class_Startup_variables.mod_Pygame__.image.load(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder, ("Resources//General_Resources//Icon.png")))
            else:
                Class_Startup_variables.WindowIcon = Class_Startup_variables.mod_Pygame__.image.load(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder, ("Resources\\General_Resources\\Icon.png")))
                Class_Startup_variables.TitleFont = Class_Startup_variables.mod_Pygame__.font.Font(Class_Startup_variables.mod_OS__.path.join(Class_Startup_variables.base_folder, ("Fonts\\Book Antiqua.ttf")), 60)
            Class_Startup_variables.TotalNumUpdate = 0
            Class_Startup_variables.Total_move_x = 0
            Class_Startup_variables.Total_move_y = 0
            Class_Startup_variables.Total_move_z = 0
            Class_Startup_variables.Total_Vertices = 0
            Class_Startup_variables.UseMouseInput = True
            Class_Startup_variables.Updated = False
            Class_Startup_variables.version = "0.9.4"
            Class_Startup_variables.X = 0
            Class_Startup_variables.Y = 0
            Class_Startup_variables.Z = 0

            Class_Startup_variables.Thread_StartLongThread = Class_Startup_variables.mod_Threading__.Thread(target=Class_Startup_variables.mod_ThreadingUtil__.ThreadingUtils.StartVariableChecking, args=(Class_Startup_variables,))
            Class_Startup_variables.Thread_StartLongThread.daemon = True
            Class_Startup_variables.Thread_StartLongThread.start()
            Class_Startup_variables.Thread_StartLongThread.name = "Thread_StartLongThread"

            Class_Startup_variables.Thread_GetCPUMetrics = Class_Startup_variables.mod_Threading__.Thread(target=Class_Startup_variables.mod_ThreadingUtil__.ThreadingUtils.StartCPUlogging, args=(Class_Startup_variables,))
            Class_Startup_variables.Thread_GetCPUMetrics.daemon = True
            Class_Startup_variables.Thread_GetCPUMetrics.start()
            Class_Startup_variables.Thread_GetCPUMetrics.name = "Thread_GetCPUMetrics"

            Class_Startup_variables.Thread_AdaptiveMode = Class_Startup_variables.mod_Threading__.Thread(target=Class_Startup_variables.mod_ThreadingUtil__.ThreadingUtils.AdaptiveMode, args=(Class_Startup_variables,))
            Class_Startup_variables.Thread_AdaptiveMode.daemon = True
            Class_Startup_variables.Thread_AdaptiveMode.start()
            Class_Startup_variables.Thread_AdaptiveMode.name = "Thread_AdaptiveMode"
            
            Class_Startup_variables.Thread_JoystickEvents = Class_Startup_variables.mod_Threading__.Thread(target=Class_Startup_variables.mod_JoystickUtil__.EstablishJoystickConnection.JoystickEvents, args=(Class_Startup_variables,))
            Class_Startup_variables.Thread_JoystickEvents.daemon = True
            Class_Startup_variables.Thread_JoystickEvents.start()
            Class_Startup_variables.Thread_JoystickEvents.name = "Thread_JoystickEvents"
            
            Class_Startup_variables.mod_Globals__.Share.initialize(Class_Startup_variables)
            
            if "site-packages" in Class_Startup_variables.base_folder or "dist-packages" in Class_Startup_variables.base_folder:
                from pycraft import GameEngine
                Class_Startup_variables.mod_MainGameEngine__ = GameEngine
            else:
                import GameEngine
                Class_Startup_variables.mod_MainGameEngine__ = GameEngine
        except Exception as Message:
            try:
                import tkinter as tk
                import sys
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Startup Fail", str(Message))
                sys.exit()
            except Exception as Message:
                sys.exit()

class Initialize:
    def Start():
        global Class_Startup_variables
        Class_Startup_variables = Startup()
        try:
            Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.ReadMainSave(Class_Startup_variables)
        except Exception as Message:
            Report = Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.RepairLostSave(Class_Startup_variables)
            ErrorString = f"Unable to access saved data, we have atttempted to repair the missing data, please try again\n\nMore Details:\n{Message}"
            Class_Startup_variables.ErrorMessage = f"main: {ErrorString}"
            Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        Class_Startup_variables.mod_GetSavedData__.FixInstaller.GetInstallLocation(Class_Startup_variables)
        if Class_Startup_variables.InstallLocation == None:
            Class_Startup_variables.mod_GetSavedData__.FixInstaller.SetInstallLocation(Class_Startup_variables)
            
        if Class_Startup_variables.ConnectionPermission == None:
            Class_Startup_variables.mod_TkinterUtils__.TkinterInfo.GetPermissions(Class_Startup_variables)

        if not Class_Startup_variables.currentDate == Class_Startup_variables.lastRun or Class_Startup_variables.crash == True:
            Class_Startup_variables.GetOutdated = [False, True]
            if Class_Startup_variables.ConnectionPermission == True:
                import urllib.request
                Class_Startup_variables.mod_urllib_request_ = urllib.request
                Class_Startup_variables.ConnectionStatus = Class_Startup_variables.mod_IntegInstaller__.CheckConnection.test(Class_Startup_variables)
                if Class_Startup_variables.ConnectionStatus == True:
                    Class_Startup_variables.Thread_Get_Outdated = Class_Startup_variables.mod_Threading__.Thread(target=Class_Startup_variables.mod_IntegInstaller__.IntegInstaller.CheckVersions, args=(Class_Startup_variables,))
                    Class_Startup_variables.Thread_Get_Outdated.daemon = True
                    Class_Startup_variables.Thread_Get_Outdated.start()
                    Class_Startup_variables.Thread_Get_Outdated.name = "Thread_Get_Outdated"

        Class_Startup_variables.mod_DisplayUtils__.DisplayUtils.SetDisplay(Class_Startup_variables)
        if not Class_Startup_variables.ErrorMessage == None:
            Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        Class_Startup_variables.mod_PycraftStartupTest__.StartupTest.PycraftSelfTest(Class_Startup_variables)
        if not Class_Startup_variables.ErrorMessage == None:
            Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        if Class_Startup_variables.theme == False:
            Class_Startup_variables.mod_ThemeUtils__.DetermineThemeColours.GetThemeGUI(Class_Startup_variables)
            if not Class_Startup_variables.ErrorMessage == None:
                Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        Class_Startup_variables.mod_ThemeUtils__.DetermineThemeColours.GetColours(Class_Startup_variables)
        if not Class_Startup_variables.ErrorMessage == None:
            Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        Class_Startup_variables.mod_Pygame__.mouse.set_visible(False)
        Class_Startup_variables.mod_StartupAnimation__.GenerateStartupScreen.Start(Class_Startup_variables)
        Class_Startup_variables.mod_Pygame__.mouse.set_visible(True)
        if not Class_Startup_variables.ErrorMessage == None:
            Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)

        while True:
            if Class_Startup_variables.Command == "saveANDexit":
                Class_Startup_variables.mod_GetSavedData__.LoadSaveFiles.SaveTOconfigFILE(Class_Startup_variables)
                if not Class_Startup_variables.ErrorMessage == None:
                    Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)
                    
                Class_Startup_variables.mod_Pygame__.quit()
                Class_Startup_variables.mod_Sys__.exit()
            elif Class_Startup_variables.Command == "Credits":
                Class_Startup_variables.mod_Credits__.GenerateCredits.Credits(Class_Startup_variables)
                Class_Startup_variables.Command = "Undefined"
                
            elif Class_Startup_variables.Command == "Achievements":
                Class_Startup_variables.mod_Achievements__.GenerateAchievements.Achievements(Class_Startup_variables)
                Class_Startup_variables.Command = "Undefined"
                        
            elif Class_Startup_variables.Command == "CharacterDesigner":
                Class_Startup_variables.mod_CharacterDesigner__.GenerateCharacterDesigner.CharacterDesigner(Class_Startup_variables)
                Class_Startup_variables.Command = "Undefined"
                
            elif Class_Startup_variables.Command == "Settings":
                Class_Startup_variables.mod_Settings__.GenerateSettings.settings(Class_Startup_variables)
                Class_Startup_variables.Command = "Undefined"
                
            elif Class_Startup_variables.Command == "Benchmark":
                Class_Startup_variables.mod_Benchmark__.GenerateBenchmarkMenu.Benchmark(Class_Startup_variables)
                Class_Startup_variables.Command = "Undefined"
                
            elif Class_Startup_variables.Command == "Play":
                Class_Startup_variables.Command = Class_Startup_variables.mod_MainGameEngine__.CreateEngine.Play(Class_Startup_variables)

                if not Class_Startup_variables.GameError == None:
                    Class_Startup_variables.ErrorMessage = "GameEngine: "+str(Class_Startup_variables.GameError)

                Class_Startup_variables.mod_Pygame__.init()
                Class_Startup_variables.clock = Class_Startup_variables.mod_Pygame__.time.Clock()
                Class_Startup_variables.FromPlay = True
                
                Class_Startup_variables.mod_DisplayUtils__.DisplayUtils.SetDisplay(Class_Startup_variables)
                    
            elif Class_Startup_variables.Command == "Inventory":
                Class_Startup_variables.mod_Inventory__.GenerateInventory.Inventory(Class_Startup_variables)
                Class_Startup_variables.Command = "Play"
                
            elif Class_Startup_variables.Command == "MapGUI":
                Class_Startup_variables.mod_MapGUI__.GenerateMapGUI.MapGUI(Class_Startup_variables)
                Class_Startup_variables.Command = "Play"
                
            elif Class_Startup_variables.Command == "Installer":
                Class_Startup_variables.mod_Pygame__.display.quit()
                Class_Startup_variables.mod_Installer__.RunInstaller.Initialize()
                Class_Startup_variables.mod_Sys__.exit()
                
                
            elif not Class_Startup_variables.ErrorMessage == None:
                Class_Startup_variables.mod_ErrorUtils__.GenerateErrorScreen.ErrorScreen(Class_Startup_variables)
                
            else:
                Class_Startup_variables.Command = Class_Startup_variables.mod_HomeScreen__.GenerateHomeScreen.Home_Screen(Class_Startup_variables)

if __name__ == "__main__":
    print("Started <Pycraft_main>")
    import psutil, sys, time
    counter = 0
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info["name"] == "Pycraft.exe":
            counter += 1
    if counter >= 3:
        sys.exit()
    Initialize.Start()

def QueryVersion():
    return "pycraft v0.9.4"

def start():
    print("Started <Pycraft_main>")
    Initialize.Start()