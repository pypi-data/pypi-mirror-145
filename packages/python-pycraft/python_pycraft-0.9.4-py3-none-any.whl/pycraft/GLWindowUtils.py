if not __name__ == "__main__":
    print("Started <Pycraft_Base>")

    import moderngl_window as mglw
    from moderngl_window.scene.camera import KeyboardCamera, OrbitCamera


    class CameraWindow(mglw.WindowConfig):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)
            self.camera_enabled = True