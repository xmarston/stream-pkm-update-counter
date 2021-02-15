import cv2
import time
import argparse
import pytesseract
import threading

parser = argparse.ArgumentParser()
parser.add_argument("-inputVideo", "-i", type=int, required=True)
parser.add_argument("-file", "-f", type=str, required=True)
parser.add_argument("-phrase", "-p", type=str, required=True)
args = parser.parse_args()

PKM_SENTENCE = args.phrase
DIFF_BETWEEN_LAST_APPEARANCE = 15
lastFound = time.time()

capture = cv2.VideoCapture(args.inputVideo)

def analyze_text(img):
    global lastFound
    text = pytesseract.image_to_string(img)
    if PKM_SENTENCE in text:
        now = time.time()
        diff = now - lastFound
        if diff >= DIFF_BETWEEN_LAST_APPEARANCE:
            lastFound = now
            updateCounter()
            time.sleep(1)

def updateCounter():
    try:
        with open(args.file, "r+") as f:
            num = int(f.read().strip())
            counter = num + 1
            print(counter)
            f.seek(0)
            f.write(str(counter))
            f.truncate()
    except IOError:
        print("File not accessible")


while True:
    __, frame = capture.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x = threading.Thread(target=analyze_text, args=(img,))
    x.start()

    key = cv2.waitKey(1000)
    if key == 27: #Key 'S'
            break

cv2.waitKey(0)
capture.release()
