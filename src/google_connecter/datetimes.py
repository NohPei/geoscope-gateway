import time


def getDate():
    return time.strftime('%Y-%m-%d')


def main():
    print(f"Date: {getDate()}")


if __name__ == '__main__':
    main()
