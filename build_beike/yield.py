# def func():
#     for x in "ABC":
#         yield x
#
# for x in func():
#     print(x)

# def func():
#     yield from "ABC"
#
# for x in func():
#     print(x)

# def gen():
#     n = 0;
#     while True:
#         yield n
#         n += 1
# g = gen()
# print(g)
# print(next(g)) # 返回0
# print(next(g)) # 返回1

def func():
    n = 0
    while True:
        s = yield n
        if s is None:
            break
        n += 1
    return n
def deligate():
    res = yield from func()
    print("the result is: %s" % res)

def main():
    d = deligate()
    next(d)
    # print(next(d))
    for i in range(3):
        print(d.send(i))
    try:
        d.send(None)
    except StopIteration:
        pass
if __name__ == '__main__':
    main()