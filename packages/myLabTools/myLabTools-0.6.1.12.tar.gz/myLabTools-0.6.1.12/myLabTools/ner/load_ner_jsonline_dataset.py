from tkinter.messagebox import NO
from datasets import load_dataset
from transformers import AutoTokenizer


tokenizer  = None
def data_process(examples):
    global tokenizer
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True,max_length=400, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples[f"ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Map tokens to their respective word.
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:  # Set the special tokens to -100.
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:  # Only label the first token of a given word.
                label_ids.append(label[word_idx])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs

class NERDataLoader:
    """命名实体识别中的数据加载模块
    """    
    def __init__(self,tokenizer_path="./sci_bert_allenai"):
        global tokenizer
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
    

    def load_encode_dataset(self,file_paths = {}):

        dataset = load_dataset("json",data_files = file_paths)
        encode_dataset = dataset.map(data_process,batched=True)
        return encode_dataset