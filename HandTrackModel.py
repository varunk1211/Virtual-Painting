import cv2
import time
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False,maxHands=2,detectionCon=0.5,trackCon =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipids = [4, 8, 12, 16, 20]

    def FindHands(self,frame,draw=True):

            imgrgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgrgb)

            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(frame, hand,self.mpHands.HAND_CONNECTIONS)
            return frame

    def FindPosition(self,frame,draw=True,handNo=0):

        self.lists=[]
        if self.results.multi_hand_landmarks:
            myhand= self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lists.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),5,(0,255,0),-1)
        return self.lists

    def tipfinding(self):
        find=[]
        # print(self.lists[self.tipids[0]][1])
        if self.lists[self.tipids[0]][1] < self.lists[self.tipids[0]-1][1]:
            find.append(1)
        else:
            find.append(0)
        for i in range(1,5):
            if self.lists[self.tipids[i]][2] < self.lists[self.tipids[i]-2][2]:
                find.append(1)
            else:
                find.append(0)

        return find


def main():

    ptime=0
    ctime=0
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    detector=HandDetector()

    while True:
        value, frame = cap.read()

        if not value:
            break

        frame = cv2.flip(frame, 1, 0)

        frame= detector.FindHands(frame)

        lmlist=detector.FindPosition(frame)
        if len(lmlist)!=0:
            print(lmlist[4])

            lists = detector.tipfinding()
            # print(lists)
        ####################################################
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = time.time()
        cv2.putText(frame, f"FPS: {fps:.2f}", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        #########################################################

        cv2.waitKey(1)
        cv2.imshow('Video', frame)


if __name__ == '__main__':
    main()