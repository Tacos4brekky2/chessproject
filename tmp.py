from collections.abc import Callable, Iterable, Mapping
import time
from threading import Thread
from typing import Any
import random

class clock(Thread):
        def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None, seconds: int) -> None:
              super().__init__(group, target, name, args, kwargs, daemon=daemon)
              self.seconds = seconds
        def run(self):
            if self.seconds == 0:
                return "WHITE TIME OUT"
            print(self.seconds)
            time.sleep(1)
            self.seconds -= 1
            self.run()

#ticker = clock(seconds=10)
#ticker.run()
            
class ThreadTest(Thread):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.time = random.randint(3, 9)
    
    def run(self):
        time.sleep(self.time)
        print(f'\nThread: {self.name}\nTime: {self.time}')

    


def test():
    for i in range(1, 6):
        name = f'thread_{i}'
        thread = ThreadTest(name)
        thread.start()        

#test()

def run(seconds: int):
    if seconds == 0:
        return "WHITE TIME OUT"
    print(seconds)
    time.sleep(1)
    run(seconds - 1)