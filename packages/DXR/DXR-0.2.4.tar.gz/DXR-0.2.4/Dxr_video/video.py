from concurrent import futures
import re
import threading
import time
import cv2
import grpc
import base64
import numpy as np
from . import Datas_pb2
from . import Datas_pb2_grpc
import sys
import cv2
from . import global_values as gv


def setIP(ip):
    gv.ip = ip


def start_run():
    gv.isStart = True
    threading.Thread(target=run, daemon=True).start()


def run():
    # サーバーの宛先
    channel = grpc.insecure_channel(gv.ip + ':50051')
    stub = Datas_pb2_grpc.MainServerStub(channel)

    try:

        # リクエストデータを作成
        message = [Datas_pb2.Request(msg='give me the stream!!')]
        responses = stub.getStream(iter(message))

        for res in responses:
            # print(res.datas)

            # 画像を文字列などで扱いたい場合
            # b64d = base64.b64decode(res.datas)

            # バッファを作成
            dBuf = np.frombuffer(res.datas, dtype=np.uint8)

            # 作成したバッファにデータを入れる
            dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
            gv.video_que.queue.clear()
            gv.video_que.put(dst)
            if not gv.isStart:
                break

    except grpc.RpcError as e:
        gv.isStart = False
        print(e.details())


def get_frame():
    return gv.video_que.get()

def get_status():
    return gv.isStart