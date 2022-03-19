import cv2
import os 

focus = 0  # min: 0, max: 255, increment:5
cam = cv2.VideoCapture(0)
cam.set(28,focus)
folderPath = 'C:/EVA/captureImages/test2' #folder path to save captured images.
cv2.namedWindow("test")

img_counter = 10

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        #cv2.imwrite(img_name,frame)
        cv2.imwrite(os.path.join(folderPath,img_name), frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()