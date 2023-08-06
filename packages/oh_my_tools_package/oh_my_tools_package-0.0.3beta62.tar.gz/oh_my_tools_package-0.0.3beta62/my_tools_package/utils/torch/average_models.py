import argparse
import sys
import os
import torch

uer_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uer"))
sys.path.append(uer_dir)


def average_models(model_list_path):
    for i, model_path in enumerate(model_list_path):
        model = torch.load(model_path)
        if i == 0:
            avg_model = model
        else:
            for k, _ in avg_model.items():
                avg_model[k].mul_(i).add_(model[k]).div_(i+1)

    return avg_model


def save_avg_model(model_list_path,avg_model_path):
    avg_model = average_models(model_list_path)
    torch.save(avg_model, avg_model_path)






