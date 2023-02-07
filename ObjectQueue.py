class Task:
    def __init__(self, Note, TableNo):
        self.TableNo = TableNo
        self.Note = Note

    def getTableNo(self):
        return self.TableNo

    def getNote(self):
        return self.Note


class Queue:
    def __init__(self):
        self.queue = []

    def addObject(self, Note, TableNo):
        self.queue.append(Task(Note, TableNo))

    def popFrontObject(self):
        return self.queue.pop(0)

    def getObject(self, index):
        return self.queue[index]

    def getLength(self):
        return len(self.queue)

class Notes:
    def __init__(self, Order, OrderNotes):
        self.Order = Order
        self.OrderNotes = OrderNotes

    def getOrder(self):
        return self.Order

    def getOrderNotes(self):
        return self.OrderNotes

class Orders:
    def __init__(self):
        self.queue = []

    def addOrder(self, Order, OrderNotes):
        self.queue.append(Notes(Order, OrderNotes))

    def popFrontOrder(self):
        return self.queue.pop(0)

    def getOrders(self, index):
        return self.queue[index]

    def getLength(self):
        return len(self.queue)
    
    def print(self):
        for e in self.queue:
            print(e)