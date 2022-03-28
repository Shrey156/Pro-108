from itertools import count
import cv2
import mediapipe as mp
cap = cv2.VideoCapture(0)
# hand landmarks points
mp_hands=mp.solutions.hands

# to draw landmarks points
mp_drawing=mp.solutions.drawing_utils

hands=mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)

tip_id=[8,12,16,20]
def count_fingers(img,hand_landmarks,handNo=0):
    if hand_landmarks:
        landmarks=hand_landmarks[handNo].landmark
        fingers=[]
        for i in tip_id:
            # x,y=int(landmarks[i].x*w),int(landmarks[i].y*h)
            # cv2.circle(img, (x,y), 15,(255,0,0),cv2.FILLED)
           
            #get finger tip and bottom y position value
            finger_tip_x=landmarks[i].x
            finger_bottom_x=landmarks[i-2].x
            thumb_tip_y=landmarks[i].y
            thumb_middle_y=landmarks[i-1].y
            thumb_bottom_y=landmarks[i-2].y
            if finger_tip_x<finger_bottom_x:
                # cv2.circle(img, (x,y), 15,(255,0,0),cv2.FILLED)
                fingers.append(True)
            else:
                fingers.append(False)
            if fingers:
                if thumb_tip_y>thumb_middle_y>thumb_bottom_y:
                    text="Like"
                    cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                else:
                    text="Dislike"
                    cv2.putText(img,text,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        
                        
            
def drawLandmarks(img,hand_landmarks):
    if hand_landmarks:
        for i in hand_landmarks:
            mp_drawing.draw_landmarks(img,i,mp_hands.HAND_CONNECTIONS)
    
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    
    results=hands.process(img)
    hand_landmarks=results.multi_hand_landmarks
    drawLandmarks(img,hand_landmarks)
    count_fingers(img,hand_landmarks)
    cv2.imshow("mediaController",img)
    
    key=cv2.waitKey(1)
    if key ==32:
        break
    
cv2.destroyAllWindows()
