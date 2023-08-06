import os
def check_dir(dirs):
    """判断文件夹是否存在，不存在的话就新建一个

    Args:
        dirs (_type_): 文件夹路径
    """    
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def check_file(filename):
    """判断文件是否存在，不存在的话就新建一个

    Args:
        filename (_type_): 文件路径
    """    
    if not os.path.exists(filename):
        os.system(r"touch {}".format(filename))#调用系统命令行来创建文件

from copy import deepcopy


def chunked_file_reader(fp, block_size=1024 * 8):
    """生成器函数：分块读取文件内容
    """
    while True:
        chunk = fp.read(block_size)
        # 当文件没有更多内容时，read 调用将会返回空字符串 ''
        yield chunk
def read_big_file(fname):
    with open(fname) as fp:
        for chunk in chunked_file_reader(fp):
            yield chunk
def read_big_file_line(fname):
    """按行读取大文件

    Args:
        fname (_type_): 文件路径

    Yields:
        _type_: 迭代器
    """    
    import copy
    last_line = ""
    for chunck in read_big_file(fname=fname):
        chunck = last_line + chunck
        if len(chunck) == 0:
            break
        # 每次读取8k会导致一行分属不同的chunck
        lines = chunck.split("\n")
        last_line = copy.deepcopy(lines[-1])
        for line in lines[:-1]:
            yield line