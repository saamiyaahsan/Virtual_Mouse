import pyautogui

# Define smoothening factor
smoothening = 9

def handle_volume(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height):
    global plocy

    # Detect the position of the hand in the frame
    hand_center_y = None

    for landmark in hand_landmarks.landmark:
        if landmark.HasField('visibility') and landmark.visibility > 0.5:
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

