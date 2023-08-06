import os
import pickle
import shutil
from files3.PfBool import *
from files3.Singleton import *
from files3.basic_files import pyfile_basic_files

class Meta(Singleton): ...
# 所有的pyfile_files均为同一对象
# All pyfiles_files are the same object

# 不能直接使用，需要在pyfile_shell加壳后使用
# It cannot be used directly. It needs to be used after (pyfile_shell) shelling
class pyfile_files(object, metaclass=Meta):
    _pflevel = 1
    backend:pyfile_basic_files = pyfile_basic_files()

    has = backend.has  #(self, info, key:str)->PfBool:
    """
    增删改查之番外-事先确认。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
    Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    """

    def set(self, info, key:str, pyobject:object)->PfBool:
        """
        存储python对象到目标文件夹下。成功返回PfTrue，如果目标文件被锁定或占用，则返回PfFalse
        Storing Python objects to pyfile under specific path in InfoPackage. Returns True successfully. If the target file is locked or occupied, returns False

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        """
        if self.backend.new(info, key, pyobject) is PfTrue:
            return PfTrue
        elif self.backend.modify(info, key, pyobject) is PfTrue:
            return PfTrue
        else:
            return PfFalse

    get = backend.get  # (self, info, key:str)->PfBool:
    """
    从目标文件夹下读取pyfile到python对象。成功返回读取到的pyobject，如果目标文件不存在，则返回PfFalse
    Read the pyfile under specific path in InfoPackage from the target folder to the python object. The read pyobject is returned successfully. If the target file does not exist, false is returned

    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    """

    delete = backend.delete  # (self, info, key:str)->PfBool:
    """
    从目标文件夹下删除pyfile文件。成功或目标文件不存在则返回PfTrue，如果目标文件存在而无法删除，则返回PfFalse
    Delete the target pyfile. Returns true if the target file is successful or does not exist. Returns false if the target file exists and cannot be deleted
    
    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    """

    def list(self, info, type=False)->list:
        """
        列举目标文件夹下所有info.type类型的文件的key。返回一个列表结果
        List all info of keys (In the target folder The key of a file of type). Returns a list result

        :param info:     InfoPackage inst
        :param type:     whether with suffix or not
        """
        _return, _len = [], len(info.type)
        _end = info.type if type else ""

        for fname in os.listdir(info.path):
            _key, _type = os.path.splitext(fname)
            if _type == info.type: _return += [_key + _end]

        return _return

    # def migrate(self, info, packname)->bool:
    #     """
    #     将目标目录下所有数据文件进行打包，打包为$packname.$info.type + 's'
    #     Package all data files in the target directory as $packname$ info. type + 's'
    #     """