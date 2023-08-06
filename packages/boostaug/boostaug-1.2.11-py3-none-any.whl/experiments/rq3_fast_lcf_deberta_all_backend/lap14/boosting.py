# -*- coding: utf-8 -*-
# file: boosting.py
# time: 2021/12/27
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.
import shutil
import autocuda
import findfile
import random
import warnings

from metric_visualizer import MetricVisualizer

from boost_aug import BoostingAug, AugmentBackend

from pyabsa.functional import APCConfigManager
from pyabsa.functional import ABSADatasetList
from pyabsa.functional import APCModelList

warnings.filterwarnings('ignore')

aug_backends = [
                AugmentBackend.SplitAug,
                AugmentBackend.BackTranslationAug,
                AugmentBackend.SpellingAug,
                AugmentBackend.ContextualWordEmbsAug
                ]
device = autocuda.auto_cuda()

seeds = [random.randint(0, 10000) for _ in range(3)]
apc_config_english = APCConfigManager.get_apc_config_english()
apc_config_english.model = APCModelList.FAST_LCF_BERT
apc_config_english.lcf = 'cdw'
apc_config_english.similarity_threshold = 1
apc_config_english.max_seq_len = 80
apc_config_english.dropout = 0
apc_config_english.optimizer = 'adam'
apc_config_english.cache_dataset = False
apc_config_english.patience = 10
apc_config_english.pretrained_bert = 'microsoft/deberta-v3-base'
apc_config_english.hidden_dim = 768
apc_config_english.embed_dim = 768
apc_config_english.log_step = 50
apc_config_english.SRD = 3
apc_config_english.learning_rate = 1e-5
apc_config_english.batch_size = 16
apc_config_english.num_epoch = 5
apc_config_english.evaluate_begin = 0
apc_config_english.l2reg = 1e-8
apc_config_english.seed = seeds
apc_config_english.cross_validate_fold = -1  # disable cross_validate

for backend in aug_backends:
    print('*'*100)
    for dataset in [ABSADatasetList.Laptop14,
                    ]:
        MV = MetricVisualizer(name=backend + '-' + dataset.dataset_name + '-' + apc_config_english.model.__name__,
                              trial_tag='Dataset',
                              trial_tag_list=['Lap14'])
        apc_config_english.MV = MV
        BoostingAugmenter = BoostingAug(AUGMENT_BACKEND=backend, device=device)
        BoostingAugmenter.apc_cross_boost_training(apc_config_english,
                                                   dataset,
                                                   rewrite_cache=True,
                                                   )
        # BoostingAugmenter.apc_classic_boost_training(apc_config_english,
        #                                              dataset
        #                                              )
        apc_config_english.MV.next_trial()
    apc_config_english.MV.summary()
