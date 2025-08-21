def build_uri(id, value):
    return "{id}-{value}".format(id=id, value=value.replace(' ', '-').lower())