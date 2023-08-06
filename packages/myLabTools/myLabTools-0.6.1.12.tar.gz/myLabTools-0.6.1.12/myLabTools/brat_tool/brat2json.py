from pybrat.parser import BratParser
import pybrat
import spacy
from tqdm import tqdm
from myLabTools.nlp.data_process import dict_list2jsonline_file

class  BRATAnnDataParser:
    """brat 标注结果的转换
    可以转换为json 格式，或者其他格式
    """    

    def __init__(self,
        data_dir_list = [],
        ent_type_map = {}
        ):
        self.data_dir_list = data_dir_list
        brat = BratParser(error="ignore")
        self.bart_ann_data = []
        self.nlp = spacy.load('en_core_web_sm')

        for data_dir in data_dir_list:
            temp = brat.parse(data_dir)
            for ex in temp:
                self.bart_ann_data.append(ex)
            print("parse {} finish ,{}".format(data_dir,len(self.bart_ann_data)))
        self.ent_type_map = ent_type_map
    

    def parse_item(self,example:pybrat.parser.Example):
        """
        Args:
            example (pybrat.parser.Example): _description_

        Returns:
            _type_: spacy.training.Example 
        """        
        doc = self.nlp.make_doc(example.text.split("\n")[0])
        temp = {
            }
        rel_list = []
        ent_list = []
        entity_pos2index = {}
        for ent_span in example.entities:
            ent_position = "{}_{}".format(ent_span.start,ent_span.end)
            ent_idx = len(entity_pos2index)
            entity_pos2index[ent_position] = ent_idx
            ent_list.append(
                {
                    "type":self.ent_type_map.get(ent_span.type,ent_span.type),
                    "start":ent_span.start,
                    "end":ent_span.end,
                    "text":ent_span.text
                }
            )


        for rel in example.relations:
            # print(rel)
            temp_rel = {
                    "type":rel.type,
                    "head":0,
                    "tail":0
                }
            for i,arg in enumerate([rel.arg1,rel.arg2]):
                ent_span = doc.char_span(arg.start,arg.end,alignment_mode = "expand")
                ent_position = "{}_{}".format(ent_span.start,ent_span.end)
                
                ent_postion_type = "head" if i == 0 else "tail"
                temp_rel[ent_postion_type] = entity_pos2index[ent_position]
            rel_list.append(temp_rel)
        
        temp["text"] = doc.text
        temp["tokens"] = [token.text for token in doc]
        temp["entities"] = ent_list
        temp["relations"] = rel_list
        temp["id"] = example.id
        # example_spacy = Example.from_dict(doc,temp)
        return temp
    def brat2json(self,target_dir = ""):
        data = []
        for brat_example in tqdm(self.bart_ann_data):
            json_format_data = self.parse_item(brat_example)
            data.append(json_format_data)
            
        return data

