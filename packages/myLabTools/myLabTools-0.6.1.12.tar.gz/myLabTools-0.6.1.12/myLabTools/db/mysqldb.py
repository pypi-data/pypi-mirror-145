import pymysql

class MysqlDB:
    def __init__(self, db_name , host = "localhost" , port = 3306,user = "root",pwd = "root",charset="utf8mb4",batch_size = 100000):
        """mysql 数据库的实用类

        Args:
            db_name (_type_): 数据库名字
            host (str, optional): 数据库的ip. Defaults to "localhost".
            port (int, optional): 端口. Defaults to 3306.
            user (str, optional): 用户名. Defaults to "root".
            pwd (str, optional): 密码. Defaults to "root".
            charset (str, optional): 字符集. Defaults to "utf8mb4".
            batch_size (int, optional): 批次大小. Defaults to 100000.
        """        
        self.db = pymysql.connect(
            host = host,user = user,passwd = pwd, 
            db = db_name,port = port ,charset="utf8mb4")
        self.cursor = self.db.cursor()
        self.batch_size = batch_size
    def bulk_insert(self,data,sql_str,table_name):
        """批量插入数据

        Args:
            data (_type_): 待插入的数据
            sql_str (_type_): sql 命令
            table_name (_type_): 插入表的名字
        """        
        
        for i in range(0,len(data),self.batch_size):
            temp = data[i:i+self.batch_size]
            # import pdb; pdb.set_trace()

            self.cursor.executemany(sql_str,temp)
            print("insert {} {} records success".format(table_name,len(temp)))
            self.db.commit()
    def select_from_db(self,sql_str):
        """通过sql 查询获取表中的数据，使用于泛化的数据较小

        Args:
            sql_str (_type_): 查询语句

        Returns:
            _type_: 查询结果
        """        
        self.cursor.execute(sql_str)
        results = list(self.cursor.fetchall())
        return  results
        
    def select_all(self,sql_str):
        """通过sql 查询获取表中的数据，使用于泛化的数据较小

        Args:
            sql_str (_type_): 查询语句

        Returns:
            _type_: 查询结果
        """  
        self.cursor.execute(sql_str)
        for row in self.cursor.fetchall():
            yield row
    def select_all_batch(self,batch_size,total_num,sql_str):
        """获取表中的所有数据

        Args:
            batch_size (_type_): 批次的大小
            total_num (_type_): 表中总的数据的个数
            sql_str (_type_): 查询语句

        Yields:
            _type_: 按批次返回数据的迭代器
        """        
        for i in range(0,total_num,batch_size):
            self.cursor.execute(sql_str.format(str(int(i)), str(int(batch_size))))
            results = list(self.cursor.fetchall())
            yield results

    def select_all_batch_v2(self,table_name,batch_size = 1000,field_names_list = ['*'], where_condition = None):
        """对数据表中的指定字段的数据，按照batch_size 进行遍历，

        Args:
            table_name (_type_): 遍历的表的名字
            batch_size (int, optional): 批次大小. Defaults to 1000.
            field_names_list (list, optional): 字段列表. Defaults to ['*'].
            where_condition (_type_, optional): 查询条件. Defaults to None.

        Yields:
            _type_: 按批次返回数据的迭代器
        """        
        total_num = 0
        sql_str_1 = "select count(*) from {} ".format(table_name)
        if where_condition:
            sql_str_1 = sql_str_1 +  " where " + where_condition
        total_num = self.select_from_db(sql_str_1)
        total_num = total_num[0][0]
        print("%s total num is %d" % (sql_str_1,total_num))


        if field_names_list == ["*"]:
            sql_str_2 = "select * from {}".format(table_name)
        else:
            sql_str_2 = "select `{}` from {} ".format("`  , `".join(field_names_list),table_name)

        
        if where_condition:
            sql_str_2 = sql_str_2 + " where " + where_condition
        sql_str_2 = sql_str_2 + " limit {} , {}"

        for i in range(0,total_num,batch_size):
            self.cursor.execute(sql_str_2.format(str(int(i)), str(int(batch_size))))
            results = list(self.cursor.fetchall())
            yield results

    def get_table_all_fields(self,table_name):
        """获取一个表的所有字段

        Args:
            table_name (_type_): 表的名字

        Returns:
            _type_: 字段列表
        """        
        sql = "show full columns from {}".format(table_name)
        f = []
        for row in self.select_from_db(sql_str=sql):
            f.append(row[0])
        return f