from threading import Thread
import threading
import time


class Task:
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
        t = threading.Thread(target=self.checkQueue)
        t.start()

    def addObject(self, Note, TableNo):
        new_object = Task(Note, TableNo)
        self.queue.append(new_object)

    def popFrontObject(self):
        # if (len(self.queue) == 0):
        #     return None
        # task = self.queue[0]
        self.queue.pop(0)

    def getOrder(self, index):
        return self.queue[index]

    def getLength(self):
        return len(self.queue)

    def checkQueue(self):
        size = len(self.queue)
        while True:
            current_size = len(self.queue)
            if (current_size > size or current_size < size):
                print("Changed")
                return "Changed"
            time.sleep(1)

    # def alterRequest(self, TableNum, New_Request):
    #     Position = -1
    #     for i, obj in enumerate(self.queue):
    #         if obj.TableNo == TableNum:
    #             Position = i
    #     if (Position >= 0):
    #         self.queue[Position].Request = New_Request

    # def printQueue(self):
    #     for order in self.queue:
    #         print(order.getNote() + " " + order.getTableNo())

    # def getQueue(self):
    #     return self.queue

# queue = Queue()
# queue.add_object('14', "Please bring some water")
# queue.ReadQueue()
# queue.add_object('15', "Please bring some bread")
# print(queue.queue[1].Request)
# queue.AlterRequest('15', "Please bring some water")
# print(queue.queue[1].Request)
# p = threading.Thread(target=queue.Check_queue)
# p.start()
