
import numpy as np
# import matplotlib.pyplot as plt
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

    def __init__(self, testData, resultData, jsonfile, weightfile):
        self.testData = testData
        self.resultData = resultData
        self.jsonfile = jsonfile
        self.weightfile = weightfile

    def dataset(self):
        #DataSetの読み込み

        TestData = np.loadtxt(os.getcwd() + self.testData,        # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )
        
        ResultData = np.loadtxt(os.getcwd() + self.resultData,        # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )

        data = TestData, ResultData

        return data

    def load(self):
        
        model = model_from_json(open(jsonfile).read()) 
        model.load_weights(weightfile)
        model.summary()

        return model

    def pred(self, model, data):
        # TestData = np.loadtxt(os.getcwd() + testDataPath,        # 読み込みたいファイルのパス
        #                         delimiter=",",                      # ファイルの区切り文字
        #                         skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
        #                         dtype=np.float32
        #                         )
        
        # ResultData = np.loadtxt(os.getcwd() + resultDataPath,        # 読み込みたいファイルのパス
        #                         delimiter=",",                      # ファイルの区切り文字
        #                         skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
        #                         dtype=np.float32
        #                         )

        #inputdata, outputdata = data
        pred_y = model.predict(data[0]) #最後に再度実行

        real = data[0], data[1]
        prediction = data[0],pred_y

        future = real, prediction

        # 二乗平方根で誤差を算出
        # mse = mean_squared_error(data[1], pred_y)

        # # 可視化
        # df = pd.DataFrame(pred_y, columns=['pred'])
        # df['act'] = pd.DataFrame(data[1])
        # fig, ax = plt.subplots(figsize=(15,4))
        # ax.plot(df['pred'], label='pred')
        # ax.plot(df['act'], label='act')
        # ax.legend()
        # fig.savefig(os.path.join(LOG_DIR, PREDICT_FILE))

        return future

class kickoff():

    def __init__(self, testData, resultData, jsonfile, weightfile):
        self.testData = testDataPath
        self.resultData = resultDataPath
        self.jsonfile = jsonfile
        self.weightfile = weightfile

    def run(self):

        #インスタンスを作成
        inst = Predict(testDataPath,resultDataPath,jsonfile,weightfile)

        #モデルの読み込み
        #model = load(os.path.join(MODEL_DIR, JSON_FILE), os.path.join(MODEL_DIR, WEIGHT_FILE))
        model = inst.load()

        #推定データの読み込み
        data = inst.dataset()

        #データの推定
        pred(model, data)
