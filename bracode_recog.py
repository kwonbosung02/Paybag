import cv2
print("cv2 loaded")
from pyzbar.pyzbar import decode
print("pyzbar loaded")



cam = cv2.VideoCapture(0)

if __name__ == "__main__":

    while(True):
        ret, frame = cam.read()

        barcodes = decode(frame)

        if len(barcodes) != 0:
            barcode = barcodes[0]

        cv2.imshow('main camera', frame)


        end_out_key = cv2.waitKey(1) & 0xFF
        if end_out_key == 27:
            break
