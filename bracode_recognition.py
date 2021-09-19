# --------------Import module---------------
import cv2
import requests, json
from pyzbar.pyzbar import decode
from playsound import playsound
print('library loaded')

# ----------------linespace-----------------
def space():
    print('-' * 24)
space()

# ----------------Market id-----------------
Market_id_ = 'market-0001'
print("Market id is "+ Market_id_)
space()

# ----------------post url------------------
URL = "http://pwnable.co.kr:8000/market_rent/"

# --------------local camera----------------
try:
    cam = cv2.VideoCapture(0)
except:
    print('Error')

if __name__ == "__main__":
    # -------------load cascade-------------
    face_cascade = cv2.CascadeClassifier('./data/haarcascade.xml')

    # --------------resize cap--------------
    mask = cv2.imread('./cap.png')
    mask_h, mask_w, _ = mask.shape
    resize_h = int(0.3*mask_h)
    resize_w = int(0.3*mask_w)
    resize_mask = cv2.resize(mask,(resize_w,resize_h), interpolation=cv2.INTER_CUBIC)

    # -------------cap bitwise--------------
    mask = cv2.cvtColor(resize_mask, cv2.COLOR_BGR2GRAY)
    mask[mask[:] >= 200] = 0
    mask[mask[:] > 0] = 255
    mask_inv = cv2.bitwise_not(mask)
    cap = cv2.bitwise_and(resize_mask, resize_mask, mask=mask)

    # ----initial barcode and check var-----
    barcode1 = ''
    barcode2 = ''
    check = 0

    # --------------main loop---------------
    while(True):

        # -----------load cam---------------
        ret, frame = cam.read()

        # -----------convert----------------
        gray_scale = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # --------face Recognition----------
        faces = face_cascade.detectMultiScale(gray_scale, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
        # scaleFactor : balance, minNeighbors : face to face minimum pixel, minsize : minimum face size

        # -----------draw rect--------------
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            try:
                x_v = -100
                y_v = -160
                # ---------masking----------
                roi = frame[y+y_v:y+resize_h+y_v,x+x_v:x+resize_w+x_v]
                back = cv2.bitwise_and(roi, roi, mask=mask_inv)
                dst = cv2.add(cap, back)

                frame[y+y_v:y+resize_h+y_v,x+x_v:x+resize_w+x_v] = dst
            except:
                pass

        # -------barcode Recognition---------
        barcodes = decode(frame)

        if len(barcodes) != 0:
            # -------update barcode----------
            barcode = barcodes[0]

            playsound("./sound/in2.mp3")
            playsound("./sound/in2.mp3")
            check = check + 1

            # -----------check---------------
            if(check == 1):
                barcode1 = barcode
                print(barcode1.data.decode('utf-8'))
            if(check == 2):
                barcode2 = barcode
                print(barcode2.data.decode('utf-8'))
            barcodes = []
        # --before post, check if barcodes are valid--
        if(check == 2):
            if (barcode1.data.decode('utf-8')[0:3] == '010' and barcode2.data.decode('utf-8')[0:3] == '010'):
                space()
                print("Two barcodes are user barcode -ERROR-")
                barcode1 = None
                barcode2 = None
                check = 0

            elif (barcode1.data.decode('utf-8')[0:3] != '010' and barcode2.data.decode('utf-8')[0:3] != '010'):
                space()
                print("Two barcodes are ecobag barcode -ERROR-")
                barcode1 = None
                barcode2 = None
                check = 0

        # --------------post-----------------
        if(check == 2):
            print("two barcodes are collected")
            # -------value initialize--------
            user_ = ''
            ecobag_ = ''

            # -------------check-------------
            if barcode1.data.decode('utf-8')[0:3] == '010':
                user_ = barcode1
                ecobag_ = barcode2
            else:
                user_ = barcode2
                ecobag_ = barcode1
            space()

            # ---------update data-----------
            print("USER : " + user_.data.decode('utf-8')[:-2])
            print("ECOBAG : " + ecobag_.data.decode('utf-8'))
            print("MARKET : " + Market_id_)
            data = {"Mid"  : str(Market_id_),
                    "phone": str(user_.data.decode('utf-8')[:-2]),
                    "Eid"  : str(ecobag_.data.decode('utf-8'))
                    }

            # -----------req post------------
            try:
                res = requests.post(URL,data=json.dumps(data))
                space()
                print(res)
            except:
                space()
                print('POST ERROR')
            check = 0
            barcodes = []
        # ------------show video-------------
        cv2.imshow('main camera', frame)

        # ----------destroy key--------------
        end_out_key = cv2.waitKey(10) & 0xFF
        if end_out_key == 27:
            break
