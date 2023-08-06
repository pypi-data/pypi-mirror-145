import os

def gen_flask_app_file(dir_path):
    """生成一个简单的flask 微服务后端框架

    Args:
        dir_path (str): 服务保存的路径
    """    
    if os.path.exists(dir_path):
        print("你输入的文件夹已经存在,请更换一个新的路径")
        exit()
    else:
        os.mkdir(dir_path)

    print("本应用依赖 flask 和 flask_cors \n安装命令： pip install flask flask_cors")
    app_file_txt = '''
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from util import PageResult, gen_url

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_AS_ASCII'] = False
app.add_template_filter(gen_url)

pages = PageResult(total=100000)

@app.route('/displayitems/<int:page_idx>',methods=["POST","GET"])
def displayitems(page_idx):
    if page_idx > 0 and page_idx < pages.total:
        item_list = pages.page_data[page_idx]

    return render_template('displayitems.html', listing =item_list,page_idx = page_idx)

@app.route('/vis/<string:paper_id>/<int:sent_id>',methods=["POST","GET"])
def vis_mech(paper_id,sent_id):
    html = ""
    return html

app.run(host="0.0.0.0", port=17215, threaded=True,debug=True)
        '''
    with open("{}/app.py".format(dir_path) , "w",encoding="utf-8") as f:
        f.write(app_file_txt)
    util_file_txt = """
class PageResult:
    def __init__(self, number = 20,total = 1000):
        from myLabTools.db.mysqldb import MysqlDB
        where_cond = "where XX > 0"
        self.db = MysqlDB(db_name = "db",host="127.0.0.1",port=3307,user="root",pwd="pwd")
        sql = ""
        self.data = list(self.db.select_all(sql))
        self.number = number
        self.total = total
        self.page = -1
        self.page_num = int(total/number)
        start_pos = list(range(0,self.total,self.number))

        self.page_data = [self.data[i:i+self.number] for i in start_pos]

    def get_next_page(self):
        self.page += 1
        if self.page == self.page_num:
            self.page = -1
            return 0
        
        return self.page


def gen_url(item):
    # 自定义的过滤器
    return "/vis/{}/{}".format(item[0],item[1])
    """
    with open("{}/util.py".format(dir_path) , "w",encoding="utf-8") as f:
        f.write(util_file_txt)
    os.mkdir("{}/templates".format(dir_path))
    temp_html = """
<center>
<ul>
    <p>当前为 第{{page_idx}} 页</p>
    {%for item in listing%}
    <a class="page-link" href="{{item | gen_url}}">

        <li>paper_id-{{item[0]}} , sent_id - {{item[1]}}</li>
    </a>
    
    {%endfor%}
</ul>

<ul class="pagination">
    {%if page_idx == 1%}
    <li class="page-item disabled"><a class="page-link" href="#">Previous</a></li>
    {%else%}
    <li class="page-item"><a class="page-link" href="/displayitems/{{page_idx-1}}">Previous</a></li>
    {%endif%}
    <li class="page-item"><a class="page-link" href="/displayitems/{{page_idx+1}}">Next</a></li>
</ul>
</center>
    """
    with open("{}/templates/displayitems.html".format(dir_path),"w",encoding="utf-8")  as f:
        f.write(temp_html)



# if __name__ == "__main__":
#     gen_flask_app_file("./app")