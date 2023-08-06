from allennlp.predictors.predictor import  Predictor
import pickle
from tqdm import  tqdm




class CorefAllenAI:
    """
    基于AllenAi 的共指消解

    使用的虚拟环境为allennlp, 需要下载模型 https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz

    https://demo.allennlp.org/coreference-resolution

    conda create -n allennlp python=3.7

    conda activate allennlp

    pip install allennlp==2.1.0 allennlp-models==2.1.0

    """    
    def __init__(self,model_path="./model/coref/coref-spanbert-large-2021.03.10.tar.gz",cuda_device = 4):
        self.predictor = Predictor.from_path(model_path,cuda_device = 4)
    

    def _coref(self,text):
        """

        What we get as a result (`prediction`) is a dictionary as Allen outputs multiple different information at once.   
        The ones that we found to be using the most are:

        |  Key                |  Type              |  Description
        |:--------------------------|:-------------------|:----------------------------------------------------
        | `top_spans`     | `List[List[int]]` | List of `spaCy` token indices pairs representing spans
        | `document` | `List[str]` | Document's tokens (from `spaCy`; but represented as string not Token)
        | `clusters` | `List[List[List[int]]]` | Clusters of spans (represented by token indices pairs)


        Args:
            text (_type_): _description_
        """        
        res = self.predictor.predict(
            document=text
        )
        coref_resolved_text = self.predictor.coref_resolved(text)
        return res,coref_resolved_text
    def process_paper(self,paper):
        abs_text = paper["Abstract"]
        coref_res,coref_resolved_text = self._coref(abs_text)

        tokens = coref_res["document"]

        clusters = [
                    [{"start":s,"end":e+1,"text":tokens[s:e+1]}for s,e in cluster]
                     for cluster in coref_res["clusters"]
            ]
        return {
            "coref_resolved_text":coref_resolved_text,
            "clusters":clusters
        }