from kivy.uix.screenmanager import Screen
from kivy.app import App

class ResultScreen(Screen):
    def on_enter(self):
        """Called when screen is entered"""
        app = App.get_running_app()
        
        # Print debug information
        print("\nSetting labels with following data:")
        print(f"Medicine name: {app.medicine_name}")
        print(f"Generic name: {app.generic_name}")
        print(f"Bengali name: {app.bg_name}")
        print(f"Bengali generic name: {app.bg_generic_name}")
        print(f"Usage: {app.usage}")
        
        # Update the labels in the KV file
        self.ids.medicine_name_label.text = app.medicine_name
        self.ids.generic_name_label.text = app.generic_name
        
        # Set Bengali text with proper encoding
        try:
            self.ids.bg_name_label.text = str(app.bg_name)
            self.ids.bg_generic_name_label.text = str(app.bg_generic_name)
        except Exception as e:
            print(f"Error setting Bengali text: {e}")
            self.ids.bg_name_label.text = "Error displaying Bengali text"
            self.ids.bg_generic_name_label.text = "Error displaying Bengali text"
            
        self.ids.usage_label.text = app.usage
    
    def go_back(self):
        """Return to camera screen"""
        self.manager.current = 'main'