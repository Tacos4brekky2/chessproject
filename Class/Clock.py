from collections.abc import Callable, Iterable, Mapping
import threading
from threading import Thread
from typing import Any
import time


class PlayerClock(Thread):
    def __init__(self, time: int, starting_color: int, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.white_time = time
        self.black_time = time
        self.__white = threading.Event()
        self.__black = threading.Event()
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

        # This is because board.startTurn calling playerclock.switch is just simpler at the start, but I don't love it.
        if starting_color == 1:
            self.__black.set()
        else:
            self.__white.set()


    def run(self):
        while self.__running.isSet():
            if self.white_time == 0:
                print('WHITE TIME OUT')
                self.stop()
            elif self.black_time == 0:
                print('BLACK TIME OUT')
            if (
                (self.__flag.isSet()) and
                (self.__white.isSet())
            ):
                time.sleep(1)
                self.white_time -= 1
            elif (
                (self.__flag.isSet()) and
                (self.__black.isSet())
            ):
                time.sleep(1)
                self.black_time -= 1

    
    def pause(self):
        self.__flag.clear()

    
    def resume(self):
        self.__flag.set()

    
    def stop(self):
        self.__flag.set()
        self.__running.clear()


    def switch(self):
        if self.__white.isSet():
            self.__white.clear()
            self.__black.set()
        else:
            self.__black.clear()
            self.__white.set()
                