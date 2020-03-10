import numpy as np
import cv2
import sys


# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

img_counter = 1

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite("my-image.png", gray[y:y+h, x:x+w])

    cv2.imshow("Video", frame)

    k = cv2.waitKey(1)

    if k % 256 == 27:
        # ESC pressed

        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "{}.png".format(img_counter)
        for (x, y, w, h) in faces:
            cv2.imwrite(img_name, frame[y:y + h, x:x + w])
        print("{} written!".format(img_name))
        img_counter += 1


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
