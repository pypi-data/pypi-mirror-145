# -*- coding: utf-8 -*-
# @Time    : 2022/4/4 10:32 下午
# @Author  : jeffery
# @FileName: ner.py
# @github  : https://github.com/jeffery0628
# @Description:

from collections import Counter
from seqeval.reporters import StringReporter


def entity_precision(label_entites, preds_entities):
    origins = label_entites
    founds = preds_entities
    rights = [entity for entity in preds_entities if entity in origins]
    return 0 if len(founds) == 0 else (len(rights) / len(founds))


def entity_recall(label_entites, preds_entities):
    origins = label_entites
    founds = preds_entities
    rights = [entity for entity in preds_entities if entity in origins]
    return 0 if len(origins) == 0 else (len(rights) / len(origins))


def entity_f1(label_entites, preds_entities):
    origins = label_entites
    founds = preds_entities
    rights = [entity for entity in preds_entities if entity in origins]
    recall = 0 if len(origins) == 0 else (len(rights) / len(origins))
    precision = 0 if len(founds) == 0 else (len(rights) / len(founds))
    return 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)

def idenf_f1(label_entites, preds_entities):
    origins = [[x[0],x[1]] for x in label_entites]
    founds = [[x[0],x[1]] for x in  preds_entities]
    rights = [entity for entity in preds_entities if entity in origins]
    recall = 0 if len(origins) == 0 else (len(rights) / len(origins))
    precision = 0 if len(founds) == 0 else (len(rights) / len(founds))
    return 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)



def entity_classification_report(label_entites, preds_entities):
    origins = label_entites
    founds = preds_entities
    rights = [entity for entity in preds_entities if entity in origins]

    class_info = {}
    origin_counter = Counter([x[2] for x in origins])
    found_counter = Counter([x[2] for x in founds])
    right_counter = Counter([x[2] for x in rights])
    target_names = set()
    for type_, count in origin_counter.items():
        target_names.add(type_)
        origin = count
        found = found_counter.get(type_, 0)
        right = right_counter.get(type_, 0)
        recall = 0 if origin == 0 else (right / origin)
        precision = 0 if found == 0 else (right / found)
        f1 = 0. if recall + precision == 0 else (2 * precision * recall) / (precision + recall)
        class_info[type_] = {"precision": round(precision, 4), 'recall': round(recall, 4), 'f1-score': round(f1, 4),
                             'support': count}

    width = max(map(len, target_names))
    reporter = StringReporter(width=width, digits=2)
    for k, v in class_info.items():
        reporter.write(k, v['precision'], v['recall'], v['f1-score'], v['support'])
    reporter.write_blank()
    # micro
    micro_precision = 0 if len(founds) == 0 else (len(rights) / len(founds))
    micro_recall = 0 if len(origins) == 0 else (len(rights) / len(origins))
    micro_f1 = 0. if micro_recall + micro_precision == 0 else (2 * micro_precision * micro_recall) / (
                micro_precision + micro_recall)
    reporter.write('micro avg', micro_precision, micro_recall, micro_f1, len(origins))
    # macro
    macro_precision = sum([v['precision'] for v in class_info.values()]) / (len(class_info))
    macro_recall = sum([v['recall'] for v in class_info.values()]) / (len(class_info))
    macro_f1 = sum([v['f1-score'] for v in class_info.values()]) / (len(class_info))
    reporter.write('macro avg', macro_precision, macro_recall, macro_f1, len(origins))
    # weight
    weight_precision = sum([v['precision'] * v['support'] for v in class_info.values()]) / (len(origins))
    weight_recall = sum([v['recall'] * v['support'] for v in class_info.values()]) / (len(origins))
    weight_f1 = sum([v['f1-score'] * v['support'] for v in class_info.values()]) / (len(origins))
    reporter.write('weighted avg', weight_precision,weight_recall,weight_f1,len(origins))
    return reporter.report()