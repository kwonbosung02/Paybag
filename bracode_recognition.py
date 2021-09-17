import cv2
import numpy as np
from pyzbar.pyzbar import decode
from playsound import playsound

print('library loaded')
print('-'*24)
Market_id_ = 'market-0001'
print("Market id is "+ Market_id_)
print('-'*24)

try:
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('./data/haarcascade.xml')
except:
    print('Error')

if __name__ == "__main__":
    mask = cv2.imread('./cap.png')
    mask_h, mask_w, _ = mask.shape
    resize_h = int(0.3*mask_h)
    resize_w = int(0.3*mask_w)
    resize_mask = cv2.resize(mask,(resize_w,resize_h), interpolation=cv2.INTER_CUBIC)

    mask = cv2.cvtColor(resize_mask, cv2.COLOR_BGR2GRAY)
    mask[mask[:] >= 200] = 0
    mask[mask[:] > 0] = 255
    mask_inv = cv2.bitwise_not(mask)
    cap = cv2.bitwise_and(resize_mask, resize_mask, mask=mask)
    barcode1 = ''
    barcode2 = ''
    check = 0
    while(True):

        ret, frame = cam.read()

        gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #face Recognition
        faces = face_cascade.detectMultiScale(gray_scale, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        #balance, ftf min pixel, min f size

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            try:
                x_v = -100
                y_v = -160
                roi = frame[y+y_v:y+resize_h+y_v,x+x_v:x+resize_w+x_v]

                back = cv2.bitwise_and(roi, roi, mask=mask_inv)

                dst = cv2.add(cap, back)

                frame[y+y_v:y+resize_h+y_v,x+x_v:x+resize_w+x_v] = dst
            except:
                pass
        #barcode Recognition
        barcodes = decode(frame)

        if len(barcodes) != 0:
            barcode = barcodes[0]

            playsound("./sound/in2.mp3")
            playsound("./sound/in2.mp3")
            check = check + 1
            if(check == 1):
                barcode1 = barcode
                print(barcode1.data.decode('utf-8'))
            if(check == 2):
                barcode2 = barcode
                print(barcode2.data.decode('utf-8'))
            barcodes = []

        if(check == 2):
            print("two barcodes are collected")
            user_ = ''
            ecobag_ = ''
            if barcode1.data.decode('utf-8')[0:3] == '010':
                user_ = barcode1
                ecobag_ = barcode2
            else:
                user_ = barcode2
                ecobag_ = barcode1
            print('-'*24)
            print("USER : " + user_.data.decode('utf-8'))
            print("ECOBAG : " + ecobag_.data.decode('utf-8'))
            print("MARKET : " + Market_id_)
            check = 0
            barcodes = []

        cv2.imshow('main camera', frame)


        end_out_key = cv2.waitKey(10) & 0xFF
        if end_out_key == 27:
            break
