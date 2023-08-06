import argparse
from .spert import input_reader
from .spert.spert_trainer import SpERTTrainer
import json
import os

def train_model(config_path):
    run_args = argparse.Namespace(**json.load(open(config_path,"r")))
    trainer = SpERTTrainer(run_args)
    
    trainer.train(train_path=run_args.train_path, valid_path=run_args.valid_path,
                  types_path=run_args.types_path, input_reader_cls=input_reader.JsonInputReader)



def eval_model(config_path):
    run_args = argparse.Namespace(**json.load(open(config_path,"r")))
    trainer = SpERTTrainer(run_args)
    
    trainer.eval(dataset_path=run_args.dataset_path, types_path=run_args.types_path,
                 input_reader_cls=input_reader.JsonInputReader)


def pred_model_v1(config_path):
    from myLabTools.sciie.predictor import Predictor
    from myLabTools.sciie.spert import input_reader
    pred_args = json.load(open(config_path,"r"))
    run_args = argparse.Namespace(**pred_args)
    sciie = Predictor(
        run_args,
        types_path=run_args.types_path,
        input_reader_cls=input_reader.TextPredictionInputReader)
    sciie.predict_on_raw_text(text_list = [])

def pred_model_v2(config_path):
    run_args = argparse.Namespace(**json.load(open(config_path,"r")))
    trainer = SpERTTrainer(run_args)
    
    trainer.predict(dataset_path=run_args.dataset_path, types_path=run_args.types_path,
                 input_reader_cls=input_reader.JsonPredictionInputReader)