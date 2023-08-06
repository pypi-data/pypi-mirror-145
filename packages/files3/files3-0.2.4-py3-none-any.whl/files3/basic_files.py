import os
import pickle
import pickle
import shutil
from files3.PfBool import *
from files3.Singleton import *
from files3.InfoPackage import *

class BasicMeta(Singleton): ...
# 所有的pyfile_basic_files均为同一对象
# All pyfile_basic_files are the same object


# 不能直接使用，需要在pyfile_shell加壳后使用
# It cannot be used directly. It needs to be used after (pyfile_shell) shelling
class pyfile_basic_files(object, metaclass=BasicMeta):
    _pflevel = 0
    def has(self, info, key:str)->PfBool:
        """
        增删改查之番外-事先确认。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
        Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        _path = info(key)
        if os.path.exists(_path): return PfTrue
        return PfFalse

    def new(self, info, key:str, pyobject:object)->PfBool:
        """
        增删改查之'增'。成功返回PfTrue，如果目标文件已存在，则返回PfFalse
        Add a new pyfile file. Returns True successfully, or False if the target file already exists

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        _path = info(key)
        if os.path.exists(_path): return PfFalse

        try:
            pickle.dump(pyobject, open(_path, "wb"))
            return PfTrue
        except Exception as err:
            if isinstance(err, SaveSelfError): raise err
            return PfFalse

    def delete(self, info, key:str)->PfBool:
        """
        增删改查之'删'。成功或目标文件不存在则返回PfTrue，如果目标文件存在而无法删除，则返回PfFalse
        Delete pyfile file. Returns True if the target file is successful or does not exist. Returns False if the target file exists and cannot be deleted

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        _path = info(key)
        if not os.path.exists(_path): return PfTrue
        try:
            os.remove(_path)
            return PfTrue
        except:
            return PfFalse

    def modify(self, info, key:str, pyobject:object)->PfBool:
        """
        增删改查之'改'。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
        Modify existing data files. Returns True successfully, or False if the target file does not exist

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        _path = info(key)
        if not os.path.exists(_path): return PfFalse

        try:
            pickle.dump(pyobject, open(_path, "wb"))
            return PfTrue
        except Exception as err:
            if isinstance(err, SaveSelfError): raise err
            return PfFalse

    def get(self, info, key:str) -> object:
        """
        增删改查之'查'。成功返回读取到的pyobject，如果目标文件不存在，则返回PfFalse
        Find data files. The read pyobject is returned successfully. If the target file does not exist, false is returned

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        _path = info(key)
        if not os.path.exists(_path): return PfFalse

        try:
            return pickle.load(open(_path, 'rb'))
        except:
            return PfFalse

if __name__ == '__main__':
    print(PfTrue == True)
    print(PfTrue is True)
