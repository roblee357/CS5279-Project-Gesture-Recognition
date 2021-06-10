import pafy
import csv

import os
import numpy as np
import mediapipe as mp # Import mediapipe
import cv2 # Import opencv

##  If this error: pafy: youtube-dl not found;
##  Run this:      pip install --upgrade youtube-dl

import os, sys
sys.path.append('c:\\users\\roble\\appdata\\roaming\\python\\python37\\site-packages')

class vid:
    def __init__(self,vid_url,title, stime, etime):
        self.vid_url = vid_url
        self.title = title
        self.stime = stime
        self.etime = etime
        self.mp_drawing = mp.solutions.drawing_utils # Drawing helpers
        self.mp_holistic = mp.solutions.holistic # Mediapipe Solutions
        print('initiated')

    def detect(self):
        print('detect')
        with self.mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            cap = cv2.VideoCapture(self.vid_url)
            #cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
            cap.set(cv2.CAP_PROP_POS_MSEC, self.stime)
            # Check if camera opened successfully
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")

            # Read until video is completed
            while(cap.isOpened()):
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:


                    # Recolor Feed
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False        
                    
                    # Make Detections
                    results = holistic.process(image)
                    # print(results.face_landmarks)
                    
                    # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                    
                    # Recolor image back to BGR for rendering
                    image.flags.writeable = True   
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    # 1. Draw face landmarks
                    self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACE_CONNECTIONS, 
                                            self.mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                            self.mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                            )
                    
                    # 2. Right hand
                    self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
                                            self.mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                            self.mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                            )

                    # 3. Left Hand
                    self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
                                            self.mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                            self.mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                            )

                    # 4. Pose Detections
                    self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS, 
                                            self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                            self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                            )

                    # Display the resulting frame
                    # cv2.imshow('Frame',frame)
                    cv2.imshow('Raw Webcam Feed', image)
                    print(cap.get(cv2.CAP_PROP_POS_MSEC))


                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

                    if cap.get(cv2.CAP_PROP_POS_MSEC) > self.etime:
                        break

                # Break the loop
                else: 
                    break

            # When everything done, release the video capture object
            cap.release()

            # Closes all the frames
            cv2.destroyAllWindows()


def main():
    print('main')
    vid_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    title = 'bigBuckBunny'
    stime = 225000
    etime = 230000
    video = vid(vid_url,title,stime,etime)
    video.detect()


if __name__ == '__main__':
    main()