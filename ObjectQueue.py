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
        self.queue.pop(0)

    def getObject(self, index):
        return self.queue[index]

    def getLength(self):
        return len(self.queue)
