from operator import index
import pickle
import json
import string
from time import time
import logging
import re
from tqdm import tqdm
import re
from os.path import join as pjoin
import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
en_char = string.ascii_lowercase+string.ascii_uppercase + " -_."


def read_from_json(path):
    return json.load(open(path,"r"))


def write_to_json(data,path):
    json.dump(
        data,
        open(path,"w",encoding="utf-8"),
        indent=2,ensure_ascii=False
    )

def read_from_excel_to_dict(path,orient = "records"):
    """_summary_

    Args:
        path (_type_): 路径
        orient (str, optional): 返回的数据的格式. Defaults to "records".

        orient : str {'dict', 'list', 'series', 'split', 'records', 'index'}
                Determines the type of the values of the dictionary.

                - 'dict' (default) : dict like {column -> {index -> value}}
                - 'list' : dict like {column -> [values]}
                - 'series' : dict like {column -> Series(values)}
                - 'split' : dict like
                {'index' -> [index], 'columns' -> [columns], 'data' -> [values]}
                - 'records' : list like
                [{column -> value}, ... , {column -> value}]
                - 'index' : dict like {index -> {column -> value}}

                Abbreviations are allowed. `s` indicates `series` and `sp`
                indicates `split`.

    Returns:
        _type_: dict
    """    
    df = pd.read_excel(path)
    data = df.to_dict(orient=orient)
    return data

def read_excel(path):
    """读取excel 文件

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """    
    df = pd.read_excel(path)
    return df


def get_torch_cuda_pip_cmd():
    return '''
    pip install torch==1.7.1+cu110  -f https://download.pytorch.org/whl/torch_stable.html
    '''


class PickleTool:
    """pickle 文件处理类
    """    
    def load_pkl(self,data_path):
        """加载pickle文件

        Args:
            data_path (_type_): pickle文件的路径

        Returns:
            _type_: 数据
        """        
        data = pickle.load(open(data_path ,"rb"))
        return data
    
    def dump_pkl(self,data,save_path):
        """保存pickle文件

        Args:
            data (_type_): 数据
            save_path (_type_): 保存路径

        Returns:
            _type_: true
        """        
        pickle.dump(data,open(save_path,"wb"))
        return True

class JsonTool:
    """json文件处理工具类
    """    
    def load_json(self,data_path,encoding = "utf-8"):
        data = json.load(open(data_path,"r",encoding = encoding))
        return data
    
    
    def dump_json(self,data,save_path,encoding = "utf-8"):
        json.dump(data,open(save_path,"w+",encoding = encoding),ensure_ascii=False,indent=2)
        return True
    
    
    def dump_str(self,data):
        return json.dumps(data,ensure_ascii=False,indent=2)
    
    
    def load_str(self,data_str):
        return json.loads(data_str)
def is_all_eng(strs):
    """文本是否是全英文的

    Args:
        strs (_type_): 文本

    Returns:
        _type_: _description_
    """    
    '''
    print(is_all_eng('i love yiu '))
    print(is_all_eng('i love you'))
    print(is_all_eng('xx中国'))
    '''
    for i in strs:
        if i not in en_char:
            return False
    return True

def time_costing(func):
    """函数的运行的时间

    Args:
        func (_type_): _description_
    """    
    def core():
        start = time()
        func()
        print('time costing:', time() - start)
    return core

def find_refs(text):
    """查找知网xml论文数据中的参考文献

    Args:
        text (_type_): 文本

    Returns:
        _type_: 参考文献id列表
    """    
    citation_re_pattern = "REF#(.*?)#"
    citaions_id_list = re.findall(citation_re_pattern,text)
    return citaions_id_list



def cited_sents_extract(text):
    temp = re.findall("(“.*?”)", text)
    cited_sents  = []
    for sent in temp:
        if len(sent) >= 8 \
                or "，" in sent \
                or "。" in sent \
                or "？" in sent \
                or "！" in sent:
            cited_sents.append(sent)
    return cited_sents

def data_split(
    all_data, 
    test_size=0.2, 
    dev_size=0.2,
    saved_dir = "/data/code/python/ner/data/bieo/wiki"):
    """
    @description  : 将数据进行切分 训练集 60% ， 验证集 2）% ， 测试集 20%
                    保存在 saved_dir 中
    @param        :
    @Returns      :
    """
       
    from sklearn.model_selection import train_test_split
    data = {}
    data["train"], _temp, = train_test_split(
        all_data, test_size=test_size+dev_size, random_state=42)
    data["test"], data["dev"] = train_test_split(
        _temp, test_size=dev_size/(dev_size+test_size), random_state=42)
    for dataset_name,dataset in data.items():
        print(dataset_name)
        with open(pjoin(saved_dir , dataset_name + ".txt"),"w+",encoding = "utf-8") as f:
            for sample in dataset:
                for row in sample:
                    f.write("%s %s\n" % (row[0],row[1]))
                f.write("\n")


def gen_label_list(
    include_label_names_list, 
    saved_dir = "./",
    saved_name = "labels.txt",
    mode = "BIEO"):
    """
    @description  : 生成一个 ner 标签文件 label.txt
    @param        :
    @Returns      :
    """
    print(include_label_names_list)
    print("saved in :",pjoin(saved_dir,saved_name))
    print("*"*20)
    with open(pjoin(saved_dir,saved_name),"w+",encoding = "utf-8") as f:
        temp_labels = ["O"] + [prefix + "-" + label for prefix in list(mode[:-1]) for  label in include_label_names_list]
        for label in temp_labels:
            f.write("%s\n" % (label))
            print(label)
    print("*"*20)


def book_extract(text):
    """基于书名号识别书籍

    Args:
        text (_type_): 文本

    Returns:
        _type_: 书籍落标
    """    
    books = re.findall("《.*?》", text)
    return books

punctuation = "~!@#$%^&*()_+`{}|\[\]\:\";\-\\\='<>?,，。“”‘’·？！a-zA-Z\d《》./"
def char_filter(text):

    '''
    文本过滤
    :param text:
    :return:
    '''
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip()


import time
from tqdm import tqdm
import inspect
def get_now():
    """获取当前时间

    Returns:
        _type_: 文本，当前时间的字文本，年月日时分秒
    """    
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

def get_func_name():
    """获取正在运行的函数的名称

    Returns:
        _type_: _description_
    """    
    return "FUNCTION : "+inspect.stack()[1][3]




def split_dict(file_num = 10,dict_data = {}):
    """把一个大的字典拆分为file_num小字典

    Args:
        file_num (int, optional): 拆分的数目. Defaults to 10.
        dict_data (dict, optional): 带拆分的字典. Defaults to {}.

    Returns:
        _type_: 拆分后的字典
    """    
    return_data = {}
    for file_index in range(file_num):
        return_data[file_index] = {}
    i = 0
    for k,v in tqdm(dict_data.items(),desc="split_dict"):
        temp_file_index = i % file_num
        return_data[temp_file_index][k] = v
        i+= 1
    return return_data

def c_tqdm(data_iter,log_step = 100,total_iter = 100):
    """自定义的进度条

    Args:
        data_iter (_type_): 需要迭代处理的数据
        log_step (int, optional): 没多少不打印一次日志. Defaults to 100.
        total_iter (int, optional): 总的迭代步数. Defaults to 100.

    Yields:
        _type_: _description_
    """    
    total_iter = len(data_iter)
    for i,item in tqdm(enumerate(data_iter)):
        if i % log_step == 0:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            print("processing {} / {}  at {} ".format(i,total_iter,t))
        yield item