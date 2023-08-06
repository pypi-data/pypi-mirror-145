from tkinter.messagebox import NO
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer,BertPreTrainedModel
from datasets import load_dataset, load_metric
import numpy as np
from transformers import AutoTokenizer
from .utils import TextClassificationConfigBase
import os
import numpy as np


TC_Config = TextClassificationConfigBase()


class TC_Trainer():
    """文本分类模型训练器
    """    
    def __init__(self,config_path):
        
        if os.path.exists(config_path):
            self.config = TC_Config.load_from_config_file(config_path)
            self.train_args = self.config["train_args"]
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config["model_checkpoint"], 
                use_fast=True
                )
            self.print_dev_info = self.config.get("print_dev_info",False)
        else:
            print("can not read ", config_path)
            exit()
        

    def _load_metric(self,config_name = "mnli"):
        """加载评测指标

        Args:
            config_name (str, optional): _description_. Defaults to "mnli".

        Returns:
            _type_: _description_
        """        
        metric = load_metric('glue', config_name)
        return metric

    def _load_dataset(self):
        """加载数据集

        Returns:
            _type_: _description_
        """        
        return load_dataset("json", data_files=self.config["json_files"])

    def _process_data(self):
        """处理数据
        """        
        def preprocess_function(examples):
            if len(self.config["sentence2_key"]) == 0:
                return self.tokenizer(
                    examples[self.config["sentence1_key"]],
                    truncation =True,
                    max_length = self.config["max_length"]
                    )
            return self.tokenizer(
                examples[self.config["sentence1_key"]],
                examples[self.config["sentence2_key"]], 
                truncation=True,
                max_length = self.config["max_length"]
                )
        dataset = self._load_dataset()

        encoded_dataset = dataset.map(preprocess_function, batched=True)
        return encoded_dataset
    def train(
        self,
        ClfModelClass:BertPreTrainedModel,
        kwargs = {
            "compute_metrics":None,
            "callbacks":[]
        }
        ):
        """训练主函数

        Args:
            ClfModelClass (BertPreTrainedModel): _description_
            kwargs (dict, optional): _description_. Defaults to { "compute_metrics":None, "callbacks":[] }.
        """        
        encoded_dataset = self._process_data()

        model = ClfModelClass.from_pretrained(
            self.config["model_checkpoint"], 
            num_labels=self.config["num_labels"])
        args = TrainingArguments(
            **self.train_args
        )

        trainer = Trainer(
            model,
            args,
            train_dataset=encoded_dataset["train"],
            eval_dataset = encoded_dataset["valid"],
            # test_dataset = encoded_dataset["test"],
            tokenizer=self.tokenizer,
            **kwargs

        )

        trainer.train()
        trainer.save_model()
        trainer.evaluate()
def gen_config_file(config_path):
    """生成一个文本分类的注册文件模板

    Args:
        config_path (_type_): 模板的保存位置
    """    
    TC_Config.gen_config_template(config_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_path", help="text classification config path", type=str)
    args = parser.parse_args()
    tctrainer = TC_Trainer(args.config_path)


