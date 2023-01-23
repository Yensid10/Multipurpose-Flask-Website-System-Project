from threading import Thread
import threading
import time


class Object:
    def __init__(self, TableNo, Request):
        self.TableNo = TableNo
        self.Request = Request


class Queue:
    def __init__(self):
        self.queue = []
        t = threading.Thread(target=self.Check_queue)
        t.start()

    def add_object(self, TableNo, Request):
        new_object = Object(TableNo, Request)
        self.queue.append(new_object)

    def AlterRequest(self, TableNum, New_Request):
        Position = -1
        for i, obj in enumerate(self.queue):
            if obj.TableNo == TableNum:
                Position = i
        if (Position >= 0):
            self.queue[Position].Request = New_Request

    def Check_queue(self):
        size = len(self.queue)
        while True:
            current_size = len(self.queue)
            if (current_size > size):
                print("Changed")
                size = current_size
            time.sleep(10)

    def ReadQueue(self):
        self.Temp = self.queue[0]
        print("("+self.Temp.TableNo + ", " + self.Temp.Request + ")")
        self.queue.pop(0)


queue = Queue()
queue.add_object('14', "Please bring some water")
queue.ReadQueue()
# queue.add_object('15', "Please bring some bread")
# print(queue.queue[1].Request)
# queue.AlterRequest('15', "Please bring some water")
# print(queue.queue[1].Request)
# p = threading.Thread(target=queue.Check_queue)
# p.start()
