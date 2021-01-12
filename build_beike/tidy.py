totalList = []

def del_same(list):
    if len(list) > 0:
        res_list = [list[0]]
        for i in list:
            flag = False
            for j in res_list:
                if i == j:
                    flag = True
            if not flag:
                res_list.append(i)
        return res_list
    else:
        return list
res = del_same(totalList)
print(res)
