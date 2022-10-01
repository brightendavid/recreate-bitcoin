from Gen_tx.gen_jiaoyi import tx


def anylize(transaction):
    money=[]
    max=0
    maxi=0
    for trans in transaction:
        Tx=tx()
        Tx.explain(trans)
        Tx.print_all2()
        money.append(Tx.gen_money_last())
        if Tx.gen_money_last() >max:
            maxi=trans
    return maxi

if __name__=="__main__":
    transaction = ["111111111180f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac15a809b07696074b030ef85abbf81ed15543decbad3ab2b0df53b8693b1e36dd554aaa6b9fbad2019600d8ba6cbb98b739ffafa2d4e63b251649c7bcb5b618a41363b82f427eb9b91640f2c69295039b079201cfe17c5fafa037dd2a899f0e7cfebbef72b11dd84624a408377698f0df5b6e502725b8e6b0e7678d1233d4beb0406fac190401fc7aae65e1a2a6f4ebe7170e1843beb2488867444b1bd59d4cf9d2cf098be2b117f0AE4C7798AA0F119471BEE11825BE46202BB79E2A5844495E97C04FF4DF25487C0240F88F1CD4E16352A73C17B7F16F07353E53A176D684A9FE0C6BB798E857a"]

    anylize(transaction)