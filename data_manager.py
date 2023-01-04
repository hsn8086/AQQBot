import os.path
from os import path


class DataManager:
    def __init__(self, fp: str = 'data'):
        self.fpp = fp
        if not os.path.exists(fp):
            os.makedirs(fp)
        self.open = self._open(fp)

    class _open:
        def __init__(self, fp: str):
            self.fp = fp

        def __call__(self, p: str, model, encoding='utf8'):
            self.filename = os.path.join(self.fp, *p.split('.'))
            if not os.path.exists(os.path.split(self.filename)[0]):
                os.makedirs(os.path.split(self.filename)[0])
            self.model = model
            self.encoding = encoding
            return self

        def __enter__(self):
            self.f = open(self.filename, self.model, encoding=self.encoding)
            return self.f

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.f.close()
            return True
