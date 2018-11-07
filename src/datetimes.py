import time


class date_time:
    date = ""
    time = ""
    timestamp = ""
    current_day = ""
    new_day = False

    def __init__(self):
        self.current_day = time.strftime("%d")
        self.now()

    def now(self):
        if self.current_day != time.strftime("%d"):
            self.new_day = True
            self.current_day = time.strftime("%d")
        self.timestamp = int(round(time.time() * 1000))
        self.date = time.strftime("%Y-%m-%d")
        self.time = time.strftime("%Y-%m-%dT%H-%M-%S")


def main():
    date_t = date_time()
    print(f"Date: {date_t.date}")
    print(f"Date: {date_t.time}")


if __name__ == "__main__":
    main()
