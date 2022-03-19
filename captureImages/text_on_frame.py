import cv2
import os

font = cv2.FONT_HERSHEY_SIMPLEX 
displayedText = "Position the bottle in the box and take pictures covering entire label."
cam = cv2.VideoCapture(0)

width = cam.get(cv2.CAP_PROP_FRAME_WIDTH )
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT )
i = 0

while True:
    ret, frame = cam.read()
    cv2.putText(frame, displayedText, (round(width*0.08),round(height*0.1)), font, 0.5, (255,255,255), 1, cv2.LINE_AA) 
    cv2.rectangle(frame, (round(width*0.3),round(height*0.2)), (round(width*0.7),round(height*0.9)), (255,255,255), 2)
    cv2.imshow('test', frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        break
    elif k%256 == 32:
        i+=1
        ret1, frame1 = cam.read()
        imageName = "testImage" + str(i) + ".png"
        cv2.imwrite(imageName,frame1)
cam.release()
cv2.destroyAllWindows()