import pyautogui

# Smoothing factor for hand movement
smoothening = 9
plocx = 0

def handle_brightness(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocx

    # Detect the position of the hand in the frame
    hand_center_x = None

    for landmark in hand_landmarks.landmark:
        if landmark.HasField('visibility') and landmark.visibility > 0.5:
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
