import pymongo
import bson
import json

class MongoDB:
    """mongodb 数据库数据访问接口
    """    
    def __init__(self,host = "127.0.0.1",port = 27017,
                                db_name = "cnki",
                                username = "",pwd = "",
                                batch_size = 10000):
        """MongoDB

        Args:
            host (str, optional): 数据库的ip. Defaults to "127.0.0.1".
            port (int, optional): 数据库的端口. Defaults to 27017.
            db_name (str, optional): 数据库的名字. Defaults to "cnki".
            username (str, optional): 用户名. Defaults to "".
            pwd (str, optional): 密码. Defaults to "".
            batch_size (int, optional): 查询，保存的批次大小. Defaults to 10000.
        """        
        self.client = pymongo.MongoClient(host=host, port=port)
        if len(username) > 0:
            admin = self.client["admin"]
            admin.authenticate(username, pwd)

        self.db = self.client[db_name]
        self.batch_size = batch_size
        self.db_name = db_name
        print("MongoDB : connect to {} success !!".format(host))

    def get_records_num(self,table_name,query = "all"):
        """获取一个表中的数据的总数，或者一个查询的结果数

        Args:
            table_name (_type_): 查询的表的名字
            query (str, optional): 查询语句. Defaults to "all".

        Returns:
            _type_: 表中的记录数
        """        
        table = self.get_table(table_name=table_name)
        if query == "all":
            return table.find().count()
        else:
            return table.find(query).count()
        
  
    def search_table(self,table_name,query = "all",batch_size = None):
        """查询表

        Args:
            table_name (_type_): 表名字
            query (str, optional): 查询. Defaults to "all".
            batch_size (_type_, optional): 批次大小. Defaults to None.

        Yields:
            _type_: 迭代器
        """        
        records_num = self.get_records_num(table_name,query)
        print("select {} from {} result num is {}".format(str(query),table_name,str(records_num)))

        table = self.get_table(table_name=table_name)
        if batch_size is None:
            batch_size = self.batch_size
        
        for page_i in range((records_num // batch_size ) + 1):
            print("selet page {}".format(page_i))
            skip = page_i * batch_size
            if query =="all":
                yield table.find().limit(batch_size).skip(skip=skip)
            else:
                yield table.find(query).limit(batch_size).skip(skip=skip)
    def find_batch(self,table_name,query = None):

        table = self.get_table(table_name=table_name)
        if query is None:
            for batch_data in table.find_raw_batches():
                data = bson.decode_all(batch_data)
                yield data
        else:
            for batch_data in table.find_raw_batches(query):
                data = bson.decode_all(batch_data)
                yield data

    def get_table(self,table_name):
        """获取数据库中的某一个表

        Args:
            table_name (_type_): 获取的标的名字

        Returns:
            _type_: 表对象
        """        
        table = self.db[table_name]
        return table
    
    def query(self,table_name,query = {},field_names_list = ['*']):
        """查询某一个表

        Args:
            table_name (_type_): 带查询的表的名字
            query (dict, optional): 查询语句. Defaults to {}.
            field_names_list (list, optional): 查询的字段列表. Defaults to ['*'].

        Returns:
            _type_: _description_
        """        
        table = self.get_table(table_name=table_name)
        fields = {}
        for f in field_names_list:
            fields[f] = 1
        fields["_id"] = 0
        return table.find(query,fields)

    def bulk_insert(self,data,table_name):
        """向表中插入数据

        Args:
            data (_type_): 插入的数据
            table_name (_type_): 插入的标的名字
        """        
        table = self.get_table(table_name=table_name)
        if len(data) > 0:
            for i in range(0, len(data), self.batch_size):
                temp = data[i:i + self.batch_size]
                table.insert_many(temp)
                print("MongoDb : insert {} to {}-{} success".format(len(temp),self.db_name,table_name))
        else:
            print("MongoDb : empty data!!")
    def select_all_batch_v2(self,table_name,field_names_list = ['*'], query = {}):
        """按照一定的批次大小迭代的获取表中的所有数据

        Args:
            table_name (_type_): 表的名字
            field_names_list (list, optional): 查询的字段列表. Defaults to ['*'].
            query (dict, optional): 查询语句. Defaults to {}.

        Yields:
            _type_: 迭代器
        """        
        '''
        对数据表中的数据按照batch_size 进行遍历
        '''
        fields = {}
        for f in field_names_list:
            fields[f] = 1
        fields["_id"] = 0

        table = self.db[table_name]
        for batch_data in table.find_raw_batches(query,fields):
            data = bson.decode_all(batch_data)
            yield data
    def select_all_batch_v3(self,table_name, query = {}):
        """按照一定的批次大小迭代的获取表中的所有数据

        Args:
            table_name (_type_): 表的名字
            query (dict, optional): 查询语句. Defaults to {}.

        Yields:
            _type_: 迭代器
        """        
        table = self.db[table_name]
        for batch_data in table.find_raw_batches(query):
            data = bson.decode_all(batch_data)
            yield data
    
    def select_iter(self,table_name,field_names_list = ['*'], query = {}):
        '''
        对数据表中的数据按照batch_size 进行遍历
        '''
        fields = {}
        for f in field_names_list:
            fields[f] = 1
        fields["_id"] = 0

        table = self.db[table_name]
        for row in table.find(query,fields):
            temp_row = []
            for f in field_names_list:
                temp_row.append(row[f])
            yield temp_row
    def get_sample_data(self,table_name,first_k = 5,
        output_file = False
        ):
        """获取表的前k个数据

        Args:
            table_name (_type_): 表的名字
            first_k (int, optional): 前k个数据的数目. Defaults to 5.
            output_file (bool, optional): 是否以文件的形式进行输出，
                        输出的文件名为table_name + "-demo-first-" + str(first_k) + ".json". Defaults to False.

        Returns:
            _type_: _description_
        """        
        table = self.db[table_name]
        return_data = []
        fields = []
        for batch_data in table.find_raw_batches({}):
            data = bson.decode_all(batch_data)
            for row in data[:3]:
                del row["_id"]
                fields = list(row.keys())
                return_data.append(row)
            break
        if output_file:
            json.dump(
                return_data,
                open("./"+table_name + "-demo-first-" + str(first_k) + ".json",
                "w+",
                encoding="utf-8"),
                indent=4,
                ensure_ascii=False
                )
        return fields

if __name__ == "__main__":
    cnki_data_db = MongoDB(db_name="cnki")
