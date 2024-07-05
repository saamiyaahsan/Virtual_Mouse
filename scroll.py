import cv2
import numpy as np
import mediapipe as mp
import pyautogui

# Smoothing factor for cursor movement
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

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
