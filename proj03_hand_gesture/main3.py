from flask import Flask, Response, jsonify, render_template, request
import cv2
import mediapipe as mp
import math
import serial
import time

app = Flask(__name__)

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# status = 'STOP'
# portNum = "COM4"
# ser = serial.Serial(portNum, 9600, timeout=1)
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2)) + math.sqrt(math.pow(y1 - y2, 2))


#   return (x1 - x2)2 + (y1 - y2) ** 2
compareIndex = [[1, 4], [6, 8], [10, 12], [14, 16], [18, 20]]
open = [False, False, False, False, False]
gesture = [
    [True, False, False, False, False, "STOP"],  # 주먹
    [True, True, False, False, False, "RIGHT"],  # 검지 하나
    [True, True, True, False, False, "LEFT"],  # 브이
    [True, True, True, True, True, "START"],  # 손가락 다피면
]


# def close_serial():
#     ser.close()
# def send_soc(message):
#     # time.sleep(1)
#     message = str(message)+'\n'
#     ser.write(message.encode('utf-8'))
#     # print()
#     # print("temp: ", temp)
#     #     result = ws.recv()
#     #     print("msg from 서버: " + result)
# def msg_get():
#     if ser.in_waiting > 1:
#         # time.sleep()
#         dataIn = ser.readline().decode().strip()
#         print("받은 말: ", dataIn)
# while True:
def web_captest(ref, frame):
    #    ref, frame = cap.read()
    h, w, c = frame.shape
    temp_txt = ""
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for i in range(0, 5):
                open[i] = dist(
                    handLms.landmark[0].x,
                    handLms.landmark[0].y,
                    handLms.landmark[compareIndex[i][0]].x,
                    handLms.landmark[compareIndex[i][0]].y,
                ) < dist(
                    handLms.landmark[0].x,
                    handLms.landmark[0].y,
                    handLms.landmark[compareIndex[i][1]].x,
                    handLms.landmark[compareIndex[i][1]].y,
                )
                print(
                    type(
                        dist(
                            handLms.landmark[0].x,
                            handLms.landmark[0].y,
                            handLms.landmark[compareIndex[i][0]].x,
                            handLms.landmark[compareIndex[i][0]].y,
                        )
                    )
                )
                print(
                    dist(
                        handLms.landmark[0].x,
                        handLms.landmark[0].y,
                        handLms.landmark[compareIndex[i][0]].x,
                        handLms.landmark[compareIndex[i][0]].y,
                    )
                )
            print(open)
            text_x = handLms.landmark[0].x * w
            text_y = handLms.landmark[0].y * h
            for i in range(0, len(gesture)):
                flag = True
                if open[1] == False:
                    temp_txt = "STOP"
                elif open[2] == False:
                    temp_txt = "RIGHT"
                elif open[3] == False:
                    temp_txt = "LEFT"
                elif open[4] == True:
                    temp_txt = "START"
                for j in range(0, 5):
                    if gesture[i][j] != open[j]:
                        flag = False
                    if flag == True:
                        # temp_txt = gesture[i][5]
                        #    send_soc(temp_txt)
                        status = temp_txt
                        cv2.putText(
                            frame,
                            temp_txt,
                            (round(text_x) - 50, round(text_y) - 250),
                            cv2.FONT_HERSHEY_PLAIN,
                            4,
                            (0, 0, 0),
                            4,
                        )
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
    if temp_txt != "":
        print(temp_txt)
        print(status)
    #     msg_get()
    #  cv2.imshow("HandTracking", frame)
    cv2.waitKey(1)


# def get_status():
#     print("get : ", status)
#     return status


def generate_frames():
    while True:
        #  success, frame = cap.read()  # 프레임 읽기
        ref, frame = cap.read()
        web_captest(ref, frame)
        if not ref:
            break
        else:
            # 프레임을 JPEG 형식으로 인코딩
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            # 클라이언트에 전송하기 위해 프레임을 yield
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/update", methods=["GET"])
def data_update():
    # motionset = get_status()
    if request.method == "GET":
        motionset = request.args.get("name", "rrrr")
        print(request.form)

    # motionset = status
    print("현재 상태 : ", motionset)
    return render_template(jsonify({"status": "rrrr"}), data="rrrr")


app.run()

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
