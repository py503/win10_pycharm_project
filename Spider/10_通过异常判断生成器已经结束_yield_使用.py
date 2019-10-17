def create_num(all_num):
    # a = 0
    # b = 1
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        print(a)
        # 如查一个函数中有yield语句,那么这个就不在是函数,而是一个生成器的模板
        yield a
        a, b = b, a + b
        current_num += 1
    # return "Ok....."
# 创建一个对象
obj1 =  create_num(20)

# print(next(obj1))
#

while True:
    try:
        ret = next(obj1)
        print(ret)
    except Exception as e:
        print(e)