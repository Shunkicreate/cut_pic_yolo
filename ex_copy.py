import os
import shutil

dir_name = 'cat'


def copy(test=1, val=2, train=7):
    sum = test + val + train
    test /= sum
    val /= sum
    train /= sum
    dir_content = os.listdir(path=dir_name)

    jpg_files = [i for i in dir_content if i[-3:] == 'jpg']
    text_files = [i for i in dir_content if i[-3:]
                  == 'txt' and i != 'classes.txt']
    test = int(len(jpg_files)*test)
    val = int(len(jpg_files)*val)
    train = int(len(jpg_files) - test - val)
    if not(os.path.exists('{}/test'.format(dir_name))):
        os.makedirs('{}/test'.format(dir_name))
    if not(os.path.exists('{}/val'.format(dir_name))):
        os.makedirs('{}/val'.format(dir_name))
    if not(os.path.exists('{}/train'.format(dir_name))):
        os.makedirs('{}/train'.format(dir_name))
    for i in range(test):
        # txt_file = text_files[i]
        shutil.copy(dir_name+'/'+jpg_files[i], './cat/test')
        # shutil.copy(txt_file,'cat/test')
        print(i)
    for i in range(val):
        # txt_file = text_files[i]
        shutil.copy(dir_name+'/'+jpg_files[i], 'cat/val')
        # shutil.copy(txt_file,'cat/val')
        print(i)
    for i in range(train):
        # txt_file = text_files[i]
        shutil.copy(dir_name+'/'+jpg_files[i], 'cat/train')
        # shutil.copy(txt_file,'cat/val')
        print(i)

    return None


copy()
