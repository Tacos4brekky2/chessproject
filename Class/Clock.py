from collections.abc import Callable, Iterable, Mapping
import threading
from threading import Thread
from typing import Any
import time


class PlayerClock(Thread):
    def __init__(self, time: int, color: int, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.time = time
        self.color = color
        self.__flag = threading.Event()
        self.__running = threading.Event()
        self.__running.set()


    def run(self):
        while self.__running.isSet():
            if self.time == 0:
                print(f'{self.color} TIME OUT')
                self.stop()
            self.__flag.wait()
            time.sleep(1)
            self.time -= 1
            print(f'{self.color} TIME: {self.time}')

    
    def pause(self):
        self.__flag.clear()

    
    def resume(self):
        self.__flag.set()

    
    def stop(self):
        self.__flag.set()
        self.__running.clear()
                