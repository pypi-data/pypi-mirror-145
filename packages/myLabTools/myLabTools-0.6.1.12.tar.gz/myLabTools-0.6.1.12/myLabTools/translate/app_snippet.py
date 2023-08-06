import os
from flask import Flask, request, jsonify
from .translator import Translator

"""
基于huggingface 的MarianMTModel 构建了一个机器翻译微服务框架
"""


app = Flask(__name__)
translator = Translator(os.environ.get("SOURCE_LANG"), os.environ.get("TARGET_LANG"), os.environ.get("MODEL_PATH"))

app.config["DEBUG"] = True # turn off in prod

@app.route('/', methods=["GET"])
def health_check():
    """检查服务是否运行

    """    
    return "Machine translation service is up and running."

@app.route('/lang_routes', methods = ["GET"])
def get_lang_route():

    lang = request.args['lang']
    all_langs = translator.get_supported_langs()
    lang_routes = [l for l in all_langs if l[0] == lang]
    return jsonify({"routes":lang_routes})

@app.route('/supported_languages', methods=["GET"])
def get_supported_languages():
    """获取支持的翻译类型
    """    
    langs = translator.get_supported_langs()
    return jsonify({"languages":langs})

@app.route('/translate', methods=["POST"])
def get_prediction():
    """机器翻译服务

    Returns:
        _type_: _description_
    """    
    text = request.json['text']
    translation = translator.translate(text)
    return jsonify({"translation":translation})

app.run(host="0.0.0.0")