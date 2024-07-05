import cv2
import pyautogui
import numpy as np
import cProfile

# Smoothing factor for cursor movement
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

# Mock pyautogui functions for profiling
def mock_moveTo(x, y):
    print(f"Mock moveTo called with coordinates: ({x}, {y})")

def mock_click():
    print("Mock click called")

def mock_doubleClick():
    print("Mock doubleClick called")

def mock_sleep(seconds):
    print(f"Mock sleep called for {seconds} seconds")

# Save the original pyautogui functions
original_moveTo = pyautogui.moveTo
original_click = pyautogui.click
original_doubleClick = pyautogui.doubleClick
original_sleep = pyautogui.sleep

# Replace pyautogui functions with the mock functions
pyautogui.moveTo = mock_moveTo
pyautogui.click = mock_click
pyautogui.doubleClick = mock_doubleClick
pyautogui.sleep = mock_sleep

def handle_click(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocx, plocy, clocx, clocy
    thumb_x = thumb_y = index_x = index_y = pinky_x = pinky_y = 0

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

        if id == 4:  # Thumb tip point number is 4
            cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
            thumb_x = (screen_width / frame_width) * x
            thumb_y = (screen_height / frame_height) * y
            if abs(index_y - thumb_y) < 70:  # Adjust threshold as needed
                pyautogui.click()
                pyautogui.sleep(1)

        if id == 20:  # Pinky tip point number is 20
            pinky_x = (screen_width / frame_width) * x
            pinky_y = (screen_height / frame_height) * y

    # Check if thumb and pinky are joined
    if abs(thumb_y - pinky_y) < 70:  # Adjust threshold as needed
        pyautogui.doubleClick()
        pyautogui.sleep(1)

# Mock data for testing
class MockLandmark:
    def __init__(self, x, y, visibility=1.0):
        self.x = x
        self.y = y
        self.visibility = visibility

class MockHandLandmarks:
    def __init__(self, landmarks):
        self.landmark = landmarks

# Create mock hand landmarks
mock_landmarks = MockHandLandmarks([
    MockLandmark(0.1, 0.1),  # Point 0
    MockLandmark(0.2, 0.2),  # Point 1
    MockLandmark(0.3, 0.3, visibility=0.6),  # Point 2 (visible)
    MockLandmark(0.4, 0.4, visibility=0.6),  # Point 3 (visible)
    MockLandmark(0.5, 0.5, visibility=0.6),  # Point 4 (visible, thumb tip)
    MockLandmark(0.6, 0.6),  # Point 5
    MockLandmark(0.7, 0.7),  # Point 6
    MockLandmark(0.8, 0.8, visibility=0.6),  # Point 7
    MockLandmark(0.9, 0.9, visibility=0.6),  # Point 8 (visible, index finger tip)
    MockLandmark(1.0, 1.0),  # Point 9
    MockLandmark(0.3, 0.3),  # Point 10
    MockLandmark(0.4, 0.4),  # Point 11
    MockLandmark(0.5, 0.5),  # Point 12
    MockLandmark(0.6, 0.6),  # Point 13
    MockLandmark(0.7, 0.7),  # Point 14
    MockLandmark(0.8, 0.8),  # Point 15
    MockLandmark(0.9, 0.9),  # Point 16
    MockLandmark(1.0, 1.0),  # Point 17
    MockLandmark(0.3, 0.3),  # Point 18
    MockLandmark(0.4, 0.4),  # Point 19
    MockLandmark(0.5, 0.5, visibility=0.6)   # Point 20 (visible, pinky tip)
])

# Mock frame and dimensions
frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_width = 640
frame_height = 480
screen_width = 1920
screen_height = 1080

# Profile the handle_click function
cProfile.run('handle_click(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

# Restore the original pyautogui functions after profiling
pyautogui.moveTo = original_moveTo
pyautogui.click = original_click
pyautogui.doubleClick = original_doubleClick
pyautogui.sleep = original_sleep
