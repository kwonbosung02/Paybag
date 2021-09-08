import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

"""


cam = cv2.VideoCapture(0)

if __name__ == "__main__":

    while(True):
        ret, frame = cam.read()

        barcodes = decode(frame)

        cv2.imshow('main camera', frame)


        end_out_key = cv2.waitKey(1) & 0xFF
        if end_out_key == 27:
            break
"""