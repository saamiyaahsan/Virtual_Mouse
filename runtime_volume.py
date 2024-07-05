import pyautogui
import cProfile
import numpy as np

# Define smoothening factor
smoothening = 9
plocy = 0

# Mock pyautogui functions for profiling
def mock_hotkey(key):
    print(f"Mock hotkey called with key: {key}")

# Save the original pyautogui.hotkey function
original_hotkey = pyautogui.hotkey

# Replace pyautogui.hotkey with the mock function
pyautogui.hotkey = mock_hotkey

def handle_volume(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocy

    # Detect the position of the hand in the frame
    hand_center_y = None

    for landmark in hand_landmarks.landmark:
        if hasattr(landmark, 'visibility') and landmark.visibility > 0.5:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            if hand_center_y is None:
                hand_center_y = y
            else:
                hand_center_y = (hand_center_y + y) // 2

    # Adjust volume based on hand movement
    if hand_center_y is not None:
        if plocy == 0:
            plocy = hand_center_y
        clocy = plocy + (hand_center_y - plocy) / smoothening
        plocy = clocy

        # Adjust volume based on hand movement direction
        if clocy < hand_center_y - 10:  # Move hand up to increase volume
            pyautogui.hotkey('f3')
        elif clocy > hand_center_y + 10:  # Move hand down to decrease volume
            pyautogui.hotkey('f2')

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

# Profile the handle_volume function
cProfile.run('handle_volume(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

# Restore the original pyautogui.hotkey function after profiling
pyautogui.hotkey = original_hotkey
