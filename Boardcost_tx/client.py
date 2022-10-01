import socket

from Gen_tx.gen_jiaoyi import gen_tx

'''
测试
使用socket库发送消息到特定的IP的特定端口
用户端
发送不验证,直接发送交易的16进制
发送新的区块
'''

ip_list = ['169.254.240.224','192.168.1.103','192.168.255.128','127.0.0.1']  # 固定ip的活跃主机
# ip_list = ['127.0.0.1']
TX_block = []
# 创建基于tcp和ipv4协议的socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sk = '371936354be730706ba4054b9e9e65d4537c6f0f14e01e91eaf2b131cc57d45e'
output = {
    "num": 1,
    "pk": [
        "0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857"],
    "money": [10]
}
inputs = "11111111218055b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08648096ee54d8d4e1ee7ef31c990ba5bd8536a59fb91b27110f4ad09db99c33a7fcaa1faca2457beeb4f73d276e4901c431e06262ff221c197a555635eabd1ad7398a8355b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b0810028076e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcfc880d125f5153fd097b31eaf55e9de6266d18630b63fe730b4381f40841a2024f1f4aaa45a2ed8a0eb2359d52b05c386925f7ee4d4d78672583bc4d238db2a2f29548376e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf20040F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A1180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a"

if __name__ == "__main__":
    TX_block.append(gen_tx(sk, inputs, output))
    # 新的交易 在本地先进行验证，不计算数据的有效性
    print("新的交易:", TX_block)
    for ip in ip_list:
        # 与服务端建立连接
        try:
            s.connect((ip, 8000))
            print('接收到的服务端数据：%s' % s.recv(1024).decode('utf-8'))
            # 分别发送三个数据
            for data in TX_block:
                print(data)
                data=bytes(data,encoding="utf-8")
                print(data)
                s.send(data)
                print('服务端又返回来的数据：%s ' % s.recv(1024).decode('utf-8'))
            s.send(b'exit')
            # 关闭socket
            s.close()
        except Exception  as e:
            print(e)
            print("ip:", ip, "disconnent!")
