class Notes:
    def __init__(self, Note1, Note2):
        self.Note1 = Note1
        self.Note2 = Note2

    def getNote1(self):
        return self.Note1

    def getNote2(self):
        return self.Note2


class Queue:
    def __init__(self):
        self.queue = []

    def addObject(self, Note1, Note2):
        self.queue.append(Notes(Note1, Note2))

    def popFrontObject(self):
        return self.queue.pop(0)

    def getObject(self, index):
        return self.queue[index]

    def getLength(self):
        return len(self.queue)
