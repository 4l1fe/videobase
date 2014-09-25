#coding:utf-8
from django.core.files.storage import FileSystemStorage
from hashlib import md5


class OverWriteFileStorage(FileSystemStorage):
    """Класс преназначен для перезаписи файла на диске при загрузке аватарки
    """

    def save(self, name, content):
        if self.exists(name):
            existed_file = self.open(name=name)
            hash1 = md5(existed_file.read()).hexdigest()
            hash2 = md5(content).hexdigest()
            if hash1 == hash2:
                self.delete(name)
            existed_file.close()
        res = super(OverWriteFileStorage, self).save(name, content)
        return res