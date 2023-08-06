import imp
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.util import paraphrase_mining
import pickle
from tqdm import tqdm


import torch
import numpy as np
from transformers import AutoTokenizer,BertPreTrainedModel
class TextEncoder:
    def __init__(self,
        config = {
            "model_checkpoint":"",
            "device":"cuda:0",
            "max_length":512
        },
        ModelClass:BertPreTrainedModel = BertPreTrainedModel
        ) -> None:
        """基于bert的文本编码器
        Args:
            config (dict, optional): bert模型的注册信息. Defaults to { "model_checkpoint":"", "device":"cuda:0", "max_length":512 }.
            ModelClass (BertPreTrainedModel, optional): bert模型的类. Defaults to BertPreTrainedModel.
        """        
        self.cuda_field = ['input_ids', 'token_type_ids', 'attention_mask']
        self.device = config["device"] 
        self.max_length = config["max_length"]
        self.config = config
        
        self.tokenizer = AutoTokenizer.from_pretrained(config["model_checkpoint"], use_fast=True)
        self.model = self.load_model(ModelClass,config["model_checkpoint"])

        self.model.to(config["device"])
        
    

    def load_model(self,ModelClass:BertPreTrainedModel,model_checkpoint):
        """加载模型

        Args:
            ModelClass (BertPreTrainedModel): _description_
            model_checkpoint (_type_): _description_

        Returns:
            _type_: _description_
        """        
        model = ModelClass.from_pretrained(
            model_checkpoint
            )
        return model

    # 将文本转换为tokenid 
    def process_text(self,text):
        """处理文本

        Args:
            text (_type_): 文本

        Returns:
            _type_: 分词，转换后的token
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
    def __call__(self,text):
        """主函数，获取文本的词向量

        Args:
            text (_type_): 文本

        Returns:
            _type_: 词向量
        """        
        inputs = self.process_text(text)
        with torch.no_grad() :
            outputs = self.model(inputs["input_ids"],attention_mask = inputs["attention_mask"])
        
        if "cuda" in self.device:
            # 获得CLS 对应的向量
            text_vect = outputs.last_hidden_state.cpu().numpy()[0][0]
            # if self.config["has_text_vector"] 
        else:
            text_vect = outputs.last_hidden_state.numpy()[0][0]

        return text_vect