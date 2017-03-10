def output(lock, message):
    lock.acquire()
    print(message)
    lock.release()