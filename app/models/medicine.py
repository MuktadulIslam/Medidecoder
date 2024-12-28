import json
import codecs  # For proper Unicode handling

class MedicineInfo:
    def __init__(self):
        # Load medicine information from JSON with proper UTF-8 encoding
        try:
            with codecs.open('assets/data/medicines.json', 'r', 'utf-8') as f:
                # Convert all keys to lowercase when loading
                data = json.load(f)
                self.medicine_data = {k.lower().strip(): v for k, v in data.items()}
        except FileNotFoundError:
            print("Warning: medicines.json not found")
            self.medicine_data = {}
    
    def clean_medicine_name(self, name):
        """Clean up medicine name for matching"""
        # Convert to lowercase
        name = name.lower()
        # Remove extra spaces
        name = name.strip()
        return name
    
    def get_info(self, medicine_name):
        """Get information about a medicine"""
        # Clean the medicine name
        medicine_name = self.clean_medicine_name(medicine_name)
        
        # Try to find an exact match first
        if medicine_name in self.medicine_data:
            info = self.medicine_data[medicine_name]
            # Print for debugging
            print(f"Found medicine: {medicine_name}")
            print(f"Bengali name: {info.get('bg_name', 'Not found')}")
            print(f"Bengali generic name: {info.get('bg_generic_name', 'Not found')}")
            return info
        
        # If no exact match, try to find a partial match
        for key in self.medicine_data.keys():
            if medicine_name in key or key in medicine_name:
                info = self.medicine_data[key]
                # Print for debugging
                print(f"Found partial match: {key}")
                print(f"Bengali name: {info.get('bg_name', 'Not found')}")
                print(f"Bengali generic name: {info.get('bg_generic_name', 'Not found')}")
                return info
        
        # Return default values if no match found
        return {
            'generic_name': 'Unknown',
            'usage': 'Information not available',
            'bg_name': 'ঔষধের নাম পাওয়া যায়নি',  # Default Bengali text
            'bg_generic_name': 'জেনেরিক নাম পাওয়া যায়নি'  # Default Bengali text
        }