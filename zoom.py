import cv2
import numpy as np
import pyautogui

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
            pyautogui.hotkey('ctrl', '+')
        elif distance > 100:  # Zoom out if fingers are far apart
            pyautogui.hotkey('ctrl', '-')

