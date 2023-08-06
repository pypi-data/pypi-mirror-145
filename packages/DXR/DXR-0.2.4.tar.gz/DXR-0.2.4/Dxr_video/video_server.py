# カメラ映像を接続されたクライアントに送信する

# ============================================================
# import packages
# ============================================================
import threading
from concurrent import futures
import grpc
from . import Datas_pb2
from . import Datas_pb2_grpc
import time
import cv2
import base64
import sys
from . import global_values as gv

# ============================================================
# property
# ============================================================
# カメラを設定


captureBuffer = None

# ============================================================
# class
# ============================================================
# サーバークラス
class Greeter(Datas_pb2_grpc.MainServerServicer):

    # ==========
    def __init__(self):
        pass

    # ==========
    def getStream(self, request_iterator, context):

        for req in request_iterator:

            # リクエストメッセージを表示
            print("request message = ", req.msg)

            while True:
                ret, buf = cv2.imencode('.jpg', captureBuffer)
                if ret != 1:
                    return

                # データを送信
                yield Datas_pb2.Reply(datas=buf.tobytes())

                # 60FPSに設定
                time.sleep(1 / 60)


# ============================================================
# functions
# ============================================================
def serve():
    cap = cv2.VideoCapture(gv.url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # サーバーを生成
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Datas_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)

    # ポートを設定
    server.add_insecure_port('[::]:50051')

    # 動作開始
    server.start()

    print('server start')

    while True:
        try:
            # カメラ映像から読み込み
            ret, frame = cap.read()
            if ret != 1:
                continue

            global captureBuffer
            captureBuffer = frame
            time.sleep(0)
            if not gv.server_isStart:
                break

        except KeyboardInterrupt:
            server.stop(0)


def set_url(url):
    gv.url = url


def start_server():
    gv.server_isStart = True
    threading.Thread(target=serve, daemon=True).start()


def stop_server():
    gv.server_isStart = False
