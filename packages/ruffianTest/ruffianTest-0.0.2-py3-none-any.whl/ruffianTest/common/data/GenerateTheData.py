import random
import datetime
import time


def phone_num(them_roughly: str = '000'):
    if them_roughly == '000':
        them_roughly_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151",
                             "152", "153", "155", "156", "157", "158", "159", "186", "187", "188", "189", "172", "176",
                             "185"]
        phone = random.choice(them_roughly_list) + "".join(random.choice("0123456789") for completion in range(8))

    else:
        phone = str(them_roughly) + "".join(random.choice("0123456789") for completion in range(8))
    return phone


def id_card_num(address: str = '000000', birthday: str = '00000000'):
    end_num = "".join(random.choice("0123456789") for completion in range(4))
    start_time = datetime.datetime(1900, 1, 1).timestamp()
    end_time = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                 datetime.datetime.now().day).timestamp()
    if address == '000000':
        address = str(random.randint(110000, 900000))
        if birthday == '00000000':
            birthday = random.randint(start_time, end_time)
            birthday = time.localtime(birthday)
            birthday = str(time.strftime("%Y%m%d", birthday))
            result = address + birthday + str(end_num)
        else:
            result = address + birthday + end_num
    else:
        if birthday == '000000':
            birthday = random.randint(start_time, end_time)
            birthday = time.localtime(birthday)
            birthday = str(time.strftime("%Y%m%d", birthday))
            result = address + birthday + end_num
        else:
            result = address + birthday + end_num

    return result


def name_chinese(length: int = 2):
    result = ''
    for times in range(length):
        result = result + chr(random.randint(0x4e00, 0x9fbf))
    return result


__all__ = [
    'phone_num',
    'id_card_num',
    'name_chinese'
]
