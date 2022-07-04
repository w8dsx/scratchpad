from enum import Enum
import os
import time
import hashlib
import abc

class sysobject():
    def __init__(self):
        pass


class server(sysobject):
    def __init__(self, **kwargs):
        # Primary properties
        try:
            self.rootDirectory=kwargs['rootDir']
            self._status=True
            self._filesSystems=[]
        except:
            self._status=False

        # Secondary Properties
        _path=appPath(directory=self.rootDirectory)
        _path.findFiles()
        self._filesSystems.append(_path)

    def fetch(self, path):
        _path=appPath(path)
        self._filesSystems.append(_path)

    def fileSystems(self):
        return self._filesSystems

    def status(self):
        return self._status

    def __repr__(self):
        _output='\nserver report'
        for _f in self._filesSystems:
            _output+=repr(_f)
        return _output

    def __len__(self):
        return len(self._filesSystems)

# described as appPath, this is primarily used for operations on application paths
# and not system directories that could require root access.

class appPath():
    def __init__(self,**kwargs):
        try:
            self._fileSystemDirectory=kwargs['directory']
            self._status=True
            self._files=[]
        except:
            print('appPath error!')
            self._status=False

    def findFiles(self):
        if self._status:
            print(self._fileSystemDirectory)
            for _root, _dirs, _files in os.walk(self._fileSystemDirectory):
                for _fileNumber, _fileName in enumerate(_files):
                    _fullPath=os.path.join(_root, _fileName)
                    _fileSize=os.stat(_fullPath).st_size
                    _lastAccess=os.stat(_fullPath).st_atime
                    _lastModification=os.stat(_fullPath).st_mtime
                    self._files.append(file(
                        fileName=_fileName,
                        path=_root,
                        fileSize=_fileSize,
                        lastModification=_lastModification,
                        lastAccess=_lastAccess
                    ))

    def files(self):
        return self._files

    def count(self):
        return len(self._files )

    def status(self):
        return self._status

    def __repr__(self):
        _output='\n'
        _output+=self._fileSystemDirectory
        for _file in self._files:
            _output+='\n'
            _output+=repr(_file)
        return _output

    def __len__(self):
        return len(self._files)

    def __iter__(self):
        self.itemno=0
        return self

    def __next__(self):
        if self.itemno>=(len(self._files)-1):
            raise StopIteration
        else:
            self.itemno += 1
            return self._files[self.itemno]




class file(sysobject):
    def __init__(self, **kwargs):
        # Primary properties
        try:
            self._name = kwargs['fileName']
            self._status = True
        except:
            self._status = False
        # Extended properties
        self.path=kwargs['path'] if 'path' in kwargs else ""
        self._size = kwargs['fileSize'] if('fileSize' in kwargs) else ""
        self._lastModification = self.timeconvert(kwargs['lastModification']) if('lastModification' in kwargs) else ""
        self._lastAccess = self.timeconvert(kwargs['lastAccess']) if('lastAccess' in kwargs) else ""

    def timeconvert(self,epochtime):
        _time=time.gmtime(epochtime)
        return time.strftime('%Y-%m-%d %H:%M:%S',_time)

    def __repr__(self):
        _output=""
        #for _attr, _value in self.__dict__.items():
        _output+=f'Filename: {self._name}'
        _output+=f' Size: {(self._size/1000)}M'
        _output+=f' Date: {self._lastModification}'
        return _output

    def __str__(self):
        return self._name

    def __iter__(self):
        return(self)

    def __next__(self):
        return self

    @property
    def extension(self):
        return self._name.split(".")[1]

    @property
    def size(self):
        return self._size

    @property
    def name(self):
        return self._name

    @property
    def lastaccess(self):
        return self._lastAccess

    @property
    def lastmodification(self):
        return self._lastModification





