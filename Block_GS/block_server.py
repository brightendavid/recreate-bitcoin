# 服务器
import os
import socket

from Boardcost_tx.deal_blocks import Bit_Blocks


def server_save():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 3008))
    server.listen(3)
    while True:
        print("start......")
        sock, adddr = server.accept()
        total_data = b''
        data = sock.recv(1024)
        total_data += data
        num = len(data)
        # 如果没有数据了，读出来的data长度为0，len(data)==0
        while len(data) > 0:
            data = sock.recv(1024)
            num += len(data)
            total_data += data

        B = Bit_Blocks()
        block_num = B.gen_last_num() + 1
        block_name = "tx_block" + str(block_num) + ".txt"
        block_dir = r"../blocks"
        block_dir = os.path.join(block_dir, block_name)

        with open(block_dir, "wb") as f:
            # 保存文件
            f.write(total_data)
        sock.close()


if __name__ == '__main__':
    server_save()
