
import os
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.callbacks import EarlyStopping
from keras.optimizers import SGD
import keras.callbacks
import keras.backend.tensorflow_backend as KTF
import pandas as pd
import keras as ks
from sklearn.metrics import mean_squared_error
import pathlib

MODEL_FILE = 'model.json'
WEIGHT_FILE = 'weights.hdf5'
HISTORY_FILE = 'history.csv'
GRAPH1_FILE = 'history.png'
GRAPH2_FILE = 'prediction.png'
LOG_DIR = './log'

BATCH_SIZE = 10

class Method():
    def __init__(self, inputDataPath, outputDataPath, epoch):
        self.inputDataPath = inputDataPath
        self.outputDataPath = outputDataPath
        self.epoch = epoch

        #MODEL保存用パス
        self.MODELDIR = './aiLearning/media/model'
        #WEIGHT保存パス
        self.WEIGHTDIR = './aiLearning/media/weight'

    def create_datasets_and_labels(self, test_size):
        #DataSetの読み込み
        originalData = np.loadtxt(self.inputDataPath,               # 読み込みたいファイルのパス
                                delimiter=",",                      # ファイルの区切り文字
                                skiprows=0,                         # 先頭の何行を無視するか（指定した行数までは読み込まない）
                                dtype=np.float32
                                )

        # #データをランダムに並び替える
        originalData = np.random.permutation(originalData)

        inputData = originalData[:,1:]
        outputData = originalData[:,:1]

        #教師データと判定データにわける
        input_testing_size = int(test_size*len(inputData))
        output_testing_size = int(test_size*len(outputData))

        train_x = inputData[:][:(-input_testing_size)]
        test_x = inputData[:][(-input_testing_size):]
        train_y = outputData[:][:(-output_testing_size)]
        test_y = outputData[:][(-output_testing_size):]

        return train_x,test_x,train_y,test_y

    def model_create(self, train_x, train_y):
        model = Sequential()
        
        # 隠れ層１を作成
        model.add(Dense(20,input_dim = train_x.shape[1],name='dense1'))
        model.add(Activation('relu', name='relu1'))
        #model.add(Dropout(0.2, name='dropout1'))

        # 隠れ層２を作成
        model.add(Dense(20, name='dense2'))
        model.add(Activation('relu', name='relu2'))
        #model.add(Dropout(0.2, name='dropout2'))

        #出力層を定義
        model.add(Dense(train_y.shape[1], name='dense3'))
        #model.add(Activation('softmax', name='softmax1'))       
        
        # モデルコンパイル
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        model.summary()

        return model

    def save(self, result):
        model = result['model']
        history = result['history']
        loss = result['loss']
        acc = result['acc']

        # def plot_history_loss(fit):
        #     axL.plot(fit.history['loss'],label="loss for training")
        #     axL.plot(fit.history['val_loss'],label="loss for validation")
        #     axL.set_title('model loss')
        #     axL.set_xlabel('epoch')
        #     axL.set_ylabel('loss')
        #     axL.legend(loc='upper right')

        # def plot_history_acc(fit):
        #     axR.plot(fit.history['accuracy'],label="loss for training")
        #     axR.plot(fit.history['val_accuracy'],label="loss for validation")
        #     axR.set_title('model accuracy')
        #     axR.set_xlabel('epoch')
        #     axR.set_ylabel('accuracy')
        #     axR.legend(loc='upper right')

        #モデル・重み保存用の名前取得

        filepath = pathlib.Path(self.inputDataPath)
        filename = filepath.stem

        #モデル保存
        model_json = model.to_json()
        jsonFile = pathlib.Path(self.MODELDIR) / pathlib.Path(filename + '.json')
        with jsonFile.open(mode='w') as jfile:
            jfile.write(model_json)

        #重み保存
        weightFile= pathlib.Path(self.WEIGHTDIR) / pathlib.Path(filename + '.hdf5')
        model.save_weights(weightFile)

        # 履歴をファイルに保存
        # pd.DataFrame.from_dict(history.history).to_csv(os.path.join(LOG_DIR,HISTORY_FILE))   

        # fig, (axL, axR) = plt.subplots(ncols=2,figsize=(10, 5), dpi=96)
        # plot_history_loss(history)
        # plot_history_acc(history)
        # fig.savefig(os.path.join(LOG_DIR, GRAPH1_FILE))

        return jsonFile, weightFile

    def train_model(self, data, model):

        train_x,test_x,train_y,test_y = data

        history = model.fit(train_x, 
                        train_y, 
                        batch_size=BATCH_SIZE,
                        epochs=self.epoch, 
                        verbose=1, 
                        validation_data=(test_x, test_y))
        
        loss, acc = model.evaluate(test_x, test_y, verbose=0)
        result = {'model': model, 'history': history, 'loss': loss, 'acc': acc}

        return result

    def predict(self, data, model):

        train_x,test_x,train_y,test_y = data
        # 予測値の取得
        pred_y = model.predict(test_x)

        # 二乗平方根で誤差を算出
        mse = mean_squared_error(test_y, pred_y)
        print("KERAS REG RMSE : %.2f" % (mse ** 0.5))
        print("KERAS REG SCORE: %3.2f" % (1.0 - mse ** 0.5 / test_y.mean()))

        # 可視化
        df = pd.DataFrame(pred_y, columns=['pred'])
        df['act'] = pd.DataFrame(test_y)
        fig, ax = plt.subplots(figsize=(15,4))
        ax.plot(df['pred'], label='pred')
        ax.plot(df['act'], label='act')
        ax.legend()
        fig.savefig(os.path.join(LOG_DIR, GRAPH2_FILE))

        return mse


class Prediction():

    def __init__(self, inputDataPath, outputDataPath, epoch):
        self.inputData = inputDataPath
        self.outputData = outputDataPath
        self.epoch = epoch

    def main(self):

        #関数クラスのインスタンス作成
        m = Method(self.inputData, self.outputData, self.epoch)

        #教師データ、テストデータの読み込み
        data = m.create_datasets_and_labels(0.2)

        #モデル作成
        model = m.model_create(data[0], data[2])

        #学習実行
        result = m.train_model(data,model)

        #各種データの保存
        jsonpath, weightpath = m.save(result)

        return jsonpath, weightpath


