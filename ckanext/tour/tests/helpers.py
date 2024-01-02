from werkzeug.datastructures import FileStorage as MockFileStorage  # noqa

IMAGE_DATA = b"a,b,c,d\n1,2,3,4"


class FakeFileStorage(MockFileStorage):
    content_type = None

    def __init__(self, stream, filename):
        self.stream = stream
        self.filename = filename
        self.name = "upload"
