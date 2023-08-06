from myLabTools.db.mongodb import  MongoDB
from tqdm import tqdm

class MultiProcess:
    def __init__(self,db_config_params = {
                    "host":'localhost',
                    "port":27017,
                    "db_name":"cnki"
                },
        input_table_name  = "data",
        output_table_name = "data_v2"
    ):
        """以多进程的的范式处理数据库中的数据

        Args:
            db_config_params (dict, optional): mongo的基本参数. Defaults to { "host":'localhost', "port":27017, "db_name":"cnki" }.
            input_table_name (str, optional): 待处理的数据所在的表. Defaults to "data".
            output_table_name (str, optional): 处理结果保存的表. Defaults to "data_v2".
        """        
        self.db = MongoDB(**db_config_params)
        self.input_table_name = input_table_name
        self.output_table_name = output_table_name
    def process_row_data(self,row):
        return row

    def process_v1(
        self,
        total_process,
        this_process
        ):
        """多进程处理

        Args:
            total_process (_type_): 总的进程数
            this_process (_type_): 当前进程
        """        
        print("total process",total_process,"this process",this_process)
        for batch_data in tqdm(
            self.db.select_all_batch_v3(
                table_name=self.input_table_name)
                ):
            data = []
            i = 0
            for row in batch_data:
                try:
                    if i % total_process == this_process:
                        new_row = self.process_row_data(row)
                        data.append(new_row)
                    i = i+1
                except :
                    i = i+1
                    continue
            self.db.bulk_insert(data=data,table_name=self.output_table_name)
    def process_v2(
        self,
        total_process,
        this_process,
        row_process_func = lambda row : row
        ):
        """多进程处理 v2


        Args:
            total_process (_type_): 总的进程数据
            this_process (_type_): 当前进程
            row_process_func (_type_, optional): 每一个数据的处理函数. Defaults to lambdarow:row.
        """        
        print("total process",total_process,"this process",this_process)
        for batch_data in tqdm(
            self.db.select_all_batch_v3(
                table_name=self.input_table_name)
                ):
            data = []
            i = 0

            for row in batch_data:
                try:
                    if i % total_process == this_process:
                        new_row = row_process_func(row)
                        data.append(new_row)
                    i = i+1
                except :
                    i = i+1
                    continue
                
            self.db.bulk_insert(data=data,table_name=self.output_table_name)
    
def mp_main():
    mp = MultiProcess()
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--total_process", help="total process num", type=int)
    parser.add_argument("--this_process", help="this process num", type=int)
    args = parser.parse_args()
    mp.process_v1(args.total_process,args.this_process)
