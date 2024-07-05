# import cv2
# import numpy as np
# import pyautogui
# import cProfile

# # Define the handle_zoom function
# def handle_zoom(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
#     index_x, index_y = None, None
#     thumb_x, thumb_y = None, None

#     for id, landmark in enumerate(hand_landmarks.landmark):
#         x = int(landmark.x * frame_width)
#         y = int(landmark.y * frame_height)

#         if id == 8:  # Index finger tip point number is 8
#             cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
#             index_x = (screen_width / frame_width) * x
#             index_y = (screen_height / frame_height) * y

#         if id == 4:  # Thumb tip point number is 4
#             cv2.circle(img=frame, center=(x, y), radius=15, color=(255, 0, 255))
#             thumb_x = (screen_width / frame_width) * x
#             thumb_y = (screen_height / frame_height) * y

#     if index_x is not None and index_y is not None and thumb_x is not None and thumb_y is not None:
#         # Calculate distance between index and thumb fingers
#         distance = np.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)

#         if distance < 50:  # Zoom in if fingers are close
#             pyautogui.hotkey('ctrl', '+')
#         elif distance > 100:  # Zoom out if fingers are far apart
#             pyautogui.hotkey('ctrl', '-')

# # Mock data for testing
# class MockLandmark:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# class MockHandLandmarks:
#     def __init__(self, landmarks):
#         self.landmark = landmarks

# # Create mock hand landmarks
# mock_landmarks = MockHandLandmarks([
#     MockLandmark(0.1, 0.1),  # Point 0
#     MockLandmark(0.2, 0.2),  # Point 1
#     MockLandmark(0.3, 0.3),  # Point 2
#     MockLandmark(0.4, 0.4),  # Point 3
#     MockLandmark(0.5, 0.5),  # Thumb tip (Point 4)
#     MockLandmark(0.6, 0.6),  # Point 5
#     MockLandmark(0.7, 0.7),  # Point 6
#     MockLandmark(0.8, 0.8),  # Point 7
#     MockLandmark(0.9, 0.9)   # Index tip (Point 8)
# ])

# # Mock frame and dimensions
# frame = np.zeros((480, 640, 3), dtype=np.uint8)
# frame_width = 640
# frame_height = 480
# screen_width = 1920
# screen_height = 1080

# # Profile the handle_zoom function
# cProfile.run('handle_zoom(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

import cv2
import numpy as np
import cProfile

# Define the handle_zoom function
def handle_zoom(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    index_x, index_y = None, None
    thumb_x, thumb_y = None, None

    for id, landmark in enumerate(hand_landmarks.landmark):
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)

        if id == 8:  # Index finger tip point number is 8
            cv2.circle(img=frame, center=(x, y), radius=15, color=(0, 255, 255))
            index_x = (screen_width / frame_width) * x
            index_y = (screen_height / frame_height) * y

        if id == 4:  # Thumb tip point number is 4
            cv2.circle(img=frame, center=(x, y), radius=15, color=(255, 0, 255))
            thumb_x = (screen_width / frame_width) * x
            thumb_y = (screen_height / frame_height) * y

    if index_x is not None and index_y is not None and thumb_x is not None and thumb_y is not None:
        # Calculate distance between index and thumb fingers
        distance = np.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)

        if distance < 50:  # Zoom in if fingers are close
            # pyautogui.hotkey('ctrl', '+')
            print("Zoom In")
        elif distance > 100:  # Zoom out if fingers are far apart
            # pyautogui.hotkey('ctrl', '-')
            print("Zoom Out")

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
    MockLandmark(0.5, 0.5),  # Thumb tip (Point 4)
    MockLandmark(0.6, 0.6),  # Point 5
    MockLandmark(0.7, 0.7),  # Point 6
    MockLandmark(0.8, 0.8),  # Point 7
    MockLandmark(0.9, 0.9)   # Index tip (Point 8)
])

# Mock frame and dimensions
frame = np.zeros((480, 640, 3), dtype=np.uint8)
frame_width = 640
frame_height = 480
screen_width = 1920
screen_height = 1080

# Profile the handle_zoom function
cProfile.run('handle_zoom(mock_landmarks, frame, frame_width, frame_height, screen_width, screen_height)')

