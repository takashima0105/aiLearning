
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
import os
import pandas as pd
from sklearn.metrics import mean_squared_error

MODEL_DIR = './model'
LOG_DIR = './log'
JSON_FILE = 'model.json'
WEIGHT_FILE = 'weights.hdf5'
PREDICT_FILE = 'predict.png'


class Predict():

    def create_datasets_and_labels(self):
        # DataSetの読み込み
        originalData = np.loadtxt(os.getcwd() + '/predict.csv',        # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )

        inputData = originalData[:,1:]
        outputData = originalData[:,:1]

        return inputData, outputData

    def __init__(self):
        pass

    def load(self, jsonfile, weightfile):

        model = model_from_json(open(jsonfile).read())
        model.load_weights(weightfile)
        model.summary()

        return model

    def pred(self, model, data):

        inputdata, outputdata = data
        pred_y = model.predict(inputdata)

        # 二乗平方根で誤差を算出
        mse = mean_squared_error(outputdata, pred_y)

        # 可視化
        df = pd.DataFrame(pred_y, columns=['pred'])
        df['act'] = pd.DataFrame(outputdata)
        fig, ax = plt.subplots(figsize=(15,4))
        ax.plot(df['pred'], label='pred')
        ax.plot(df['act'], label='act')
        ax.legend()
        fig.savefig(os.path.join(LOG_DIR, PREDICT_FILE))

        return mse

    def run(self):

        #モデルの読み込み
        model = load(os.path.join(MODEL_DIR, JSON_FILE), os.path.join(MODEL_DIR, WEIGHT_FILE))
        #推定データの読み込み
        data = create_datasets_and_labels()
        #データの推定
        pred(model, data)
