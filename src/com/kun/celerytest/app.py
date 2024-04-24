import time
from task import kun_add
if __name__=="__main__":
    print("start...")
    result = kun_add.delay(5,6)
    print("end...")
    print(result)