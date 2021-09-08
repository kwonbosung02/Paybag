import cv2

cam = cv2.VideoCapture(0)

if __name__ == "__main__":

    while(True):
        ret, frame = cam.read()

        cv2.imshow('main camera', frame)


        end_out_key = cv2.waitKey(1) & 0xFF
        if end_out_key == 27:
            break