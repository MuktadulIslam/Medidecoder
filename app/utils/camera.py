import cv2

class CameraHandler:
    def __init__(self):
        self.capture = None
    
    def start(self):
        """Start camera capture"""
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)  # Use default camera
            if self.capture.isOpened():
                # Set camera resolution
                self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def stop(self):
        """Stop camera capture"""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
    
    def get_frame(self):
        """Get current frame from camera"""
        if self.capture is not None and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                return frame
        return None