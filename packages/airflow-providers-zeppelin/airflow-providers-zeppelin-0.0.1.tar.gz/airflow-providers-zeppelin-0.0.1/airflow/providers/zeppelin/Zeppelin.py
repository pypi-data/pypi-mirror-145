
class Zeppelin():

    def __init__(self, note_id, name='', path='', paragraphs='[]'):
        self.__note_id = note_id
        self.__name = name
        self.__path = path
        self.__paragraphs = paragraphs

    @property
    def note_id(self):
        return self.__note_id

    @note_id.setter
    def note_id(self, note_id):
        self.__note_id = note_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def paragraphs(self):
        return self.__paragraphs

    @paragraphs.setter
    def paragraphs(self, paragraphs):
        self.__paragraphs = paragraphs

    def __str__(self):
        return '{"note_id":"%s","name":"%s","path":"%s","paragraphs":"%s"}' % (self.note_id, self.name, self.path, self.paragraphs)

    def __eq__(self, other):
        if self.note_id == other.note_id:
            return True
        else:
            return False
