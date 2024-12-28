from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.app import App
import cv2
import numpy as np
from app.utils.ml_handler import MLHandler
from app.utils.camera import CameraHandler
from app.models.medicine import MedicineInfo

class MainScreen(Screen):
    camera_preview = ObjectProperty(None)
    ml_handler = MLHandler()
    camera_handler = CameraHandler()
    medicine_info = MedicineInfo()
    status_label = ObjectProperty(None)
    
    def on_enter(self):
        """Called when screen is entered"""
        self.camera_handler.start()
        Clock.schedule_interval(self.update_preview, 1.0 / 30.0)  # 30 FPS
        if self.status_label:
            self.status_label.text = "Point camera at prescription"
    
    def on_leave(self):
        """Called when screen is exited"""
        Clock.unschedule(self.update_preview)
        self.camera_handler.stop()
    
    def update_preview(self, dt):
        """Update camera preview"""
        frame = self.camera_handler.get_frame()
        if frame is not None:
            # Convert frame to texture for Kivy
            buf = cv2.flip(frame, 0).tostring()
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_preview.texture = texture
    
    def capture_image(self):
        """Capture and process image"""
        if self.status_label:
            self.status_label.text = "Processing..."
            
        frame = self.camera_handler.get_frame()
        if frame is not None:
            # Process image with ML model
            medicine_name = self.ml_handler.predict(frame)
            
            # Get medicine information
            info = self.medicine_info.get_info(medicine_name.lower())
            
            # Store results in app
            app = App.get_running_app()
            app.medicine_name = medicine_name
            app.generic_name = info.get('generic_name', 'Not found')
            app.usage = info.get('usage', 'Information not available')
            app.bg_name = info.get('bg_name', '')
            app.bg_generic_name = info.get('bg_generic_name', '')
            
            # Switch to result screen
            self.manager.current = 'result'