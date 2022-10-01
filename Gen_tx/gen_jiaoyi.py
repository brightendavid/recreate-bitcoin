"""
无敌的宋佳维大人
2021/10/7

依据以上数据，实现交易生成算法。
交易支持多个输入和多个输出。输入包含来源和解锁脚本，输出包含金额和锁定脚本。
所使用的数字签名算法是SM2，所使用的哈希函数是SM3。
"""

# 最初的交易ID  hash值 :F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A

from gmssl import sm2, func
# from pysmx.SM2 import generate_keypair
# len_para = 64
# pk, sk = generate_keypair(len_para)
# import sm3_self
from Gen_tx import sm3_self
from pysmx.SM2 import *
from base64 import *

len_para = 64


class tx:
    def __init__(self):
        self.version = "11111111"  # 8位

        self.input_num = 2  # 1位

        # message和pk
        # 来源
        self.pk = [
            "55b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08",
            "76e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf"]
        self.menory = [100, 200]
        self.sig = [
            "96ee54d8d4e1ee7ef31c990ba5bd8536a59fb91b27110f4ad09db99c33a7fcaa1faca2457beeb4f73d276e4901c431e06262ff221c197a555635eabd1ad7398a",
            "d125f5153fd097b31eaf55e9de6266d18630b63fe730b4381f40841a2024f1f4aaa45a2ed8a0eb2359d52b05c386925f7ee4d4d78672583bc4d238db2a2f2954"]
        self.message = [
            "55b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08100",
            "76e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf200"]
        self.last_tx_hash = "F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A"  # 上一个交易hash     前面加上长度

        self.output_num = 1
        # 去向
        self.out_put_pk = [
            "f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac1"]  # 收款方的pk
        self.out_menory = [90]  # 金额
        self.str_all = []

    def gen_money_last(self):
        sum1 = 0
        sum2 = 0
        for money in self.out_menory:
            sum1 += money
        for money in self.menory:
            sum2 += money
        return sum2 - sum1

    def clear_all(self):
        self.input_num = 0  # 1位
        self.pk = []
        self.menory = []
        self.sig = []
        self.message = []
        self.last_tx_hash = ""  # 上一个交易hash     前面加上长度
        self.output_num = 0
        # 去向
        self.out_put_pk = []  # 收款方的pk
        self.out_menory = []  # 金额
        # self.str_all = []

    def add_all(self):
        # 将可读的数据结构  变为16进制字符串
        self.str_all = []
        self.str_all.append(self.version)

        self.str_all.append(self.D2H2S(self.input_num))
        self.message = []

        for i in range(self.input_num):
            # 处理输入部分
            # 写入公钥，签名，消息
            input_id = i + 1
            self.str_all.append(self.D2H2S(input_id))
            self.str_all.append(self.D2H2S(len(self.pk[i])))  # 长度
            self.str_all.append(self.pk[i])  # 公钥
            self.str_all.append(self.D2H2S(self.menory[i]))
            # # print("mon",self.D2H2S(self.menory[i]))  # 钱全部2位数字

            # new added
            self.str_all.append(self.D2H2S(len(self.sig[i])))
            # # print(self.sig[i])
            self.str_all.append((self.sig[i]))  # 对应的签名

            # 对应的消息  就是pk+meney
            # 自己的pk和收到的money
            self.message.append(append_list(str(self.pk[i]), str(self.menory[i])))
            self.str_all.append(self.D2H2S(len(self.message[i])))
            self.str_all.append(self.message[i])  # 对应的消息
        # 上一个输入的hash的长度
        self.str_all.append(self.D2H2S(len(self.last_tx_hash)))
        # 上一个输入的hash
        self.str_all.append(self.last_tx_hash)

        self.str_all.append(self.D2H2S(self.output_num))
        for i in range(self.output_num):
            # 处理输入部分
            output_id = i + 1
            self.str_all.append(self.D2H2S(output_id))
            self.str_all.append(self.D2H2S(len(self.out_put_pk[i])))  # 长度
            self.str_all.append(self.out_put_pk[i])  # 公钥
            self.str_all.append(self.D2H2S(self.out_menory[i]))
        # 输出部分结束
        # # print(self.str_all)
        self.last_str = "".join(self.str_all)

    def explain(self, last_TX=""):
        """
        解释编码后的交易
        :return:  无return   返回到类的  属性中   有# print_all2 查看
        """
        self.clear_all()
        # self.pk.clear()
        # self.menory.clear()
        if last_TX != "":
            self.last_str = last_TX
        self.version = self.last_str[:8]
        self.last_str = self.last_str[8:]
        self.input_num = self.S2D(self.last_str[0])
        self.last_str = self.last_str[1:]
        for i in range(self.input_num):
            id = self.last_str[0]
            self.last_str = self.last_str[1:]
            len = self.S2D(self.last_str[:2])
            self.last_str = self.last_str[2:]
            self.pk.append(self.last_str[:len])
            self.last_str = self.last_str[len:]
            self.menory.append(int(self.last_str[:2], 16))
            self.last_str = self.last_str[2:]

            # 加入sig 和message
            # sig
            len = self.S2D(self.last_str[:2])
            self.last_str = self.last_str[2:]
            self.sig.append(self.last_str[:len])
            self.last_str = self.last_str[len:]

            # message
            # print("str  mess", self.last_str)
            len = self.S2D(self.last_str[:2])
            self.last_str = self.last_str[2:]
            self.message.append(self.last_str[:len])
            self.last_str = self.last_str[len:]

        len = self.S2D(self.last_str[:2])
        self.last_str = self.last_str[2:]
        self.last_tx_hash = self.last_str[:len]
        self.last_str = self.last_str[len:]

        # 输出部分
        self.output_num = self.S2D(self.last_str[0])
        self.last_str = self.last_str[1:]
        for i in range(self.output_num):
            """
            self.str_all.append(self.D2H2S(output_id))
            self.str_all.append(self.D2H2S(len(self.out_put_pk[i])))  # 长度
            self.str_all.append(self.out_put_pk[i])  # 公钥
            self.str_all.append(self.D2H2S(self.out_menory[i]))
            """
            id = self.last_str[0]
            self.last_str = self.last_str[1:]
            len = self.S2D(self.last_str[:2])
            self.last_str = self.last_str[2:]
            self.out_put_pk.append(self.last_str[:len])
            self.last_str = self.last_str[len:]
            self.out_menory.append(int(self.last_str[:2], 16))
            self.last_str = self.last_str[2:]

    def print_all(self):
        """
        :return: 最终输出的交易（编码后）
        """
        print("all:", self.last_str)

    def D2H2S(self, num):
        return str(hex(num))[2:]

    def S2D(self, str):
        """
        16进制字符串转10进制数字
        :param str:  字符串
        :return:  数字
        """
        import math
        hex = [ord(n) - 55 if n in list("ABCDEF") else ord(n) - 48 for n in str.upper()]
        dec = [hex[-i - 1] * math.pow(16, i) for i in range(len(hex))]
        return int(sum(dec))

    def print_all2(self):
        """
        :return: 输出这个类的全部字段
        """
        # self.explain()
        print("输出全部的字段")
        print("# print(self.version)", self.version)
        print("# print(self.pk)", self.pk)
        print("# print(self.input_num)", self.input_num)
        print("# print(self.last_tx_hash)", self.last_tx_hash)
        print("# print(self.menory)", self.menory)
        print("sig", self.sig)
        print("message", self.message)
        print("# print(self.output_num)", self.output_num)
        print("# print(self.out_put_pk)", self.out_put_pk)
        print("out money", self.out_menory)


def vrf(sig, message, pk):  # 私钥，消息，公钥   检验是否满足使用这笔交易的要求
    # 先签名，再拿出公钥取解密  若和MESSAGE相同  则通过，证明可以使用这个输出作为新的输入 ；PK和sig对应的sk是对应的
    # print("sig",(sig).hex())
    # print("message",message)
    t = Verify(sig, message, pk, len_para)
    # # print("ttttt",t)
    return t


def get_bit(ss):
    return bytes.fromhex(ss)


def gen_tx(sk, input, output):
    txx = tx()
    if input != "0000000000000000000000000000000000000000000000000000000000000000":
        txx.last_str = input
        txx.explain()  # 解析上一个交易的全部字符，到可以读取的形式
        txx.last_tx_hash = sm3_self.sm3_hash(bytes(input, encoding='utf-8'))  # 上一个交易的sm3 hash值
        # print(txx.last_tx_hash)
        all_money = 0

        sig_list = []
        message_list = []
        pk_list = []
        money_youxiao = []

        for i in range(len(txx.out_put_pk)):
            sk_bit = get_bit(sk)
            # message 和上一个交易有关，表示有权使用UTXO 输出，是上一个交易的的out_pk 和out_money
            # 等价于新的交易的pk和money
            message = append_list(str(txx.out_put_pk[i]), str(txx.out_menory[i]))
            sig = Sign(message, sk_bit, '123678', len_para)
            pk = get_bit(txx.out_put_pk[i])

            # print("使用的vrf:")
            # print("sig:", sig.hex())
            # print("message:", message)
            # print("pk:", pk.hex())

            if vrf(sig, message, pk):
                # 验签，若符合条件，则总金额+对应的金额
                all_money += txx.out_menory[i]
                sig_list.append(str(sig.hex()))
                message_list.append(message)
                pk_list.append(str(pk.hex()))
                money_youxiao.append(txx.out_menory[i])
        txx.pk = pk_list
        txx.message = message_list
        txx.sig = sig_list
        txx.menory.clear()
        txx.menory = money_youxiao

    # 输出部分  按照输入进行填写
    if input == "0000000000000000000000000000000000000000000000000000000000000000":
        txx.version = "00000000"
    txx.output_num = output["num"]
    txx.out_put_pk = output["pk"]
    txx.out_menory = output["money"]
    print("最后的money:", txx.out_menory)
    txx.input_num = txx.output_num
    txx.add_all()
    # print("strall:",txx.str_all)
    # txx.print_all2()
    return txx.last_str


def append_list(str1, str2):
    # str(txx.out_put_pk)+str(txx.out_menory)
    return str1 + str2


def child_sk(sk, index):
    """
    :param sk:  父节点代表的私钥
    :param index:  父节点 下子节点的索引序号  1，2，3
    :return:  子节点的私钥   sk_child =sk +H(sk+index)
    """
    sk_child = sk + str(index)
    sk_child = sk + sm3_self.sm3_hash(bytes(sk_child, encoding='utf-8'))
    return sk_child


if __name__ == "__main__":
    # TX = tx()
    #
    # TX.add_all()
    # print(TX.last_str)
    # 1号交易 有固定的填写数值生成
    # 11111111218055b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08648096ee54d8d4e1ee7ef31c990ba5bd8536a59fb91b27110f4ad09db99c33a7fcaa1faca2457beeb4f73d276e4901c431e06262ff221c197a555635eabd1ad7398a8355b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b0810028076e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcfc880d125f5153fd097b31eaf55e9de6266d18630b63fe730b4381f40841a2024f1f4aaa45a2ed8a0eb2359d52b05c386925f7ee4d4d78672583bc4d238db2a2f29548376e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf20040F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A1180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a
    # TX.clear_all()
    # TX.explain()
    # TX.print_all2()
    # TX.# print_all2()
    # pk, sk = generate_keypair(len_para)

    sk = '371936354be730706ba4054b9e9e65d4537c6f0f14e01e91eaf2b131cc57d45e'
    output = {
        "num": 1,
        "pk": [
            "0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857"],
        "money": [10]
    }
    inputs = "11111111218055b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08648096ee54d8d4e1ee7ef31c990ba5bd8536a59fb91b27110f4ad09db99c33a7fcaa1faca2457beeb4f73d276e4901c431e06262ff221c197a555635eabd1ad7398a8355b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b0810028076e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcfc880d125f5153fd097b31eaf55e9de6266d18630b63fe730b4381f40841a2024f1f4aaa45a2ed8a0eb2359d52b05c386925f7ee4d4d78672583bc4d238db2a2f29548376e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf20040F4A38489E32B45B6F876E3AC2168CA392362DC8F23459C1D1146FC3DBFB7BC9A1180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a"
    print("新的交易:", gen_tx(sk, inputs, output))
    # 新的交易  (sk, inputs, output) 生成
    # 111111111180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac164809b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b83f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac1100401fc7aae65e1a2a6f4ebe7170e1843beb2488867444b1bd59d4cf9d2cf098be2b117f0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857a

    print("\n解析新的交易\n")
    tx = tx()
    tx.clear_all()
    tx.print_all2()

    tx.explain(
        "111111111180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a809b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b82f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac190401fc7aae65e1a2a6f4ebe7170e1843beb2488867444b1bd59d4cf9d2cf098be2b117f0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857a")
    tx.print_all2()
