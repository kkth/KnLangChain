from com.kun.itest.mycalbase import CalBase


class MyAdd(CalBase):
    num_a = 0.0

    def __init__(self, num):
        print("MyAdd.init() is called")
        self.num_a = num

    def cal(self, num):
        return self.num_a + num


class MyRevert(CalBase):

    def __init__(self):
        print("MyRevert.init() is called")

    def cal(self, val):
        return -1*val


my_add = MyAdd(5.0)


class MyClass:
    def __init__(self):
        print("Initializing MyClass instance")
