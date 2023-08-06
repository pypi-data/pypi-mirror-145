import os
import platform
from binascii import b2a_hex, a2b_hex

from files3.Singleton import Singleton


class EncryptInfo(object):
    def __init__(self, aes_fname:str, before_ftype:str, aes_ftype:str, pfh_info:str, use_local:bool, local_hash16:str):
        """

        :param aes_fname:
        :param before_ftype:    # 带.
        :param aes_ftype:    # 带.
        :param pfh_info:
        :param use_local:
        :param local_hash16:
        """
        self.fname = aes_fname
        self.btype = before_ftype
        self.ftype = aes_ftype
        self.ptype = pfh_info
        self.local = use_local
        self.loc16 = local_hash16

    def __str__(self):
        return "EncryptInfo(fname={}, btype={}, ftype={}, ptype={}, local={}, loc16={})".format(self.fname, self.btype, self.ftype, self.ptype, self.local, self.loc16)

class EncrypterMeta(Singleton): ...

class Encrypter(object, metaclass=EncrypterMeta):
    from Crypto.Cipher import AES
    try:
        from files3.pyfilehash import info as pfh_info, hash16, hash32, hash64  # 自定义hash    my hash    [Only for author]
    except:
        def hash16(object):
            return bytes(bytearray(list(range(16))))
        def hash32(object):
            return bytes(bytearray(list(range(32))))
        def hash64(object):
            return bytes(bytearray(list(range(64))))

    @staticmethod
    def encrypt(text, key, iv):
        cryptor = Encrypter.AES.new(key, Encrypter.AES.MODE_CBC, iv)
        count = len(text)
        if (count % 16 != 0):
            add = 16 - (count % 16)
        else:
            add = 0
        text = text + (b'\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    @staticmethod
    def decrypt(text, key, iv):
        cryptor = Encrypter.AES.new(key, Encrypter.AES.MODE_CBC, iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\0')

    @staticmethod
    def bin2bytes(bin)->bytes:
        return bytes.fromhex(hex(bin)[2:])

    @staticmethod
    def bytes2bin(bytes)->bin:
        return bin(int(bytes.hex(), 16))

    @staticmethod
    def locals()->str:
        """
        获取本地信息，包括用户名 操作系统类型 处理器类型 系统架构
        Get local information, includes: user name, operating system type, processor type, system architecture
        :return:
        """
        return str([platform.system(), platform.node(), platform.release(), platform.machine(), platform.processor()])

    def genkey(self, file_name:str, before_type='.object', type=".aes", local=False)->bytes:
        """
        生成AES加密用的key
        Generate keys for AES encryption
        :param file_name:   源文件的文件名 The file name of the source file
        :param before_type: 加密文件的源文件的后缀 The suffix of the source file of the encrypted file
        :param type:加密文件的后缀 Suffix of encrypted file
        :param local:   是否启用本地加密模式    Enable local encryption mode
        :return: bytes
        """
        raw = file_name + before_type + type + (self.locals() if local else "")
        # print("debug: raw: ", raw)
        key = self.hash32(raw.encode("utf-8"))
        return key

    def decrypt_file(self, header_path:str, crypt_info:EncryptInfo):
        """
        对指定的头文件进行解密，要求数据文件和头文件在同一目录下
        Decrypt the specified header file. The data file and header file are required to be in the same directory
        :param header_path:    Header文件的路径    file path of aes-header
        :param crypt_info:      头加密信息       header aes info
        :return: bytes
        """
        abs_path = os.path.abspath(header_path)
        dirname = os.path.dirname(abs_path)

        # hash内核检查
        assert crypt_info.ptype == self.pfh_info(), "pyfilehash kernel parameters are different and cannot be decrypted."
        # 本地简略信息检查
        locals = self.locals()
        if crypt_info.local:
            assert crypt_info.loc16 == self.hash16(locals.encode("utf-8")), "Local information does not match. Select 'add local information' (local = true) when encrypting. When the environment is changed or the local environment is changed, the previous file cannot be decrypted.\n\nLocal information includes: user name, operating system type, processor type, system architecture"

        # 进行解密
        key = self.genkey(crypt_info.fname, crypt_info.btype, crypt_info.ftype, crypt_info.local)
        iv = self.hash16(key)
        # print("debug: k-v:", key, iv)
        _bytes = open(os.path.join(dirname, crypt_info.fname + crypt_info.ftype), 'rb').read()
        plain = self.decrypt(_bytes, key, iv)

        return plain

    def encrypt_file(self, file_path:str, type=".aes", local=False)->EncryptInfo:
        """
        对指定的文件进行加密，要求最后将数据文件和头文件放在同一目录下
        Encrypt the specified file, and finally put the data file and header file in the same directory

        注意: Header信息并未自动写入
        Note: header information is not written automatically

        :param file_path:    文件路径    file path
        :param type:    加密后的数据文件的后缀     Suffix of encrypted data file
        :param local:     是否加入本地信息, 加入本地信息后不同计算机将无法对文件进行解密
                          Whether to add local information. After adding local information, different computers will not be able to decrypt the file
                          本地信息包括: 用户名 操作系统类型 处理器类型 系统架构
                          Local information includes: user name, operating system type, processor type, system architecture
        :return: EncryptInfo加密信息
        """
        assert os.path.exists(file_path), "File '{}' can not be found.".format(file_path)

        # 生成头信息
        abs_path = os.path.abspath(file_path)
        dirname = os.path.dirname(abs_path)
        basename = os.path.basename(abs_path)
        aes_fname, before_ftype = os.path.splitext(basename)    # 带.
        aes_ftype = type    # 带.
        if os.path.exists(os.path.join(dirname, aes_fname + aes_ftype)):  # 适应重复加密
            i = 0
            _aes_ftype = aes_ftype + str(i)
            while (os.path.exists(os.path.join(dirname, aes_fname + _aes_ftype))):
                i += 1
                _aes_ftype = aes_ftype + str(i)
            aes_ftype = _aes_ftype


        locals = self.locals()
        loc16 = self.hash16(locals.encode("utf-8")) if local else b"0" * 16
        pfh_info:str = self.pfh_info()
        crypt_info = EncryptInfo(aes_fname, before_ftype, aes_ftype, pfh_info, local, loc16)

        # 进行加密
        key = self.genkey(crypt_info.fname, crypt_info.btype, crypt_info.ftype, crypt_info.local)
        iv = self.hash16(key)
        # print("debug: k-v:", key, iv)
        _bytes = open(abs_path, 'rb').read()
        crypt = self.encrypt(_bytes, key, iv)

        # 输出数据
        crypt_data_path = os.path.join(dirname, aes_fname + aes_ftype)
        open(crypt_data_path, 'wb').write(crypt)

        return crypt_info

if __name__ == '__main__':
    tool = Encrypter()
    cf = tool.encrypt_file("test_raw.object", local=False)
    bin = tool.decrypt_file("test_raw.object", cf)
    open("test_decoded.object", 'wb').write(bin)

