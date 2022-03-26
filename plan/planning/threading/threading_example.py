import threading 

def Method1():
    print("method 1 is running\n")
    return
def Method2():
    print("method 2 is running\n")
    return

def StartThreads():
    print("Current number of threads open is",threading.active_count())
    thread1=threading.Thread(target=Method1,daemon=True);thread1.start()
    thread2=threading.Thread(target=Method2,daemon=True);thread2.start()
while True:
    StartThreads()

