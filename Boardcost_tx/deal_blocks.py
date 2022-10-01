import os

class Bit_Blocks:
    """
    读取所有的本机区块
    """
    def __init__(self,dir="../blocks"):
        self.len=0
        self.dir=dir
    def gen_newest(self):
        """
        返回最新的一个block数据
        :return:
        """
        names=os.listdir(self.dir)
        names=sorted(names,key=len)
        print(names)
        try:
            last_block=sorted(names[-2:],reverse=False)
        except Exception as e:
            # 说明只有一个block,即创世区块
            print("错误",e)
            return names[0]

        print(last_block)
        print(last_block[-1])
        return last_block[-1]



    def gen_second(self):
            """
            返回最新的一个block数据
            :return:
            """
            names = os.listdir(self.dir)
            names = sorted(names, key=len)
            try:
                last_block = sorted(names[-2:], reverse=True)
            except Exception as e:
                return names[0]

            return last_block[-2]

    def gen_last_num(self):
        last_name=self.gen_newest()
        num=int(last_name[len("tx_block"):-len(".txt")])
        return num

    def gen_items(self,name=""):
        if name=="":
            name=self.gen_newest()
        path=os.path.join(self.dir, name)


        block_message={
                "previoushash": "dasdasdsda",
                 "time": 454545,
                 "nonce": 58445,
                 "difficulty": 8,
                 "transactionhash": "ce0e68fc0865473ab791c67f00f010530ba38253cd9043808eac973bd585f00b",
                "transaction":[]
        }
        count =0
        """
         if count==0:
                    block_message["previoushash"]=line.strip()[len("previoushash:"):]
                # if "time" in line:
                elif count == 1:
                    block_message["time"]=int(line.strip()[len("time:"):])
                # if "nonce" in line:
                elif count == 2:
                    block_message["nonce"]=int(line.strip()[len("nonce:"):])
                # if "difficulty" in line:
                elif count == 3:
                    block_message["difficulty"]=int(line.strip()[len("difficulty:"):])
                # if "transactionhash" in line:
                elif count == 4:
                    block_message["transactionhash"]=line.strip()[len("transactionhash:"):]
                else:
                    block_message["transaction"].append()
        """
        with open(path, "r") as f:
            for line in f.readlines():

                # if "previoushash" in line:
                if count==0:
                    block_message["previoushash"]=line.strip()
                # if "time" in line:
                elif count == 1:
                    block_message["time"]=int(line.strip())
                # if "nonce" in line:
                elif count == 2:
                    block_message["nonce"]=int(line.strip())
                # if "difficulty" in line:
                elif count == 3:
                    block_message["difficulty"]=int(line.strip())
                # if "transactionhash" in line:
                elif count == 4:
                    block_message["transactionhash"]=line.strip()
                else:
                    block_message["transaction"].append(line.strip())
                count+=1
        return block_message



class TXT_operation:
    def __init__(self, file_path=r"./UTXO.txt"):
        self.file_path = file_path
        self.len=0
        self.gen_len()

    def read_UTXO(self):
        lines = []
        with open(self.file_path, "r") as f:
            # print(f)
            # print(f.read())
            for i in f.readlines():
                lines.append(i.strip())  # 去除结尾换行符号
                # lines.append(i)

            return lines
    def gen_len(self):
        """
        返回transaction的个数
        :return:
        """
        with open(self.file_path, "r") as f:
            sss=f.read()
            num=sss.count("transaction:")
        self.len=num

    def print_file(self):
        with open(self.file_path, "r") as f:
            print(f.read())

    def add(self, str_list):
        """
        加入新的元素
        :param str_list:
        :return:
        """
        lines = self.read_UTXO()
        for item in str_list:
            lines.append(item)
        self.chongxie_UTXO(lines)


    def delete(self, str_list):
        """
        消除旧的元素
        :param str_list:
        :return:
        """
        lines = self.read_UTXO()
        for item in str_list:
            if item in lines:
                lines.remove(item)  # 移除
        self.chongxie_UTXO(lines)


    def chongxie_UTXO(self, str1_list):
        """
        使用str1_list覆盖 现有的UTXO 池
        从本机的UTXO池中UTXO 记录
        :param str1:
        :return:
        """
        with open(self.file_path, "w") as f:
            # B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E246202075a
            for line in str1_list:
                if line!=None:
                    f.write(line)
                    f.write("\n")
        self.gen_len()



if __name__=="__main__":
    D=Bit_Blocks()
    D.gen_newest()
    print(D.gen_last_num())
    print(D.gen_items())