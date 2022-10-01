import socket

from Gen_tx.gen_jiaoyi import gen_tx

'''
测试
使用socket库发送消息到特定的IP的特定端口
用户端
发送不验证,直接发送交易的16进制
发送新的区块
'''

ip_list = ['169.254.240.224', '192.168.1.103', '192.168.255.128', '127.0.0.1']  # 固定ip的活跃主机
# ip_list = ['127.0.0.1']
TX_block = []
# 创建基于tcp和ipv4协议的socket



def client_send(file_dir):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for ip in ip_list:
        # 与服务端建立连接
        try:
            data = open(file_dir, "rb")
            s.connect((ip, 8001))
            print('接收到的服务端数据：%s' % s.recv(1024).decode('utf-8'))
            # 分别发送三个数据
            s.sendall(data.read())
            print('服务端又返回来的数据：%s ' % s.recv(1024).decode('utf-8'))
            s.send(b'exit')
            # 关闭socket
            s.close()
        except Exception  as e:
            print(e)
            print("ip:", ip, "disconnent!")


if __name__ == "__main__":
    client_send(r"../blocks/tx_block0.txt")
