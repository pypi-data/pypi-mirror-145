import base64
import os


def img_to_base64(image_bytes):
    """

    :param image_bytes: 文件路径
    :return: base64字符串
    """
    with open(image_bytes, "rb") as fb:
        img = fb.read()
        base64_bytes = base64.b64encode(img)
        img_suffix = os.path.splitext(image_bytes)[1].replace('.', '')
        if img_suffix == 'jpg' or img_suffix == 'JPG' or img_suffix == 'jpeg' or img_suffix == 'JPEG':
            base64_str = 'data:image/jpeg;base64,' + base64_bytes.decode("utf-8")
        elif img_suffix == 'png' or img_suffix == 'PNG':
            base64_str = 'data:image/png;base64,' + base64_bytes.decode("utf-8")
        elif img_suffix == 'gif' or img_suffix == 'GIF':
            base64_str = 'data:image/gif;base64,' + base64_bytes.decode("utf-8")
        elif img_suffix == 'icon' or img_suffix == 'ICON':
            base64_str = 'data:image/x-icon;base64,' + base64_bytes.decode("utf-8")
        else:
            return '不支持此格式文件'
    return base64_str
