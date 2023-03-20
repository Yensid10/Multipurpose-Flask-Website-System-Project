class Notes:
    def __init__(self, Note1, Note2):
        """
        A class that represents notes.

        Parameters:
        Note1 (int): The first note.
        Note2 (str): The second note.

        Returns:
        None
        """
        self.Note1 = Note1
        self.Note2 = Note2

    def getNote1(self):
        """
        Returns the first note.

        Parameters:
        None

        Returns:
        int: The first note.
        """
        return self.Note1

    def getNote2(self):
        """
        Returns the second note.

        Parameters:
        None

        Returns:
        str: The second note.
        """
        return self.Note2


class Queue:
    def __init__(self):
        """
        A class that represents a queue.

        Parameters:
        None

        Returns:
        None
        """
        self.queue = []

    def addObject(self, Note1, Note2):
        """
        Adds an object to the queue.

        Parameters:
        Note1 (int): The first note.
        Note2 (str): The second note.

        Returns:
        None
        """
        self.queue.append(Notes(Note1, Note2))

    def popFrontObject(self):
        """
        Removes and returns the first object in the queue.

        Parameters:
        None

        Returns:
        Notes: The first object in the queue.
        """
        return self.queue.pop(0)

    def getObject(self, index):
        """
        Returns the object at the specified index.

        Parameters:
        index (int): The index of the object to return.

        Returns:
        Notes: The object at the specified index.
        """
        return self.queue[index]

    def getLength(self):
        """
        Returns the length of the queue.

        Parameters:
        None

        Returns:
        int: The length of the queue.
        """
        return len(self.queue)

    def getSpecificOrder(self, tableNo):
        """
        Returns the second note of the first object in the queue where the first note matches the specified table number.

        Parameters:
        tableNo (int): The table number to search for.

        Returns:
        str or bool: The second note of the first object in the queue where the first note matches the specified table number, or False if no match is found.
        """
        for i in range(self.getLength()):
            if self.getObject(i).getNote1() == tableNo:
                return self.getObject(i).getNote2()
        return False

    def popSpecificOrder(self, tableNo):
        """
        Removes and returns the second note of the first object in the queue where the first note matches the specified table number.

        Parameters:
        tableNo (int): The table number to search for.

        Returns:
        str or bool: The second note of the first object in the queue where the first note matches the specified table number, or False if no match is found.
        """
        for i in range(self.getLength()):
            if self.getObject(i).getNote1() == tableNo:
                return self.queue.pop(i).getNote2()
        return False
