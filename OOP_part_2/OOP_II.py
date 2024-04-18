import sys
import os
import shutil
from tempfile import mkdtemp
import time

class MeasureTime:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Блок кода выполнен за: {self.elapsed_time:.6f} сек.")

class TmpDir:
    def __init__(self, dir_path='.', to_delete=True):
        self.dir_path = dir_path
        self.to_delete = to_delete
        self.tmp_dir_path = None

    def __enter__(self):
        self.tmp_dir_path = mkdtemp(dir=self.dir_path)
        return self.tmp_dir_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.to_delete:
            shutil.rmtree(self.tmp_dir_path)

class MyDict:
    def __init__(self, *args, **kwargs):
        self._data = {}
        self.update(*args, **kwargs)
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __delitem__(self, key):
        del self._data[key]
    
    def __iter__(self):
        return iter(self.items())
    
    def __len__(self):
        return len(self._data)
    
    def clear(self):
        self._data.clear()
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()
    
    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def __repr__(self):
        return repr(self._data)

class FastaRecord:
    def __init__(self, id, seq, description=""):
        self.id = id
        self.seq = seq
        self.description = description

    def __repr__(self):
        return f"FastaRecord(id='{self.id}', description='{self.description}', seq='{self.seq[:10]}...')"

class OpenFasta:
    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = mode
        self.file = None
        self._iterator = None

    def __enter__(self):
        self.file = open(self.filepath, self.mode)
        self._iterator = self.__iter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    def __iter__(self):
        self.file.seek(0)  # Сбросить указатель файла для повторной итерации
        current_record = None
        for line in self.file:
            if line.startswith(">"):
                if current_record:
                    yield current_record
                header = line[1:].strip().split(maxsplit=1)
                record_id = header[0]
                description = header[1] if len(header) > 1 else ''
                current_record = FastaRecord(id=record_id, seq='', description=description)
            else:
                if current_record:
                    current_record.seq += line.strip()
        if current_record:
            yield current_record

    def __next__(self):
        if self._iterator is None:
            self._iterator = self.__iter__()
        return next(self._iterator)

    def read_record(self):
        try:
            return self.__next__()
        except StopIteration:
            self._iterator = None  # Сбросить итератор для возможности повторного использования
            return None

    def read_records(self):
        return list(self.__iter__())  # Этот метод вернёт все записи с начала файла
