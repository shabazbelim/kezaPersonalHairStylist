import cv2
from hairstylist.pipeline.faceWarp import find_landmarks, face_warp
def face_wrapping(source_image, target_image, predictor):
    img2 = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    img1 = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    facial_mask = img2
    frame_in = img1
    facial_mask_lm = find_landmarks(facial_mask, predictor)
    frame_out = face_warp(facial_mask, facial_mask_lm, frame_in)
    blur = cv2.GaussianBlur(frame_out,(5,5),0)

    return blur