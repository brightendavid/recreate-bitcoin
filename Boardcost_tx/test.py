from Boardcost_tx.server import TXT_operation


if __name__ =="__main__":
    T=TXT_operation("../blocks/tx_block0.txt")
    T.print_file()

    T.add(["111"])
    T.print_file()
    T.add(["111"])
    T.print_file()
    print(T.len)