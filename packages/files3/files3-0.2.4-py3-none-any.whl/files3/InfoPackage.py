import os
import shutil
from files3.PfBool import *

class InfoPackage(object):
    path = "/"
    temp = "/.pftemp"
    type = ".object"
    aes_type = ".aes"

    def __init__(self, path:str, type:str=".inst", aes_type=".aes"):
        # 记录工作位置    Record working position
        self.NewPath(path)

        # 记录数据文件后缀  Record data file suffix
        self.NewType(type)

        # 记录加密文件的后缀 Record the suffix of the encrypted file
        self.NewAesType(aes_type)

        # 开辟缓冲区 Prepare directory buffer
        self.OpenTemp(".pftemp", ignore=True)  # ignore overwrite error

    def NewPath(self, path:str):
        """
        指定新的数据文件目录
        :param type: str    带.      contain .
        :return:
        """
        self.path = os.path.abspath(path)
        if not os.path.exists(self.path):  #  "directory {} doesn't exists.".format(self.path)
            os.makedirs(self.path)

    def NewType(self, type:str):
        """
        指定新的数据文件后缀
        :param type: str    带.      contain .
        :return:
        """
        self.type = type
        assert type[0] == '.', "'type'[0] must be '.'"

    def NewAesType(self, aes_type:str):
        """
        指定新的AES文件后缀
        :param aes_type: str    带.      contain .
        :return:
        """
        self.aes_type = aes_type
        assert aes_type[0] == '.', "'aes_type'[0] must be '.'"

    def OpenTemp(self, tmp_name="temp", ignore=False):
        """
        在path下开辟临时缓冲目录
        :param tmp_name: 临时目录名称
        :return:
        """
        _path = os.path.join(self.path, tmp_name)
        assert ignore or not os.path.exists(_path), "Temp Path already exists. If that's last temp or just need overwrite it , please set ignore=True"
        if os.path.exists(_path):
            if os.path.isfile(_path): os.remove(_path)
            else: shutil.rmtree(_path)

        os.mkdir(_path)
        self.temp = _path

    def __call__(self, key:str)->str:
        """
        生成key的完整路径
        Generate the full path of the key
        """
        return os.path.join(self.path, key + self.type)
