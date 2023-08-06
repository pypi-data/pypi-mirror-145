import json
import os

def read_tsv_data(data_file_path,encoding = "utf-8"):
    """读取tsv 数据

    Args:
        data_file_path (_type_): 文件路径
        encoding (str, optional): 编码格式. Defaults to "utf-8".
    """    
    with open(data_file_path,"r",encoding = encoding) as f:
        data = []
        for line in f:
            data.append(line.strip().split("\t"))

def dict_list2jsonline_file(data,output_dir,saved_file_name):
    """把字典列表保存为jsonline 文件

    Args:
        data (_type_): 字典列表
        output_dir (_type_): 输出的文件夹
        saved_file_name (_type_): 保存的文件名
    """    
    with open(os.path.join(output_dir,saved_file_name),"w+",encoding="utf-8") as f:
        for example in data:
            f.write(json.dumps(example,ensure_ascii=False)+"\n")

def read_jsonline_file(file_path):
    """读取json line file 文件

    Args:
        file_path (_type_): _description_
    """
    with open(file_path,"r") as f:
        data = []
        for line in f:
            data.append(json.loads(line))
        return data


def train_dev_test_data2jsonline(data_dir,output_dir):
    file_name_list = ["dev","train","test"]
    for file_name in file_name_list:
        if os.path.exists(os.path.join(data_dir,file_name+".txt")):
            data = read_tsv_data(os.path.join(data_dir,file_name+".txt"))
            dict_list2jsonline_file(data,output_dir,file_name+".json")
        else:
            print("can not read ", os.path.join(data_dir,file_name+".txt"))
            