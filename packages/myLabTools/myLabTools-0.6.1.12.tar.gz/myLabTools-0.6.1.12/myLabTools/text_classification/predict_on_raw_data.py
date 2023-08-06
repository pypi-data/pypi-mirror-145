from transformers import AutoTokenizer
import json
from tqdm import tqdm
from sklearn.metrics import classification_report
from .bert_text_classify_pipeline import TextClassificationPipeline
from .bert_model import BertCNNForSequenceClassification
import copy

"""文本分类模型预测器
"""

class PredictBase():
    """文本分类预测器的 base类
    """    
    def __init__(self,model_checkpoint,device = 0):
        model,tokenizer = self.load_checkpoint(model_checkpoint)

        self.tc_pipline = TextClassificationPipeline(
            model = model,
            tokenizer = tokenizer,
            device = device,
            return_all_scores = True
            )
    def load_checkpoint(self,model_checkpoint):
        """加载模型和分词器

        Args:
            model_checkpoint (_type_): checkpoint的路径

        Returns:
            _type_: 模型，分词器
        """        
        model = BertCNNForSequenceClassification.from_pretrained( 
            model_checkpoint
            )
        tokenizer = AutoTokenizer.from_pretrained(
            model_checkpoint, 
            use_fast=True
            )
        return model,tokenizer
    def pred_jsonline_file(self,
        data_path = "./json_data/task_1/v1/test.json",
        text_field = "text",
        write_to_json = True,
        output_json_path = "./prediction.json"
        ):
        """预测jsonline 文件中的数据

        Args:
            data_path (str, optional): jsonline文件的路径. Defaults to "./json_data/task_1/v1/test.json".
            text_field (str, optional): 样例中文本的字段. Defaults to "text".
            write_to_json (bool, optional): 是否保存结果. Defaults to True.
            output_json_path (str, optional): 保存结果的路径. Defaults to "./prediction.json".

        Returns:
            _type_: _description_
        """        
        res = []
        with open(data_path,"r",encoding="utf-8") as f:
            for line in tqdm(f):
                data = json.loads(line)
                temp = copy.deepcopy(data)
                text = temp[text_field]
                tc_pred_res = self.tc_pipline(text)
                temp["prediction"] = tc_pred_res
                res.append(temp)
        if write_to_json:
            json.dump(res,open(output_json_path,"w+",encoding = "utf-8"),indent=4,ensure_ascii=False)
        return res
    def model_report(self,
        y_true, 
        y_pred,
        digits = 4,
        print_classification_report = True,
        return_classification_report_dict  =True
        ):
        """计算模型预测结果的分类评测指标

        Args:
            y_true (_type_): 真实标签列表
            y_pred (_type_): 预测标签列表
            digits (int, optional): 输出指标的小数点位数. Defaults to 4.
            print_classification_report (bool, optional): 是否打印评测指标. Defaults to True.
            return_classification_report_dict (bool, optional): 是否以字典的形式返回评测指标. Defaults to True.

        Returns:
            _type_: _description_
        """        
        if print_classification_report:
            print(classification_report(
                y_true, 
                y_pred,
                digits = digits)
            )
        if return_classification_report_dict:
            return classification_report(
                y_true, 
                y_pred,
                digits = digits,
                output_dict = True
                )
        else:
            return None

from transformers import AutoTokenizer,BertPreTrainedModel
import torch
import json
import numpy as np

class PredictorForPairTextClf():
    """对文本对进行分类
    """    
    def __init__(self,
        predictor_config = {
            "model_checkpoint":"",
            "device":"cuda:0",
            "max_length":512
        },
        id2label = {
                    0:"entailment",
                    1:"contradiction",
                    2:"neutral"
                },
        ClfModelClass:BertPreTrainedModel = None
        ) -> None:
        """对文本对进行分类

        Args:
            predictor_config (dict, optional): 分类模型的基本参数. Defaults to { "model_checkpoint":"", "device":"cuda:0", "max_length":512 }.
            id2label (dict, optional): id2class的映射. Defaults to { 0:"entailment", 1:"contradiction", 2:"neutral" }.
            ClfModelClass (BertPreTrainedModel, optional): 分类模型定义. Defaults to None.
        """        
        self.cuda_field = ['input_ids', 'token_type_ids', 'attention_mask']
        self.device = predictor_config["device"] 
        self.config = predictor_config

        self.max_length = predictor_config["max_length"]
        self.id2label = id2label

        self.tokenizer = AutoTokenizer.from_pretrained(predictor_config["model_checkpoint"], use_fast=True)

        self.model = self.load_model(ClfModelClass,predictor_config["model_checkpoint"])

        self.model.to(predictor_config["device"])
        
    

    def load_model(self,ClfModelClass:BertPreTrainedModel,model_checkpoint):
        model = ClfModelClass.from_pretrained(
            model_checkpoint, 
            num_labels=len(self.id2label))
        return model

    # 将文本转换为tokenid 
    def process_pair_text(self,sent_1,sent_2):
        encoded_data = self.tokenizer(
            sent_1,sent_2, 
            padding="max_length", 
            max_length=self.max_length,
            truncation=True,
            return_tensors = "pt"
            )
        encoded_data["labels"] = None
        for field in self.cuda_field:
            encoded_data[field] = encoded_data[field].to(self.device)
        return encoded_data
    
    def predict(self,sent_1,sent_2):
        """对文本对进行分类主函数

        Args:
            sent_1 (_type_): 文本1
            sent_2 (_type_): 文本2

        Returns:
            _type_: 字典{
                logits：
                prediction：
                    {
                        label_id：
                        label：
                    }
            }
        """        
        inputs = self.process_pair_text(sent_1,sent_2)
        with torch.no_grad() :
            outputs = self.model(**inputs)
        
        if "cuda" in self.device:
            logits = outputs["logits"].cpu().numpy()[0]
            # if self.config["has_text_vector"] 
        else:
            logits = outputs["logits"].numpy()[0]

        prediction = np.argmax(logits)
        result = {
            "logits":dict(zip(self.id2label.values(), logits.tolist())), # 各个标签对应的概率
            "prediction":{"label_id":int(prediction) ,"label":self.id2label[int(prediction)]}# 预测的结果
        }
        return result



class PredictorForSingleTextClf():
    """对单个文本进行分类
    """    
    def __init__(self,
        predictor_config = {
            "model_checkpoint":"",
            "device":"cuda:0",
            "max_length":512
        },
        id2label = {
                    0:"pos",
                    1:"neg"
                },
        ClfModelClass:BertPreTrainedModel = None
        ) -> None:
        """对单个文本进行分类

            Args:
            predictor_config (dict, optional): 分类模型的基本参数. Defaults to { "model_checkpoint":"", "device":"cuda:0", "max_length":512 }.
            id2label (dict, optional): id2class的映射. Defaults to { 0:"entailment", 1:"contradiction", 2:"neutral" }.
            ClfModelClass (BertPreTrainedModel, optional): 分类模型定义. Defaults to None.

       """        
        self.cuda_field = ['input_ids', 'token_type_ids', 'attention_mask']
        self.device = predictor_config["device"] 
        self.max_length = predictor_config["max_length"]
        self.config = predictor_config
        self.id2label = id2label
        
        self.tokenizer = AutoTokenizer.from_pretrained(predictor_config["model_checkpoint"], use_fast=True)
        self.model = self.load_model(ClfModelClass,predictor_config["model_checkpoint"])

        self.model.to(predictor_config["device"])
        
    

    def load_model(self,ClfModelClass:BertPreTrainedModel,model_checkpoint):
        """加载模型

        Args:
            ClfModelClass (BertPreTrainedModel): _description_
            model_checkpoint (_type_): _description_

        Returns:
            _type_: _description_
        """        
        model = ClfModelClass.from_pretrained(
            model_checkpoint, 
            num_labels=len(self.id2label))
        return model

    def process_text(self,text):
        """将文本转换为tokenid

        Args:
            text (_type_): 文本

        Returns:
            _type_: encoded_data
        """        
        encoded_data = self.tokenizer(
            [text],
            padding="max_length", 
            max_length=self.max_length,
            truncation=True,
            return_tensors = "pt")
        
        encoded_data["labels"] = None
        for field in self.cuda_field:
            encoded_data[field] = encoded_data[field].to(self.device)
        return encoded_data
    
    # 文本分类 传入一个文本
    def predict(self,text):
        """对单个文本进行分类

        Args:
            text (_type_): 文本

        Returns:
            _type_: 分类结果
            字典{
                logits：
                prediction：
                    {
                        label_id：
                        label：
                    }
            }
        """        
        inputs = self.process_text(text)
        with torch.no_grad() :
            outputs = self.model(**inputs)
        
        if "cuda" in self.device:
            logits = outputs["logits"].cpu().numpy()[0]
            # if self.config["has_text_vector"] 
        else:
            logits = outputs["logits"].numpy()[0]

        prediction = np.argmax(logits)
        result = {
            "logits":logits.tolist(), # 各个标签对应的概率
            "prediction":{"label_id":int(prediction) ,"label":self.id2label[int(prediction)]} # 预测的结果
        }
        return result