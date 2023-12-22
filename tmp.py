import time


def clock(start: int,
          stop=0):
    while start > stop:
        start -= 1
        print(start)
        time.sleep(1)
    
clock(11)