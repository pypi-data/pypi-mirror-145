import json
from pathlib import Path

import json
from pathlib import Path

import numpy as np
from tensorflow.keras.callbacks import Callback


class HintTermostat(Callback):
    def __init__(self, tokenizer_path, target_loss, log_path, init_step=0, verbose=False):
        super(HintTermostat, self).__init__()
        self.levels = np.abs(np.load(Path(tokenizer_path) / 'termostat.npy'))
        with open(Path(tokenizer_path) / 'hints.json', 'r', encoding='utf-8') as fr:
            self.hints = json.load(fr)
        self.level_num = init_step
        self.target_loss = target_loss
        self.log_path = Path(log_path)
        self.verbose = verbose

    def get_distribution(self):
        return self.levels[self.level_num]

    def on_epoch_end(self, epoch, logs=None):
        loss = logs['loss']
        if loss < self.target_loss:
            self.level_num += 1
        else:
            self.level_num -= 1

        # Saturate by range of values
        self.level_num = max(self.level_num, 0)
        self.level_num = min(self.level_num, self.levels.shape[0])
        if self.verbose:
            print(f'Level: {self.level_num}/{self.levels.shape[0]}')
        with open(self.log_path / 'levels.txt', 'a', encoding='utf-8') as fw:
            print(f'{self.level_num}', file=fw)
