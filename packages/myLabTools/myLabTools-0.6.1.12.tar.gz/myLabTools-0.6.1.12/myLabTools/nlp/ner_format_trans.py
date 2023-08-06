import spacy
import json
from myLabTools.nlp.data_process import  dict_list2jsonline_file
from spacy.training import offsets_to_biluo_tags
import os



class NERFormatConv:
    """
    将以word offset 形式存储的书句转换为 biluo tags
    """    
    def __init__(self,tag2id_path,conv_tag2id = True):
        if conv_tag2id:
            self.tag2id = json.load(open(tag2id_path,"r"))
        self.conv_tag2id = conv_tag2id
        self.nlp = spacy.load("en_core_web_sm")

    def process_dataset_from_jsonline(self,data_path,saved_dir = "",saved_name = "",type = "dygie"):
        """命名实体识别书句处理主函数

        原始数据格式，有text，tokens，entities，relations，id等字段的dict

        {
        "text": "We improve the basic framework by Skip-chain CRFs and 2D CRFs to better accommodate the features of forums for better performance .", 
        "tokens": ["We", "improve", "the", "basic", "framework", "by", "Skip", "-", "chain", "CRFs", "and", "2D", "CRFs", "to", "better", "accommodate", "the", "features", "of", "forums", "for", "better", "performance", "."], 
        "entities": [{"type": "Operation", "start": 6, "end": 10, "text": "Skip-chain CRFs"}, {"type": "Effect", "start": 22, "end": 23, "text": "performance"}, {"type": "Operation", "start": 11, "end": 13, "text": "2D CRFs"}], 
        "relations": [{"type": "Pos_Affect", "head": 0, "tail": 1}, {"type": "Pos_Affect", "head": 2, "tail": 1}] }


        Args:
            data_path (_type_): 输入数据的路径
            saved_dir (_type_): 输入文件夹
            saved_name (_type_): 保存名字
            type (str, optional): 转换类型 dygie / biluo. Defaults to "dygie".
        """        

        # "id": "4c4a95645bb719cb53d668cca3b104e529746377_3"}
        data = [json.loads(line) for line in open(data_path,"r")]
        new_data = []
        for item in data:
            if type == "biluo":
                new_data.append(self.conv2biluo(item["tokens"],item["entities"],item["id"]))
            elif type == "dygie":
                new_data.append(self.conv2dygiepp(item["tokens"],item["entities"],item["relations"],item["id"]))
            else:
                exit
        if not len(saved_dir) == 0:
            dict_list2jsonline_file(new_data,saved_dir,saved_name)
        return new_data
    def process_data(self,data,saved_dir = "",saved_name = "",type = "dygie"):
        """命名实体识别书句处理主函数

        原始数据格式，有text，tokens，entities，relations，id等字段的dict

        {
        "text": "We improve the basic framework by Skip-chain CRFs and 2D CRFs to better accommodate the features of forums for better performance .", 
        "tokens": ["We", "improve", "the", "basic", "framework", "by", "Skip", "-", "chain", "CRFs", "and", "2D", "CRFs", "to", "better", "accommodate", "the", "features", "of", "forums", "for", "better", "performance", "."], 
        "entities": [{"type": "Operation", "start": 6, "end": 10, "text": "Skip-chain CRFs"}, {"type": "Effect", "start": 22, "end": 23, "text": "performance"}, {"type": "Operation", "start": 11, "end": 13, "text": "2D CRFs"}], 
        "relations": [{"type": "Pos_Affect", "head": 0, "tail": 1}, {"type": "Pos_Affect", "head": 2, "tail": 1}] ,
        "id": "4c4a95645bb719cb53d668cca3b104e529746377_3"}


        Args:
            data_path (_type_): 输入数据的路径
            saved_dir (_type_): 输入文件夹
            saved_name (_type_): 保存名字
            type (str, optional): 转换类型 dygie / biluo. Defaults to "dygie".
        """        

        new_data = []
        for i,item in enumerate(data):
            if "id" in item.keys():
                item_id = item["id"]
            else:
                item_id = i
            
            if type == "biluo":
                new_data.append(self.conv2biluo(item["tokens"],item["entities"],item_id))
            elif type == "dygie":
                new_data.append(self.conv2dygiepp(item["tokens"],item["entities"],item["relations"],item_id))
            else:
                exit
        if not len(saved_dir) == 0:
            dict_list2jsonline_file(new_data,saved_dir,saved_name)
        return new_data
    def conv2biluo(self,tokens,entities,id = ""):
        """Conoll 格式

        ['O', 'O', 'O', 'O', 'O', 'O', 'B-Operation', 'I-Operation', 'I-Operation', 'L-Operation', 'O', 'B-Operation', 'L-Operation', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'U-Effect', 'O']

        Args:
            tokens (_type_): _description_
            entities (_type_): _description_
            id (_type_): _description_

        Returns:
            _type_: _description_
        """        
        text = " ".join(tokens)
        pos_map = {
            -1:{"start":-1,"end":-1}
        }
        for i,token in enumerate(tokens) :
            pos_map[i] = {
                "start":pos_map[i-1]["end"]+1,
                "end":pos_map[i-1]["end"]+1+len(token)
            }
        ents = []
        new_entities = []
        for e in entities:
            ents.append({
                "start":pos_map[e["start"]]["start"],
                "end":pos_map[e["end"]-1]["end"],
                "label":e["type"]}
            )
            new_entities.append((pos_map[e["start"]]["start"], pos_map[e["end"]-1]["end"], e["type"]))

        doc = self.nlp(text)
        ner_tags = offsets_to_biluo_tags(doc, new_entities)
        assert len(ner_tags) == len(tokens)
        # print("BILUO before adding new entity:", ner_tags)
        #  ['O', 'O', 'O', 'O', 'O', 'O', 'B-Operation', 'I-Operation', 'I-Operation', 'L-Operation', 'O', 'B-Operation', 'L-Operation', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'U-Effect', 'O']

        return {
            "id":id,
            "ner_tags":[self.tag2id[t] for t in ner_tags] if self.conv_tag2id  else ner_tags,
            "tokens":tokens
        }
    def conv2dygiepp(self,tokens,entities,reltions ,id):
        # {"clusters": 
        # [[[6, 17], [32, 32]], [[4, 4], [55, 55], [91, 91]], [[58, 62], [64, 64], [79, 79]]], 
        # "sentences": [["This", "paper", "presents", "an", "algorithm", "for", "computing", "optical", "flow", ",", "shape", ",", "motion", ",", "lighting", ",", "and", "albedo", "from", "an", "image", "sequence", "of", "a", "rigidly-moving", "Lambertian", "object", "under", "distant", "illumination", "."], ["The", "problem", "is", "formulated", "in", "a", "manner", "that", "subsumes", "structure", "from", "motion", ",", "multi-view", "stereo", ",", "and", "photo-metric", "stereo", "as", "special", "cases", "."], ["The", "algorithm", "utilizes", "both", "spatial", "and", "temporal", "intensity", "variation", "as", "cues", ":", "the", "former", "constrains", "flow", "and", "the", "latter", "constrains", "surface", "orientation", ";", "combining", "both", "cues", "enables", "dense", "reconstruction", "of", "both", "textured", "and", "texture-less", "surfaces", "."], ["The", "algorithm", "works", "by", "iteratively", "estimating", "affine", "camera", "parameters", ",", "illumination", ",", "shape", ",", "and", "albedo", "in", "an", "alternating", "fashion", "."], ["Results", "are", "demonstrated", "on", "videos", "of", "hand-held", "objects", "moving", "in", "front", "of", "a", "fixed", "light", "and", "camera", "."]], 
        # "ner": [[[4, 4, "Generic"], [6, 17, "Task"], [20, 21, "Material"], [24, 26, "Material"], [28, 29, "OtherScientificTerm"]], [[32, 32, "Generic"], [42, 42, "Material"], [44, 45, "Material"], [48, 49, "Material"]], [[55, 55, "Generic"], [58, 62, "OtherScientificTerm"], [64, 64, "Generic"], [67, 67, "Generic"], [69, 69, "OtherScientificTerm"], [72, 72, "Generic"], [74, 75, "OtherScientificTerm"], [79, 79, "Generic"], [81, 88, "Task"]], [[91, 91, "Generic"], [95, 105, "Method"]], [[115, 118, "Material"]]], 
        # "relations": [[[4, 4, 6, 17, "USED-FOR"], [20, 21, 4, 4, "USED-FOR"], [24, 26, 20, 21, "FEATURE-OF"], [28, 29, 24, 26, "FEATURE-OF"]], [[42, 42, 44, 45, "CONJUNCTION"], [44, 45, 48, 49, "CONJUNCTION"]], [[58, 62, 55, 55, "USED-FOR"], [67, 67, 64, 64, "HYPONYM-OF"], [67, 67, 69, 69, "USED-FOR"], [67, 67, 72, 72, "CONJUNCTION"], [72, 72, 64, 64, "HYPONYM-OF"], [72, 72, 74, 75, "USED-FOR"], [79, 79, 81, 88, "USED-FOR"]], [[95, 105, 91, 91, "USED-FOR"]], []], 
        # "doc_key": "ICCV_2003_158_abs"}

        ent_list = [[e["start"],e["end"],e["type"]] for e in entities]
        rel_list = [[
            ent_list[rel["head"]][0], ent_list[rel["head"]][1],
            ent_list[rel["tail"]][0], ent_list[rel["tail"]][1],
            rel["type"]
        ] for rel in reltions]

        return {
            "clusters":[],
            "sentences":[tokens],
            "ner":ent_list,
            "relations":rel_list,
            "doc_key":id
        }