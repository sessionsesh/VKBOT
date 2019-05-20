import pickle
import os


def dout(d, folder):  # запись в файл
    with open(folder, 'wb') as out:
        pickle.dump(d, out)


def din(folder):  # чтение из файла
    with open(folder, 'rb') as inp:
        d = pickle.load(inp)
    return d


def user_checker(user_id, folder):
    if os.stat(folder).st_size == 0:
        return False
    if user_id in din(folder).keys():
        return True
    else:
        return False


def get_group(user_id, folder):
    with open(folder, 'rb') as inp:
        d = pickle.load(inp)
    for each in d.keys():
        if str(user_id).lower() == each.lower():
            res = d[each]
    return res
print(user_checker(str(482658803), 'D:\\Code\\Python\\VKBOT\\folder.txt'))
