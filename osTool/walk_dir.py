import os
path = os.getcwd()

def text_create(desktop_path, name, msg):
    full_path = desktop_path + name + '.txt'
    file = open(full_path, 'w')
    file.write(msg)
    file.close()

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        # print(files) #当前路径下所有非目录子文件

    text_create('E:\projects\\test_plane\\test\Productions\Production_1 (2)\Data','1',','.join(dirs))
file_name(path)