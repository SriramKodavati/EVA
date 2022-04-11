# Here we integrated both the capture of images and text recognition programs.
import cv2
import os
import numpy as np
import pytesseract
#from pytesseract import Output
#from matplotlib import pyplot as plt

beginOCR = False  # Decides when to start OCR.
folderPath = 'C:/Users/Alex Davison/PycharmProjects/EVAProject'  # folder path to create a folder and save captured images.
folderName = 'capturedImages'
# cv2.namedWindow("test")

img_counter = 0  # count of no of images captured.
pillBottleCount = 0  # Keeps track of no of pill bottles captured.

# Code below is to capture images.
font = cv2.FONT_HERSHEY_SIMPLEX
displayedText = "Position the bottle in the box and take pictures covering entire label."
IMG_DIR = os.path.join(folderPath, folderName)
cam = cv2.VideoCapture(0)  # opens the camera.

width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame = cam.read()
    cv2.putText(frame, displayedText, (round(width * 0.08), round(height * 0.1)), font, 0.5, (255, 255, 255), 1,
                cv2.LINE_AA)
    cv2.rectangle(frame, (round(width * 0.3), round(height * 0.2)), (round(width * 0.7), round(height * 0.9)),
                  (255, 255, 255), 2)
    cv2.imshow('test', frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        break
    elif k % 256 == 32:
        img_counter += 1
        imageName = "Image" + str(img_counter) + ".png"
        try:
            if not os.path.isdir(IMG_DIR):
                os.mkdir(IMG_DIR)
            ret1, frame1 = cam.read()
            cv2.imwrite(os.path.join(IMG_DIR, imageName), frame1)
            print("{} written".format(imageName))
        except OSError as error:
            print("Error creating or saving a image to the folder\n", error)
cam.release()
cv2.destroyAllWindows()

beginOCR = True  # Starting character recognition for each image.

print("Starting Tesseract OCR..!")
# Beginning text extraction using Tesseract OCR.
if beginOCR:
    # get grayscale image
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # noise removal
    def remove_noise(image):
        return cv2.medianBlur(image, 5)


    # thresholding
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    # dilation
    def dilate(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)


    # erosion
    def erode(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)


    # opening - erosion followed by dilation
    def opening(image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


    # canny edge detection
    def canny(image):
        return cv2.Canny(image, 100, 200)


    # skew correction
    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


    # template matching
    def match_template(image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


    print('\n-----------------------------------------')
    print('TESSERACT OUTPUT --> Original Image')
    print('-----------------------------------------')

    for image_name in os.listdir(IMG_DIR):
        image = cv2.imread(os.path.join(IMG_DIR, image_name))
        # width = int(image.shape[1])
        # height = int(image.shape[0])
        # d = pytesseract.image_to_data(image, output_type=Output.DICT)

        # preprocess image
        '''
        gray = get_grayscale(image)
        thresh = thresholding(gray)
        opening = opening(gray)
        canny = canny(gray)
        images = {'gray': gray, 
                'thresh': thresh, 
                'opening': opening, 
                'canny': canny}
        '''

        # Get OCR output using Pytesseract
        custom_config = r'-c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-:" " --oem 3'

        print("{} output".format(image_name))

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        print(pytesseract.image_to_string(image, config=custom_config))