from enum import Enum

class BookState(Enum):
    TO_BE_READ = (0, "To be Read")
    READING = (1, "Reading")
    FINISHED = (2, "Finished")

    def __init__(self, id, title):
        self.id = id
        self.title = title