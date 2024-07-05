##### (Unoptimized code)  Code 1  #####

import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyaudio
from scroll import handle_scroll
from click import handle_click
from zoom import handle_zoom
from volume import handle_volume
from brightness import handle_brightness

# Initialize Mediapipe and webcam
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()

def detect_gesture():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)

        # Check the recognized command and return the corresponding gesture
        if "scroll" in command:
            return "scroll"
        elif "click" in command:
            return "click"
        elif "zoom" in command:
            return "zoom"
        elif "volume" in command:
            return "volume"
        elif "brightness" in command:
            return "brightness"
        elif "exit" in command:
            return "exit"
        else:
            print("Unrecognized command. Please try again.")
            return None
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            gesture = detect_gesture()
            
            # Exit the program if the gesture is "exit"
            if gesture == "exit":
                cap.release()
                cv2.destroyAllWindows()
                print("Exiting the program.")
                exit()
            
            # Call appropriate function based on the gesture
            if gesture == "scroll":
                handle_scroll(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height)
            elif gesture == "click":
                handle_click(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height)
            elif gesture == "zoom":
                handle_zoom(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height)
            elif gesture == "volume":
                handle_volume(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height)
            elif gesture == "brightness":
                handle_brightness(hand_landmarks, frame, frame_width, frame_height, screen_width, screen_height)
            # Add more elif conditions for additional operations as needed

    cv2.imshow('Virtual Mouse', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()





