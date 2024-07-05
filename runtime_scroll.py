import cv2
import numpy as np
import mediapipe as mp
import cProfile
import pyautogui

# Smoothing factor for cursor movement
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

# Mock pyautogui functions for profiling
def mock_moveTo(x, y):
    print(f"Mock moveTo called with x: {x}, y: {y}")

def mock_scroll(amount):
    print(f"Mock scroll called with amount: {amount}")

# Save the original pyautogui functions
original_moveTo = pyautogui.moveTo
original_scroll = pyautogui.scroll

# Replace pyautogui functions with the mock functions
pyautogui.moveTo = mock_moveTo
pyautogui.scroll = mock_scroll

def handle_scroll(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocx, plocy, clocx, clocy
    for id, landmark in enumerate(hand_landmarks.landmark):
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)

        if id == 8:  # Index finger tip point number is 8
            cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
            index_x = (screen_width / frame_width) * x
            index_y = (screen_height / frame_height) * y
            clocx = plocx + (index_x - plocx) / smoothening
            clocy = plocy + (index_y - plocy) / smoothening
            pyautogui.moveTo(clocx, clocy)
            plocx, plocy = clocx, clocy

        if id == 12:  # Middle finger tip point number is 12
            cv2.circle(img=frame, center=(x, y), radius=15, color=(255, 0, 255))
            middle_x = (screen_width / frame_width) * x
            middle_y = (screen_height / frame_height) * y
            if middle_y < index_y:  # Scroll up
                pyautogui.scroll(10)
            elif middle_y > index_y:  # Scroll down
                pyautogui.scroll(-10)

# Mock data for testing
class MockLandmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockHandLandmarks:
    def __init__(self, landmarks):
        self.landmark = landmarks

# Create mock hand landmarks
mock_landmarks = MockHandLandmarks([
    MockLandmark(0.1, 0.1),  # Point 0
    MockLandmark(0.2, 0.2),  # Point 1
    MockLandmark(0.3, 0.3),  # Point 2
    MockLandmark(0.4, 0.4),  # Point 3
    MockLandmark(0.5, 0.5),  # Point 4
    MockLandmark(0.6, 0.6),  # Point 5
    MockLandmark(0.7, 0.7),  # Point 6
    MockLandmark(0.8, 0.8),  # Point 7
    MockLandmark(0.9, 0.9),  # Index tip (Point 8)
    MockLandmark(1.0, 1.0)   # Middle tip (Point 12)
])

# Mock frame and dimensions
frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_width = 640
frame_height = 480
screen_width = 1920
screen_height = 1080

# Profile the handle_scroll function
cProfile.run('handle_scroll(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

# Restore the original pyautogui functions after profiling
pyautogui.moveTo = original_moveTo
pyautogui.scroll = original_scroll
