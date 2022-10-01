'''
宋佳维
2021/10/23
测试
使用socket库发送消息到特定的IP的特定端口
server端

接收所有缺失的区块，并进行判别
'''
# B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E246202075a/n/n
import _thread
import os
import time
import socket
import threading

from Boardcost_tx import time_manager
from Boardcost_tx.BloomFilter import BloomFilter
from Boardcost_tx.deal_blocks import Bit_Blocks, TXT_operation
from Gen_tx.gen_jiaoyi import tx, vrf, get_bit

# 由于socket 无法返回，设计   孤立交易池  为全局变量     可以接收多个块  每隔一段时间进行UTXO验证->更新区块->清空!!!!
# 对于每个机器都是独立的，不进行共享
menmpool = []




# 对于menmpool 中的每一个block进行验证,更新UTXO
def menmpool_upadta():
    print(menmpool)
    # time_manager.loop_func(menmpool_upadta,5)
    """
    调用  is_TX_true  判断每个block的正确性
    若正确，更新UTXO；
    若错误，则nop
    最后，清空menmpool
    :return:
    """
    # 不需要考虑  时间
    delete_UTXO = []
    add_UTXO = []
    tx_save_block_list=[]


    T=TXT_operation(r"../TXs/tx.txt")

    # 则新建文件夹为"tx_block"    +   number    +  ".txt"
    # number 由已有的block
    origin_blocks=T.read_UTXO()
    bloom = BloomFilter(10000, 20)
    for block in origin_blocks:
        bloom.add(block)

    for tx_block in menmpool:
        if tx_block in bloom:
            print("not pass",tx_block)
            # 如果已经在chain 中存储了，下一个区块
            continue
        else:
            # 如果不在chain中，放入bloom 中
            print("pass",tx_block)
            bloom.add(tx_block)

        if is_TX_true(tx_block):
            #  对于交易的所有输入部分，清除UTXO 中对应的数据；对于输出部分作为，UTXO 新的加入
            TX = tx()
            TX.explain(tx_block)
            for i in range(TX.input_num):
                delete_UTXO.append(TX.pk[i] + TX.D2H2S(TX.menory[i]))
            for i in range(TX.output_num):
                add_UTXO.append(TX.out_put_pk[i] + TX.D2H2S(TX.out_menory[i]))
            tx_save_block_list.append(tx_block)

    # 保存区块
    T.add(tx_save_block_list)


    # global menmpool
    menmpool.clear()

    U = TXT_operation()
    U.delete(delete_UTXO)
    U.add(add_UTXO)


def check_isin_UTXO(tx_out_list):
    ss = TXT_operation()
    UTXO_list = (ss.read_UTXO())
    bloom = BloomFilter(10000, 20)
    # First insertion of animals into the bloom filter
    for tx in UTXO_list:
        bloom.add(tx)  # 生成一个二进制序列
    for tx in tx_out_list:
        if tx in bloom:
            # 若在UTXO 中，则返回false,不需要复原
            return False
        else:
            bloom.add(tx)  # 若不在本机UTXO 中，则修改这个序列，加入此次的交易
    return True


# 单个block的交易验证正确性
def is_TX_true(tx_block):
    """
    # 单个block
    3步验证   按照计算量的大小进行排列
    :param tx_block:  交易的16进制字符
    :return: boolen数值
    """
    TX = tx()
    TX.explain(tx_block)  # explain 附带了清空原有交易结构，解析



    # 1 金额验证 金额验证放在密钥验证前面
    out_money_sum = 0
    in_money_sum = 0
    for imoney in TX.menory:
        in_money_sum += imoney
    for imoney in (TX.out_menory):
        if imoney < 0:
            return False
        out_money_sum += imoney
    if in_money_sum < out_money_sum:
        return False

    # 2 UTXO 验证
    # 1,获取输入部分（pk和金额）
    pk_money = []
    for i in range(TX.input_num):
        pk_money.append(TX.pk[i] + TX.D2H2S(TX.menory[i]))
        # 使用BloomFliter算法进行验证：输出是否在UXTO中   三个hash  映射到一组二进制向量，验证
    if not check_isin_UTXO(pk_money):
        # 若交易被 BloomFliter 判断为已经在UTXO中，则FALSE
        return False

    # 3 交易金额数据有效性验证
    for i in range(TX.input_num):
        # 16进制字符-》bit   bytes.fromhex((pk))
        print("sig",TX.sig[i])
        print("pk",TX.pk[i])
        print("message",TX.message[i])
        sig = get_bit(TX.sig[i])
        message = TX.message[i]
        pk = get_bit(TX.pk[i])  # (TX.pk[i]).hex()
        # 这里验证签名部分已经修正
        if not vrf(sig, message, pk):
            print("交易造假！！")
            return False
    print("交易有效")
    return True





# socket调用
def dealtcp(sock, addr):
    """
    接收传来的数据，并发送给对方数据
    """
    print('Accept new connection from %s:%s' % addr)
    # 发送数据
    sock.send(b'Hello, I am server')
    # 循环接收数据
    while True:
        # data.decode('utf-8')  获得的交易block
        # 每次接收1024字节
        data = sock.recv(1024)
        # 等待1s
        time.sleep(1)
        # 如果data为空或客户端发送过来exit循环中断
        if not data or data.decode('utf-8') == 'exit':
            break
        print('客户端发来的数据：%s' % data.decode('utf-8'))

        global menmpool
        menmpool.append(data.decode('utf-8'))

        # time_manager.loop_func(menmpool_upadta, 2)
        # print("menmpool:",menmpool)


        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))


    # 关闭socket
    sock.close()
    print('Connection from %s:%s closed.' % addr)
    # global menmpool
    # if len(menmpool)>5:
    # 不使用依据时间作为更新UTXO 的线索，使用menmpool中的交易的数量为线索
    # # 要等10分钟更新block和UTXO
    # menmpool_upadta()


def server_on():
    # 创建一个基于IPv4和TCP协议的Socket：
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本地ip和端口
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname) # 获取本机的ip
    print("本机的ip地址为:",ipaddr,"8000")
    s.bind((ipaddr, 8000))
    # 监听端口，传入的参数表示等待连接的最大连接数
    s.listen(10)
    print('Waiting for connection...')
    # 等待连接

    # 重要：每隔一段时间运行menmpool_upadta

    while True:
        # 无限循环
        # accept等待连接进入，返回新的socket和ip:端口

        sock, addr = s.accept()
        # 创建线程执行
        t = threading.Thread(target=dealtcp, args=(sock, addr))
        # 启动线程
        t.start()




if __name__ == '__main__':


    # time_manager.loop_func(menmpool_upadta, 2)
    t1 = threading.Thread(target=time_manager.loop_func, args=((menmpool_upadta, 20))) # 新的线程，每隔10分钟，更新一硬盘
    # 启动线程
    t1.start()



    server_on()