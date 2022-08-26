import time


class Timer:
    def __init__(self):
        # timer setup
        self.total_time = 150 # seconds
        self.start_time = time.time()

        # pause setup
        self.paused = False
        self.pause_time = 0
        self.offset = 0

    def pause(self):
        # pause timer
        self.paused = True
        self.pause_start = time.time()

    def unpause(self):
        # unpause timer
        self.paused = False
        self.pause_time = time.time() - self.pause_start
        # offset keeps track of how long the game was paused in total
        self.offset += self.pause_time

    def get_time_elapsed(self):
        # return elapsed time to 2 decimal places
        if self.paused:
            # return the time that was on the timer when the game was paused
            return round(self.pause_start - self.start_time - self.offset)
        return round(time.time() - self.start_time - self.offset)

    def get_timer_time(self):
        # return timer time as a string in format MM:SS
        seconds = self.total_time - self.get_time_elapsed()
        m, s = divmod(seconds,60)
        return f'{m}:{s:02}' # ensure seconds is given to 2 digits, adding a leading zero if necessary

