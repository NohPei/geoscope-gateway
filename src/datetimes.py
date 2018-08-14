import time


class date_time:
    date = ""
    time = ""
    timestamp = ""

    def __init__(self):
        self.now()

    def now(self):
        self.timestamp = int(round(time.time() * 1000))
        self.date = time.strftime('%Y-%m-%d')
        self.time = time.strftime('%Y-%m-%dT%H-%M-%S')


def main():
    date_t = date_time()
    print(f"Date: {date_t.date}")
    print(f"Date: {date_t.time}")


if __name__ == '__main__':
    main()
