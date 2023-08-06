# -*- coding: utf-8 -*-
# file: boosting.py
# time: 2021/12/27
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import os

import autocuda
import random
import warnings

from metric_visualizer import MetricVisualizer

from boost_aug import BoostingAug, AugmentBackend

from pyabsa.functional import APCConfigManager, ClassificationConfigManager
from pyabsa.functional import ABSADatasetList, ClassificationDatasetList
from pyabsa.functional import APCModelList, BERTClassificationModelList

warnings.filterwarnings('ignore')

aug_backends = [
    AugmentBackend.EDA,
    AugmentBackend.SplitAug,
    AugmentBackend.SpellingAug,
    AugmentBackend.ContextualWordEmbsAug,
    AugmentBackend.BackTranslationAug,

]
device = autocuda.auto_cuda()

seeds = [random.randint(0, 10000) for _ in range(2)]

# config = APCConfigManager.get_apc_config_english()
# config.model = APCModelList.FAST_LCF_BERT
# config.lcf = 'cdw'
# config.similarity_threshold = 1
# config.max_seq_len = 80
# config.dropout = 0
# config.optimizer = 'adam'
# config.cache_dataset = False
# config.patience = 10
# config.pretrained_bert = 'bert-base-uncased'
# config.hidden_dim = 768
# config.embed_dim = 768
# config.log_step = -1
# config.SRD = 3
# config.learning_rate = 1e-5
# config.batch_size = 16
# config.num_epoch = 15
# config.evaluate_begin = 5
# config.l2reg = 1e-8
# config.seed = seeds
# config.cross_validate_fold = -1  # disable cross_validate
#
# for backend in aug_backends:
#     print('*' * 100)
#     MV = MetricVisualizer(name=backend + '-' + config.model.__name__,
#                           trial_tag='Dataset',
#                           # trial_tag_list=['Lap14', 'Rest14', 'Rest15', 'Rest16', 'MAMS'])
#                           trial_tag_list=['MAMS'])
#     config.MV = MV
#     for dataset in [
#         # ABSADatasetList.Laptop14,
#         # ABSADatasetList.Restaurant14,
#         # ABSADatasetList.Restaurant15,
#         # ABSADatasetList.Restaurant16,
#         ABSADatasetList.MAMS
#     ]:
#         BoostingAugmenter = BoostingAug(ROOT=os.getcwd(), AUGMENT_BACKEND=backend, AUGMENT_NUM_PER_CASE=3, device=device)
#         BoostingAugmenter.apc_cross_boost_training(config,
#                                                    dataset,
#                                                    train_after_aug=True,
#                                                    rewrite_cache=True,
#                                                    )
#         # BoostingAugmenter.apc_classic_boost_training(config,
#         #                                              dataset
#         #                                              )
#         config.MV.next_trial()
#     config.MV.summary()

config = ClassificationConfigManager.get_classification_config_english()
config.model = BERTClassificationModelList.BERT
config.lcf = 'cdw'
config.similarity_threshold = 1
config.max_seq_len = 80
config.dropout = 0
config.optimizer = 'adam'
config.cache_dataset = False
config.patience = 5
# config.pretrained_bert = 'microsoft/deberta-v3-base'
config.pretrained_bert = 'bert-base-uncased'
config.hidden_dim = 768
config.embed_dim = 768
config.log_step = -1
config.SRD = 3
config.learning_rate = 1e-5
config.batch_size = 16
config.num_epoch = 15
config.evaluate_begin = 0
config.l2reg = 1e-8
config.seed = seeds
config.cross_validate_fold = -1  # disable cross_validate

for backend in aug_backends:
    print('*' * 100)
    MV = MetricVisualizer(name=backend + '-' + config.model.__name__,
                          trial_tag='Dataset',
                          trial_tag_list=['SST2', 'SST5'])
    config.MV = MV
    for dataset in [
        ClassificationDatasetList.SST2,
        ClassificationDatasetList.SST1
    ]:
        BoostingAugmenter = BoostingAug(ROOT=os.getcwd(), AUGMENT_BACKEND=backend, AUGMENT_NUM_PER_CASE=3, device=device)
        BoostingAugmenter.tc_cross_boost_training(config,
                                                  dataset,
                                                  train_after_aug=True,
                                                  rewrite_cache=True,
                                                  )
        # BoostingAugmenter.tc_classic_boost_training(config,
        #                                              dataset
        #                                              )
        config.MV.next_trial()
    config.MV.summary()
