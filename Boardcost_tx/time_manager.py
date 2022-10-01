import _thread
import threading
import time
# 每隔一段时间运行一次的程序实现


flag=False
def printHello():
    print("Hello")
    print("当前时间戳是", time.time())


def loop_func(func, second):
    # 每隔second秒执行func函数
    # while True:
    while True:
        global flag
        if int(time.time())%second==0 and flag==True:
            func()
            flag=False
        elif int(time.time())%second!=0:
            flag=True

        # time.sleep(second)


if __name__=="__main__":
        # t=_thread.start_new_thread(loop_func, ((printHello, 2)))
        t = threading.Thread(target=loop_func, args=((printHello, 2)))
        # 启动线程
        t.start()
        while(True):
            print(1)

# print("asfdsddddddddddd")