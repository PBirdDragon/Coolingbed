#내가 작성하고 있는 코드

import cv2
import mediapipe as mp
import math
from cvzone.FaceMeshModule import FaceMeshDetector


mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils #정상 작동 여부 확인을 위해 mediapipe의 drawing 사용

cap = cv2.VideoCapture(0) #openCV를 이용해서 웹캠의 입력을 cap에 입력
detector = FaceMeshDetector(maxFaces=1) 

 
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("카메라에서 추적할 수 없습니다.")
        break
    frame, faces = detector.findFaceMesh(frame, draw=False)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #이미지를 RGBB로 변환
    results = pose.process(rgb_frame)
    
    if results.pose_landmarks and faces:
        
        #카메라와 눈 사이의 거리를 측정
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]
        cv2.line(frame, pointLeft, pointRight, (0, 200, 0), 3)
        cv2.circle(frame, pointLeft, 5, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, pointRight, 5, (255, 0, 255), cv2.FILLED)
        iris_distance, _ = detector.findDistance(pointLeft, pointRight) #카메라 상의 두 눈사이의 거리
        real_iris_distance = 7.5 #실제 눈 사이의 거리 cm
        correction_iris = 480 #보정계수
        distance_between_cam_and_iris = (real_iris_distance * correction_iris) / iris_distance #카메라와 눈 사이의 거리
        
        #카메라와 어깨 사이의 거리를 측정
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        shoulder_left = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_right = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        shoulder_distance = math.sqrt((shoulder_right.x - shoulder_left.x)**2 + (shoulder_right.y - shoulder_left.y)**2) #카메라 상의 두 어깨 사이의 거리
        real_shoulder_width = 40 #실제 어깨 사이의 거리 cm
        correction_shoulder = 0.75 # 보정계수
        camera_to_shoulder_distance = real_shoulder_width * correction_shoulder / shoulder_distance  #카메라와 어깨 사이의 거리
        
        #눈 깜빡임 측정
        
        
        gap = camera_to_shoulder_distance - distance_between_cam_and_iris
        print(f"The gap is {gap:.1f}cm")
        
        
        
    cv2.imshow('result', frame)
    
    
    if cv2.waitKey(1) == ord('q'):
        break

#종료시 자원 해제, 창닫기
cap.release()
cv2.destroyAllWindows()