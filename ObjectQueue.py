from threading import Thread
import threading
import time


class Order:
    # def __init__(self, TableNo, Note):
    #     self.TableNo = TableNo
    #     self.Note = Note

    def __init__(self, Note, TableNo):
        self.TableNo = TableNo
        self.Note = Note
        # self.Price = Price

    def getTableNo(self):
        return self.TableNo

    def getNote(self):
        return self.Note

    # def getPrice(self):
    #     return self.Price


class Queue:
    def __init__(self):
        self.queue = []
        t = threading.Thread(target=self.Check_queue)
        t.start()

    def add_object(self, Note, TableNo):
        new_object = Order(Note, TableNo)
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
            time.sleep(1)

    def ReadQueue(self):
        for order in self.queue:
            print(order.getNote() + " " + order.getTableNo())

    def getQueue(self):
        return self.queue

    def getOrder(self, index):
        return self.queue[index]

    def getQueueLength(self):
        return len(self.queue)
    # Use the above functions in my HTML code instead

# queue = Queue()
# queue.add_object('14', "Please bring some water")
# queue.ReadQueue()
# queue.add_object('15', "Please bring some bread")
# print(queue.queue[1].Request)
# queue.AlterRequest('15', "Please bring some water")
# print(queue.queue[1].Request)
# p = threading.Thread(target=queue.Check_queue)
# p.start()
