from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.core.text import LabelBase
import os

# Register the Bengali font
font_path = os.path.join('assets', 'fonts', 'Noto-Sans-Bengali.ttf')
LabelBase.register(name='Noto-Sans-Bengali', fn_regular=font_path)

# Load KV files
Builder.load_file('assets/kv/main.kv')
Builder.load_file('assets/kv/main_screen.kv')
Builder.load_file('assets/kv/result_screen.kv')

from app.screens.main_screen import MainScreen
from app.screens.result_screen import ResultScreen

class MediDecodeApp(App):
    # Properties to store prediction results
    medicine_name = StringProperty('')
    generic_name = StringProperty('')
    usage = StringProperty('')
    bg_name = StringProperty('')
    bg_generic_name = StringProperty('')
    
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ResultScreen(name='result'))
        
        return sm

if __name__ == '__main__':
    Window.size = (400, 700)  # Set window size for desktop testing
    MediDecodeApp().run()