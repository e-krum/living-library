from living_library.data.static.genre import Genre

def build_uri(id, value):
    return "{id}-{value}".format(id=id, value=value.replace(' ', '-').lower())

def convert_genre(id):
        for genre in list(Genre):
            if genre.id == id: return genre.title