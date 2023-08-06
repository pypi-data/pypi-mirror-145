import os
import pickle
import shutil
from files3.PfBool import *
from files3.Singleton import *
from files3.InfoPackage import *
from files3.files import pyfile_files
from files3.pycrypt import Encrypter, EncryptInfo


class ExMeta(Singleton): ...
# 所有的pyfile_ex_files均为同一对象
# All pyfiles_files are the same object

# 不能直接使用，需要在pyfile_shell加壳后使用
# It cannot be used directly. It needs to be used after (pyfile_shell) shelling
class pyfile_ex_files(object, metaclass=ExMeta):
    _pflevel = 2
    backend: pyfile_files = pyfile_files()

    has = backend.has  # (self, info, key:str)->PfBool:
    """
    增删改查之番外-事先确认。成功返回PfTrue，如果目标文件不存在，则返回PfFalse
    Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    """

    set = backend.set  # (self, info, key: str, pyobject: object)->PfBool
    """
    存储python对象到目标文件夹下。成功返回PfTrue，如果目标文件被锁定或占用，则返回PfFalse
    Storing Python objects to pyfile under specific path in InfoPackage. Returns True successfully. If the target file is locked or occupied, returns False

    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    :param pyobject: python对象   python object
    """

    def get(self, info, key:str)->PfBool:
        """
        从目标文件夹下读取pyfile到python对象。成功返回读取到的pyobject，如果目标文件不存在，则返回PfFalse
        Read the pyfile under specific path in InfoPackage from the target folder to the python object. The read pyobject is returned successfully. If the target file does not exist, false is returned

        如果目标是加密文件，pyfile会尝试进行解密。成功解密则返回解密后的数据，未成功则返回该加密文件的加密信息。
        If the target is an encrypted file, pyfile attempts to decrypt it. If the decryption is successful, the decrypted data will be returned; if not, the encrypted information of the encrypted file will be returned.

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        get = self.backend.get(info, key)

        if isinstance(get, EncryptInfo):
            encrypter = Encrypter()
            entry_file = info(key)
            entry_info = InfoPackage(info.temp)

            # 迭代(伪递归) 多层
            while (isinstance(get, EncryptInfo)):
                key = encrypter.genkey(get.fname, get.btype, get.ftype, get.local);
                iv = Encrypter.hash16(key);

                crypt = open(os.path.join(info.path, get.fname + get.ftype), 'rb').read()
                plain_bytes = encrypter.decrypt(crypt, key, iv)

                open(os.path.join(info.temp, "ex_files_get" + entry_info.type), 'wb').write(plain_bytes)

                get = self.backend.backend.get(entry_info, "ex_files_get")
        # elif get is PfFalse:  # 合并了   same with noram return
        #     return PfFalse
        return get

    delete = backend.delete  # (self, info, key:str)->PfBool:
    """
    从目标文件夹下删除pyfile文件。成功或目标文件不存在则返回PfTrue，如果目标文件存在而无法删除，则返回PfFalse
    Delete the target pyfile. Returns true if the target file is successful or does not exist. Returns false if the target file exists and cannot be deleted

    :param info:     InfoPackage inst
    :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
    """

    list = backend.list  # (self, info) -> list
    """
    列举目标文件夹下所有info.type类型的文件的key。返回一个列表结果
    List all info of keys (In the target folder The key of a file of type). Returns a list result

    :param info:     InfoPackage inst
    """

    def encrypt(self, info, key:str, local=False)->PfBool:
        """
        对名称为key的pyfile文件进行加密, 成功返回PfTrue，失败返回PfFalse。
        Encrypt the pyfile file named key.Returns True for success and False for failure.

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
        :param local:    是否加入本地信息, 加入本地信息后不同计算机将无法对文件进行解密
                          Whether to add local information. After adding local information, different computers will not be able to decrypt the file
        """
        get = self.backend.get(info, key)
        encrypter = Encrypter()
        crypt_info = encrypter.encrypt_file(info(key), info.aes_type, local)
        # print(crypt_info)
        return self.set(info, key, crypt_info)

    def decrypt(self, info, key:str, recursion=False)->PfBool:
        """
        对名称为key的pyfile文件进行解密, 成功返回PfTrue，失败返回PfFalse。
        Decrypt the pyfile file named key.Returns True for success and False for failure.

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                     File name. It is similar to the primary key of a database and cannot be duplicated
        :param recursion:   是否以递归的方式解密， 用于嵌套加密的解密。
                        Whether to decrypt recursively. Decryption for nested encryption.
        """
        crypt_info = self.get(info, key)
        # print(crypt_info)
        if not isinstance(crypt_info, EncryptInfo): return PfFalse
        encrypter = Encrypter()
        plain_bytes = encrypter.decrypt_file(info(key), crypt_info)
        open(info(key), 'wb').write(plain_bytes)
        os.remove(os.path.join(info.path, crypt_info.fname + crypt_info.ftype))
        return PfTrue
        try:
            ...
        except:
            return PfFalse


if __name__ == '__main__':
    from pyfile.InfoPackage import InfoPackage
    info = InfoPackage("test", aes_type=".locked")
    pf = pyfile_ex_files()
    # pf.set(info, "a", [1,2,3,4,5,6])
    pf.encrypt(info, 'a', local=True)
    print(pf.get(info, 'a'))
