import cv2
import pyautogui

# Smoothing factor for cursor movement
smoothening = 9
plocx, plocy = 0, 0
clocx, clocy = 0, 0

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

        if id == 4:  # Thumb tip point number is 4==
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

