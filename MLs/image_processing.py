import cv2
import numpy as np

class ImageProcessor:
    
    def __init__(self, frame):
        self.frame = frame

    def process_image(self, server):
        print("Inside process_image method")
        while True:
            frame = server.frame_queue.get()
            if frame is None:
                break
            array = ["a"] #, "s", "d", "q", "w", "e", "z", "x"]
            server.next_move = np.random.choice(array)
            self.frame = frame  # Update self.frame with the new frame data
            self.frame = cv2.resize(self.frame, (640, 320))
            cv2.imshow('stream', self.frame)
            cv2.waitKey(1)

            