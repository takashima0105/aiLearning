
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

    def __init__(self, testDatapath, resultDatapath, jsonfilepath, weightfilepath):
        self.testData = testDatapath
        self.resultData = resultDatapath
        self.jsonfile = jsonfilepath
        self.weightfile = weightfilepath

    def dataset(self):
        #DataSetの読み込み

        TestData = np.loadtxt(os.getcwd() + '/aiLearning' + self.testData,        # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )
        
        ResultData = np.loadtxt(os.getcwd() + '/aiLearning' + self.resultData,        # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )

        data = TestData, ResultData

        #モデルの読み込み        
        model = model_from_json(open(self.jsonfile).read()) 
        model.load_weights(self.weightfile)
        model.summary()

        #予測を実行
        pred_y = model.predict(data[0]) 
        pred_r = []
        
        #予測結果を２次元配列から１次元配列に変換
        for i in range(pred_y.shape[0]):
            pred_r.append(pred_y[i][0])

        #学習データ
        real = data[0], data[1]
        
        #予測結果
        prediction = data[0],pred_r

        #学習データと予測結果を戻り値に
        future = real, prediction

        return future

class Kickoff():

    def __init__(self, testDataPath, resultDataPath, jsonfilepath, weightfilepath):
        self.testData = testDataPath
        self.resultData = resultDataPath
        self.jsonfile = jsonfilepath
        self.weightfile = weightfilepath

    def run(self):

        #インスタンスを作成
        inst = Predict(self.testData,self.resultData,self.jsonfile,self.weightfile)

        #予測を実行
        result = inst.dataset()

        return result
