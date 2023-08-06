from random import randint

# 10**n 查找表
searchMax = 32
searchTable = []
for i in range(searchMax):
    searchTable.append(10*10**i - 1)

def NewRandom(ulen=16):  # 本机测试:1.5us生成1次
    assert 0 < ulen <= searchMax, "[ulen] can not over than {} and less than 0".format(searchMax)
    return randint(0, searchTable[ulen-1])


def NewRandomID(ulen=16):  # 本机测试:3us生成1次
    return ("{:0>" + str(ulen) + "d}").format(NewRandom(ulen))


if __name__ == '__main__':
    @fn_timer
    def test(times, ulen=32):
        for i in range(times):
            NewRandomID(ulen)

    print(NewRandomID(16))
    test(10000)
    test(10000)
    test(10000)
    test(10000)