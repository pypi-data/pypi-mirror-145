import numpy as np
from lime.lime_text import LimeTextExplainer
from myLabTools.text_classification.predict_on_raw_data import PredictorForSingleTextClf
from tqdm import  tqdm


sent_clf = None

def lime_predictor(texts):
    global sent_clf
    prob_list = []
    for t in tqdm(texts):
        out = sent_clf.predict(t)
        logits = out["logits"]
        prob_list.append(logits)
        # probas = F.softmax(logits).numpy()
    
    return np.stack(prob_list)

class LIME:

    def __init__(self,class_names = ['0','1'],predictor:PredictorForSingleTextClf = None):
        """_summary_

        Args:
            class_names (list, optional): _description_. Defaults to ['0','1'].

            sent_clf (PredictorForSingleTextClf, optional): _description_. Defaults to None.
             sent_clf = PredictorForSingleTextClf(
                    predictor_config = {
                            "model_checkpoint":"saved_model",
                            "device":"cuda:0",
                            "max_length":256
                        },
                        id2label = {0: '0',
                                    1: '1',
                                    },
                        ClfModelClass= WeightMechSentClf
                )
        """        
        self.class_names = class_names
        global sent_clf
        sent_clf = predictor

    def ana_text_clf_by_lime(
        self,
        str_to_predict = "Our experiments show that our reranking system using parts of speech and syntactic features improves performance and achieves state-of-theart quality , with an F0.5 score of 40.0 .",
        saved_dir = "./",
        saved_name = ""
        ):
        """基于lime 对文本分类进行可解释分析的主函数

        Args:
            str_to_predict (str, optional): _description_. Defaults to "Our experiments show that our reranking system using parts of speech and syntactic features improves performance and achieves state-of-theart quality , with an F0.5 score of 40.0 .".
            saved_dir (str, optional): _description_. Defaults to "./".
            saved_name (str, optional): _description_. Defaults to "".

        Returns:
            _type_: _description_
        """        
        explainer = LimeTextExplainer(class_names=self.class_names)

        exp = explainer.explain_instance(str_to_predict, lime_predictor, num_features=20, num_samples=1500)
        if len(saved_name) > 0:
            fig = exp.as_pyplot_figure()
            fig.savefig(fname="{}/{}.svg".format(saved_dir,saved_name))

            html = exp.as_html()
            with open("{}/{}.html".format(saved_dir,saved_name),"w") as f:
                f.write(html)
        return exp
       





