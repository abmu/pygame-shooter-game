import time


class Timer:
    def __init__(self):
        # timer setup
        self.total_time = 150 # seconds
        self.start_time = time.time()

    def get_time_elapsed(self):
        # return elapsed time to 2 decimal places
        return round(time.time() - self.start_time)

    def get_timer_time(self):
        # return timer time as a string in format MM:SS
        seconds = self.total_time - self.get_time_elapsed()
        m, s = divmod(seconds,60)
        return f'{m}:{s:02}' # ensure seconds is given to 2 digits, adding a leading zero if necessary

