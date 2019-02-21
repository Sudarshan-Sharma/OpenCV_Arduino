import imutils
import cv2
import serial  # Serial imported for Serial communication
import time  # Required to use delay functions

ArduinoSerial = serial.Serial('COM16', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(2)  # wait for 2 seconds for the communication to get established

print ArduinoSerial.readline()

# define the lower and upper boundaries of the colors in the HSV color space

yellowLower = (20, 200, 10)
yellowUpper = (40, 255, 255)

# if not args.get("video", False):
camera = cv2.VideoCapture(0)
# else:
#     camera = cv2.VideoCapture(args["video"])

while True:
    (grabbed, frame) = camera.read()

    frame = imutils.resize(frame, width=700)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Yellow', (int(x), int(y)), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            ArduinoSerial.write('1')  # send 1
            print ("LED turned ON")

    else:
        ArduinoSerial.write('0')  # send 1
        print ("LED turned OFF")

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()