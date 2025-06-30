import cv2
import numpy as np
import pygame
import time

# Initialize pygame for sound
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm_sound.mp3")  # Make sure to have this file

def detect_fire(frame):
    """
    Detect fire in the frame using color detection
    """
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for fire color in HSV
    lower_fire = np.array([0, 120, 70])
    upper_fire = np.array([20, 255, 255])
    
    # Threshold the HSV image to get only fire colors
    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    
    # Calculate percentage of fire-colored pixels
    fire_percentage = (np.sum(mask > 0) / mask.size) * 100
    
    return mask, fire_percentage

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    # Check if webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    alarm_playing = False
    last_alarm_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect fire
        fire_mask, fire_percent = detect_fire(frame)
        
        # Display fire percentage
        cv2.putText(frame, f"Fire: {fire_percent:.2f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Trigger alarm if fire is detected (more than 5% of the frame)
        if fire_percent > 5:
            current_time = time.time()
            if not alarm_playing or current_time - last_alarm_time > 3:
                alarm_sound.play()
                alarm_playing = True
                last_alarm_time = current_time
                print("FIRE DETECTED! Playing alarm...")
            
            # Draw warning on frame
            cv2.putText(frame, "FIRE DETECTED!", (frame.shape[1]//4, frame.shape[0]//2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        else:
            if alarm_playing and time.time() - last_alarm_time > 3:
                alarm_sound.stop()
                alarm_playing = False
        
        # Show original frame and fire mask
        cv2.imshow('Fire Detection', frame)
        cv2.imshow('Fire Mask', fire_mask)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()