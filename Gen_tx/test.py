from pysmx.SM2 import *
from base64 import *

from Gen_tx.gen_jiaoyi import gen_tx
from Gen_tx.sm3_self import sm3_hash

len_para = 64
pk, sk = generate_keypair(len_para)

# bit流和hex 之间的转换
print("pk")
print((pk).hex())
print((sk).hex())
# print(bytes.fromhex((pk).hex()))
# 651561659ce0e68fc0865473ab791c67f00f010530ba38253cd9043808eac973bd585f00b
t=(bytes.fromhex("a6ca59aa671526457475070fa370d441d3e8f350c0904a7378ed084825872292d9755bfd135fd2d913c6eb91463e83ec31edf9d8a95fa83089b57e48867ad766"))
print("ttttt")
print(sm3_hash(t))
# sk = b"00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5"
# pk = b"B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207"

# sig = Sign("你好", sk, '123678', len_para)  # data   sk   随机数   len_para
# # sig = b64decode(b"PUlcyV4Hf+Yiabo5bCNg6i4puU1EHobBTRyH0e2oJlwqNqEgJBLb9Bv6qE3nvsv5NfFEVWOzenxnGzAf6Pxm6g==")
# print("sig:", b64encode(sig))
# print("data:", b64encode(bytes('你好', encoding='utf8')))
# print(Verify(sig, "你好", pk, len_para))
# a="1E"
# b=int(a,16)
# print(b)
# print(bytes.fromhex(a))


# pk = ["55b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08",
#       "76e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf"]
# menory = [100, 200]
# sig=["04f2a1f4a1da88753ef6831b9aaaf6a094a3663f7034020d1cfe8783d5fd17d3c793921f1045c4dcf495386b903ae7b863d333167e310f571a4ddbbb3491e0b0",
#                   "04f2a1f4a1da88753ef6831b9aaaf6a094a3663f7034020d1cfe8783d5fd17d3c793921f1045c4dcf495386b903ae7b863d333167e310f571a4ddbbb3491e0b0"]
# message=["55b7cc6f98537860d3dcde7e90f133419ab6f0352c26f959354a5ded28ea419ecba2d1a9865460e1c2ed6103373e88deb8308e2c2511be7b6432d490d5112b08100",
#                       "76e1b32f204349b72d84379820f43d555475980fb94131032d9f472bdb834e0bc95accef52b52cdb8621b4339d81de4e3ee7f16956f1f214a0bf841ff7540bcf200"]
# sk=['d389fdd5c144014a0c5bc30e5093cfe00dfdf0be5286306ad59890312820d6fb',
#     '3afd670cbdf40670b94defebf799cc47c2013a56a11bcc7f03e70c1d460faf45']
sig =['9b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b']
message= ['f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac190']
pk=['f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac1']
sk=["371936354be730706ba4054b9e9e65d4537c6f0f14e01e91eaf2b131cc57d45e"]

sig_now =bytes.fromhex((sig[0]))
pk_now= bytes.fromhex((pk[0]))
sk_now=bytes.fromhex((sk[0]))

sig= Sign(message[0], sk_now, '123678', len_para)
sig_hex=(sig).hex()
print(sig_hex)
# for i in range(len(pk)):
#     # sk_now=bytes.fromhex(sk[i]) # hex to bit
#     # pk_now=bytes.fromhex((pk[i]))
#     message_now=((message[i]))
#     pk_now=pk[i]
#
#     # sig[i] = Sign(message_now, sk_now, '123678', len_para)
#     sig_hex=(sig[i])
#     print(sig_hex) # 存储形式
#     sig_bit=bytes.fromhex(sig_hex)  # 验证形式
#     print(sig_bit)
#     print(Verify(sig_bit, message_now, pk_now, len_para))

#
# sk = '0000000000000000000000000000000000000000000000000000000000000000'
# output = {
#     "num": 1,
#     "pk": [
#         "0000000000000000000000000000000000000000000000"],
#     "money": [50]
# }
# inputs = "0000000000000000000000000000000000000000000000000000000000000000"
# print("新的交易:", gen_tx(sk, inputs, output))