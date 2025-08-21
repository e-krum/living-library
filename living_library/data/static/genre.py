from enum import Enum

class Genre(Enum):
    ACTION_ADVENTURE = (0, 'Action & Adventure')
    CLASSIC = (1, 'Classical')
    CONTEMPORARY_FICTION = (2, 'Contemporary Fiction')
    DYSTOPIAN = (3, 'Dystopian')
    FANTASY = (4, 'Fantasy')
    HISTORICAL_FICTION = (5, 'Historical Fiction')
    HORROR = (6, 'Horror')
    MYSTERY = (7, 'Mystery')
    ROMANCE = (8, 'Romance')
    SCIENCE_FICTION = (9, 'Science Fiction')
    STEAMPUNK = (10, 'Steampunk')
    THRILLER = (11, 'Thriller')
    WESTERN = (12, 'Western')

    def __init__(self, id, value):
        self.id = id
        self.value = value
