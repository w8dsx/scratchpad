from enum import Enum
import os
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
            self.myStatus=True
            self.fileSystems=[]
        except:
            self.myStatus=False

        # Secondary Properties
        _path=appPath(directory=self.rootDirectory)
        _path.findFiles()
        self.fileSystems.append(_path)

    def fetch(self, path):
        _path=appPath(path)
        self.fileSystems.append(_path)

    def filesSystems(self):
        return self.fileSystems

    @property
    def status(self):
        return self.myStatus

    def __repr__(self):
        _output='server report'
        for _f in self.fileSystems:
            _output+=repr(_f)

    def __len__(self):
        return len(self.fileSystems)


# described as appPath, this is primarily used for operations on application paths
# and not system directories that could require root access.

class appPath():
    def __init__(self,**kwargs):
        try:
            self.fileSystemDirectory=kwargs['directory']
            self.myStatus=True
            self.allFiles=[]
        except:
            print('appPath error!')
            self.myStatus=False

    def findFiles(self):
        if self.myStatus:
            print(self.fileSystemDirectory)
            for _root, _dirs, _files in os.walk(self.fileSystemDirectory):
                for _fileNumber, _fileName in enumerate(_files):
                    _fullPath=os.path.join(_root, _fileName)
                    _fileSize=os.stat(_fullPath)
                    self.allFiles.append(file(
                        fileName=_fileName,
                        fileSize=_fileSize
                    ))

    @property
    def files(self):
        return self.allFiles

    @property
    def count(self):
        return len(self.allFiles )

    @property
    def status(self):
        return self.myStatus

    def __repr__(self):
        _output=self.fileSystemDirectory
        for _files in self.allFiles:
            _output+='\n'
            _output+=repr(_files)
        return _output

    def __len__(self):
        return len(self.allFiles)

    def __iter__(self):
        return self.allFiles






class file(sysobject):
    def __init__(self, **kwargs):
        # Primary properties
        try:
            self.fileName = kwargs['fileName']
            self.myStatus = True
        except:
            self.myStatus = False
        # Extended properties
        try:
            self.fileSize = kwargs['fileSize']
        except:
            pass

    def __repr__(self):
        _output=""
        #for _attr, _value in self.__dict__.items():
        _output+=f'Filename: {self.fileName}'
        try:
            _output+=f'Size: {self.fileSize}'
        except:
            pass

        return _output

    def __str__(self):
        return self.fileName



