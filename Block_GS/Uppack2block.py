import os
import socket
import time

from Block_GS.anylize_tx import anylize
from Block_GS.block_client import client_send
from Boardcost_tx.deal_blocks import Bit_Blocks, TXT_operation
from Gen_tx.gen_jiaoyi import gen_tx, tx
from Gen_tx.sm3_self import sm3_hash


def text_create(name, msg=""):
    desktop_path = "../blocks"  # 新创建的txt文件的存放路径
    full_path = os.path.join(desktop_path, name)  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    if msg != "":
        file.write(msg)
    file.close()


import hashlib
def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash

class Uppack_Txs:
    """
    交易打包，分块
    把打包包含的交易总输出-总输入   的差价给自己（记账人）
    """

    def __init__(self, pack_num=0):
        """
        init  记账的交易数量，默认不记账，直接收取区块奖励
        :param pack_num:
        """
        self.last_unpask_tx_index = 0
        self.pack_num = pack_num

        self.previoushash = ""
        self.time = 0
        self.nonce = 58445
        self.difficulty = 8
        self.transactionhash = 'ce0e68fc0865473ab791c67f00f010530ba38253cd9043808eac973bd585f00b'
        self.transaction = [
            "111111111180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a809b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b82f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac190401fc7aae65e1a2a6f4ebe7170e1843beb2488867444b1bd59d4cf9d2cf098be2b117f0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857a"]
        self.add_to_transaction_transaction_hash()
        self.gen_last_block()
        self.need_str = self.add_all_message()

    def add_to_transaction_transaction_hash(self):
        XX = TXT_operation(r"../TXs/unpacklist.txt")  # 这个unpacklist.txt 有人工手动加入
        self.transaction = XX.read_UTXO()  # self.transaction是读取的unpacklist.txt 中的全部交易
        TT=Bit_Blocks()
        last_block=TT.gen_newest()
        hashfile=os.path.join(r"../blocks",last_block)
        if not os.path.exists(hashfile):
            hashfile = os.path.join(os.path.dirname(__file__), hashfile)
        if not os.path.exists(hashfile):
            print("cannot found file")
        else:
            self.transactionhash=CalcMD5(hashfile)  # 求出self.transactionhash

    def add_all_message(self):
        """
        除了需要求的nonce 没有，其他的全部在return 中
        :return:
        """
        sstr = self.previoushash + str(self.difficulty) + self.transactionhash
        return sstr

    def gen_last_block(self):
        """
        挖矿部分
        准备挖矿,获取必要信息
        :return:
        """
        B = Bit_Blocks()
        Messages = B.gen_items()
        # print(Messages)
        """
        {'previoushash': '5156165165', 'time': 454545, 'nonce': 58445, 'difficulty': 8, 'transactionhash': 'ce0e68fc0865473ab791c67f00f010530ba38253cd9043808eac973bd585f00b'}
        """
        self.previoushash = Messages['previoushash']
        time1 = Messages['time']
        self.difficulty = Messages['difficulty']
        Messages2 = B.gen_items(B.gen_second())
        time2 = Messages2['time']

        time2_time2 = abs(time1 - time2)
        # 计算最近两个block的时间差 和10分钟做比较
        # 10分钟=600秒
        if time2_time2 < 600:
            # 若区块产生时间小于10分钟，加大难度
            self.difficulty += 1
        else:
            # 若区块产生时间大于10分钟，减小难度
            self.difficulty -= 1

    def prove_of_work(self):
        diff_hash = []
        for i in range(64):
            diff_hash.append("f")
        for i in range(self.difficulty):
            diff_hash[i] = "0"
        diff_hash = "".join(diff_hash)
        diff_hash = bytes.fromhex(diff_hash)
        nonce = 111111
        while nonce < 0x10000:
            if sm3_hash(bytes.fromhex(str(hex(nonce))[2:] + self.need_str)) < diff_hash:
                # 找到了
                return hex(nonce)
        # 没找到
        return -1

    def gen_list2block(self):
        ll = []
        ll.append(self.previoushash)
        ll.append(str(self.time))
        ll.append(str(self.nonce))
        ll.append(str(self.difficulty))
        ll.append(self.transactionhash)
        # ll.append(self.gen_last_block())
        if self.pack_num != 0:
            for i in range(self.pack_num):
                # 加入需要的交易
                # 由于记账人是自己，若将已经记账的交易发出去，则不会有其他人记账
                trans = anylize(self.transaction)  # 选择差价最大的交易
                self.transaction.remove(trans)  # 去除最大值
                self.transaction[i] = gen_tx_cost(trans)
                ll.append(trans)
                # 收取交易费用

        # 区块奖励
        # 还有一点问题，这个区块奖励在现在的代码中还用不了
        B = Bit_Blocks()
        num = (B.gen_last_num() + 1) // 65535
        if num > 1:
            money = 50 // pow(2, num)
        else:
            money = 50
        sk = '0000000000000000000000000000000000000000000000000000000000000000'
        output = {
            "num": 1,
            "pk": [
                my_pk],
            "money": [money]
        }
        inputs = "0000000000000000000000000000000000000000000000000000000000000000"
        ll.append(gen_tx(sk, inputs, output))
        return ll

    def pack(self):
        self.nonce = self.prove_of_work()
        self.time = int(time.time())
        B = Bit_Blocks()

        block_num = B.gen_last_num() + 1
        block_name = "tx_block" + str(block_num) + ".txt"
        print("block_name", block_name)
        block_dir = r"../blocks"
        block_dir = os.path.join(block_dir, block_name)
        if self.pack_num != 0:
            # 如果想要交易记账奖励
            text_create(block_name)
            T = TXT_operation()
            # add 参数是所有内容的一个list,不包含换行
            T.add(self.gen_list2block())
        else:
            # 此部分完成
            text_create(block_name)
            block_dir = r"../blocks"
            block_dir = os.path.join(block_dir, block_name)
            T = TXT_operation(block_dir)
            # add 参数是所有内容的一个list,不包含换行
            T.add(self.gen_list2block())
            # 不要交易记账奖励
            # 直接计算pow
        # 区块的上链
        client_send(block_dir)


def gen_tx_cost(txx):
    TX = tx()
    TX.explain(txx)  # 解析这个交易
    TX.print_all2()
    money_to_charge = TX.gen_money_last()
    TX.output_num += 1
    TX.out_put_pk.append(my_pk)
    TX.out_menory.append(money_to_charge)
    TX.add_all()
    return TX.last_str


if __name__ == "__main__":
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)  # 获取本机的ip
    my_ip = ipaddr
    my_pk = "9a29a6f9f8bcf90a54d821bf3be709d5034eb6f8767e8aa73df6e2153de444c95355046b452253ff114d6a2377921618d91238d359bce85c582e10a4bdf66f73"
    my_sk = "1f702fb190380312ba478a5f5541521c0400c1d3c89e072ac7104b02161d49ff"
    print(int(time.time()))
    T = Uppack_Txs()
    (T.gen_last_block())

    # print(gen_tx_cost("111111111180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a809b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b82f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac190401fc7aae65e1a2a6f4ebe7170e1843beb2488867444b1bd59d4cf9d2cf098be2b117f0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857a"))
    T.pack()
