import time

class DigitalClock:
    def __init__(self, h=0, m=0, s=0):
        self.__hour = h
        self.__minute = m
        self.__second = s
    
    @property
    def current_time(self):
        return f"{self.__hour:02d}:{self.__minute:02d}:{self.__second:02d}"

    def __str__(self):
        return self.current_time

    def _tick(self):
        self.__second += 1
        if self.__second == 60:
            self.__second = 0
            self.__minute += 1
            if self.__minute == 60:
                self.__minute = 0
                self.__hour += 1
                if self.__hour == 24:
                    self.__hour = 0

    def run(self):
        while True:
             # end='\r' giúp quay về đầu dòng thay vì xuống dòng (\n)
            print(self.current_time, end='\r')
            self._tick()
            time.sleep(1)

if __name__ == "__main__":
    clock = DigitalClock(23, 59, 58)
    clock.run()
