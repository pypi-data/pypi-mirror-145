import json
import spacy


DEMO = '''
{"logits": [0.0006508865626528859, 0.9992977380752563], "tokens": ["The", "proposed", "approach", "improves", "the", "performance", "by", "efficiently", "pruning", "the", "search", "space", "and", "extracting", "the", "complete", "set", "of", "coverage", "patterns", "."], "entities": [{"end": 3, "type": "Operation", "start": 2}, {"end": 6, "type": "Effect", "start": 5}], "relations": [{"head": 0, "tail": 1, "type": "Pos_Affect"}], "prediction": {"label": "Mechanism", "label_id": 1}}
'''

class OverlapEntityMerge:
    """
    spert 获取的实体存在重叠

    最有相同起始位置的实体进行处理

    对于起始位置相同的实体，选择结尾位置较大的实体，然后进行合并

    对于终止位置相同的实体，选择开始位置较小的实体，然后进行合并
    
    """    
    def __init__(self) -> None:
        self.filter_list = [
            "same_start",
            "same_end"
        ]
        pass
    def __same_postion_entity_merge(self,entity_span_list,filter):
        """具备相同的开始位置或者结束位置的实体进行合并

        Args:
            entity_span_list (_type_): 具备相同的开始位置或者结束位置的实体列表
            filter (_type_): "same_start"或者"same_end"

        Returns:
            _type_: _description_
        """        
        res_span = entity_span_list[0]
        if filter == "same_start":
            # 对于起始位置相同的实体，选择结尾位置较大的实体，然后进行合并
            for span in entity_span_list[1:]:
                if span["end"] > res_span["end"]:
                    new_class_label = span["type"]
                    res_span = span
                    res_span["type"] = new_class_label
        elif filter == "same_end":
            # 对于终止位置相同的实体，选择开始位置较小的实体，然后进行合并
            for span in entity_span_list[1:]:
                if span["start"] < res_span["start"]:
                    new_class_label = span["type"]
                    res_span = span
                    res_span["type"] = new_class_label
        else:
            pass
        for ent in entity_span_list:
            for k,v in self.entity_map.items():
                if v == ent["id"]:
                    self.entity_map[k] = res_span["id"]
            self.entity_map[ent["id"]] = res_span["id"]
            

        return res_span

    def __merge_same_postion_entity(self,entities,type = "same_start"):
        """找到一个实体列表中具有相同k开始或者结束位置的列表
        
        entity 需要有start ，end ， type, id 四个字段

        Args:
            entities (_type_): _description_
            type (str, optional): _description_. Defaults to "same_start"或者"same_end".
        """        
        same_postion_entity_map = {}

        for entity_span in entities:
            postion = entity_span["start"] if type == "same_start" else entity_span["end"]
            temp_list = same_postion_entity_map.get(postion,[])
            temp_list.append(entity_span)
            same_postion_entity_map[postion] = temp_list

        new_entities = []
        for _,same_start_span_list in same_postion_entity_map.items():
            if len(same_start_span_list) <= 1:
                new_entities.append(same_start_span_list[0])
            else:
                new_entities.append(
                    self.__same_postion_entity_merge(entity_span_list=same_start_span_list,filter=type))
        return new_entities
    def __call__(self, entities_list):
        """主函数

        entity 需要有start ，end ， type 三个字段


        Args:
            entities_list (_type_): 待处理的实体列表

        Returns:
            _type_: _description_
        """        
        self.entity_map = {}
        for en_idx,entity in enumerate(entities_list):
            entity["id"] = en_idx
            self.entity_map[en_idx] = en_idx
        for type in self.filter_list:
            entities_list = self.__merge_same_postion_entity(
                entities_list,type
            )
        
        return entities_list, self.entity_map



class RelationMerge:
    """
    
    重叠实体合并后，会存在关系的冗余

    因此需要对冗余的关系进行消除

    """    
    def __init__(self) -> None:
        pass
    
    def has_entity_overlap(self,entity_merge_map):
        """检查实体是否存在重叠的现象

        没有重叠时，每个实体都指向的是自己

        存在重叠时，会有实体志向和他具有相同开始或者终止位置，并且比自己更长的实体，此时entity_merge_map 中的k,v 存在不一致

        Args:
            entity_merge_map (_type_): _description_

        Returns:
            _type_: _description_
        """        
        flag = False
        overlap_entity = {}
        for ent_id, map_ent_id in entity_merge_map.items():
            if not ent_id == map_ent_id:
                overlap_entity[ent_id] = map_ent_id
                flag = True
        return flag,overlap_entity


    def __call__(self, reltions,entity_merge_map):
        flag,overlap_entity = self.has_entity_overlap(entity_merge_map)
        if not flag:
            return reltions
        rel_set = set()
        new_relations = []
        for relation in reltions:

            # 把关系的头尾实体替换为映射转换后的实体类型
            rel_head = overlap_entity.get(relation["head"],relation["head"])
            rel_tail = overlap_entity.get(relation["tail"],relation["tail"])

            rel_uid = "{}_{}".format(rel_head,rel_tail)
            if rel_uid not in rel_set:
                # 去除重复的关系
                new_relations.append(
                    {
                        "head":rel_head,
                        "tail":rel_tail,
                        "type":relation["type"]
                    }
                )
                rel_set.add(rel_uid)
        return new_relations


class EntRelFix:
    """
    基于spert 获得的实体存在重叠，需要将其进行去除

    """    
    def __init__(self) :
        self.demo = json.loads(DEMO)
        self.__ent_merger__ = OverlapEntityMerge()
        self.__rel_merger__ = RelationMerge()
        self.__entity_type2color__ = {
            "Effect":"#D94600",
            "Operation":"#6FB7B7"
        }

    def relation_entity_process(self,reltions,entities,tokens):
        entities_list, entity_map = self.__ent_merger__(entities)

        entity_id2idx = dict(zip([e["id"] for e in entities_list],list(range(len(entities_list)))))

        has_op_entity = any([True for e in entities_list if e["type"] == "Operation"])
        has_eff_entity = any([True for e in entities_list if e["type"] == "Effect"])
        if len(entities_list) > 1 and has_op_entity and has_eff_entity:

            for e_id ,e in enumerate(entities_list):
                e["id"] = e_id
                e["text"] = " ".join(tokens[
                    e["start"]:e["end"]
                ])

            new_rel = self.__rel_merger__(reltions,entity_map)
            new_rel_list = []
            for rel in new_rel:
                rel["head"] = entity_id2idx[rel["head"]]
                rel["tail"] = entity_id2idx[rel["tail"]]
                if entities_list[rel["head"]]["type"] == "Operation" and \
                    entities_list[rel["tail"]]["type"] == "Effect":
                    new_rel_list.append(rel)
            return entities_list,new_rel_list
        else:
            return [],[]
        
        
    