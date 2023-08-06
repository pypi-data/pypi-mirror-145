import base64
import hashlib
import hmac

"""
@description: 加密方法
"""


class Encryption:
    def __init__(self, not_encrypted_str, mode, key=''):
        """

        :param not_encrypted_str: 未加密字符串
        :param mode: 加密方式 md5、sha256...
        :param key: 盐 可选
        """
        self.mode = mode  # Es = Encrypted string
        self.key = key
        self.NES = not_encrypted_str

    def encryption(self):
        if self.key == '':
            encrypted_string = hashlib.new(self.mode, bytes(self.NES, encoding='utf-8')).hexdigest()
            return encrypted_string

        else:
            encrypted_string = hmac.new(
                bytes(self.key, encoding='utf-8'), bytes(self.NES, encoding='utf-8'), self.mode
            )
            return encrypted_string.hexdigest()

        """
        Example 1

        esd = Encryption('123456', 'md5', 'key').encryption()
        print(esd)

        Example 2
        esd = Encryption('123456', 'md5').encryption()
        """


def to_base64(item):
    """

    :param item: str
    :return: str.base64
    """
    return str(base64.b64encode(item.encode('utf-8')), "utf-8")
