import pyautogui
import cProfile
import cv2
import numpy as np
import mediapipe as mp

# Smoothing factor for hand movement
smoothening = 9
plocx = 0

# Mock pyautogui functions for profiling
def mock_hotkey(key):
    print(f"Mock hotkey called with key: {key}")

# Save the original pyautogui.hotkey function
original_hotkey = pyautogui.hotkey

# Replace pyautogui.hotkey with the mock function
pyautogui.hotkey = mock_hotkey

def handle_brightness(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocx

    # Detect the position of the hand in the frame
    hand_center_x = None

    for landmark in hand_landmarks.landmark:
        if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            if hand_center_x is None:
                hand_center_x = x
            else:
                hand_center_x = (hand_center_x + x) // 2

    # Adjust brightness based on hand movement
    if hand_center_x is not None:
        if plocx == 0:
            plocx = hand_center_x
        clocx = plocx + (hand_center_x - plocx) / smoothening
        plocx = clocx

        # Adjust brightness based on hand movement direction
        brightness_change = (clocx - frame_width / 2) / (frame_width / 2)  # Normalize to [-1, 1]
        brightness_change *= 20  # Adjust sensitivity as needed
        if brightness_change > 0:  # Increase brightness
            pyautogui.hotkey('f12')
        elif brightness_change < 0:  # Decrease brightness
            pyautogui.hotkey('f11')

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
    MockLandmark(0.4, 0.4, visibility=0.6)   # Point 3 (visible)
])

# Mock frame and dimensions
frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_width = 640
frame_height = 480
screen_width = 1920
screen_height = 1080

# Profile the handle_brightness function
cProfile.run('handle_brightness(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

# Restore the original pyautogui.hotkey function after profiling
pyautogui.hotkey = original_hotkey
