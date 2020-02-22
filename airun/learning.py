
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
from keras import optimizers
import pathlib

MODEL_FILE = 'model.json'
WEIGHT_FILE = 'weights.hdf5'
LOG_DIR = './log'

class Method():
    def __init__(self, contexts):
        self.inputDataPath = contexts['inputData']
        self.outputDataPath = contexts['outputData']
        self.epoch = contexts['epoch']
        self.batchSize = contexts['batchSize']
        self.hiddenLayer = contexts['hiddenLayer']
        self.node = contexts['node']
        self.testSize = contexts['testSize']

        # MODEL保存用パス
        self.MODELDIR = './aiLearning/result/model'
        # WEIGHT保存パス
        self.WEIGHTDIR = './aiLearning/result/weight'

    def create_datasets_and_labels(self, test_size):
        # DataSetの読み込み
        inputData = np.loadtxt('/Users/yusuke/Desktop/AI/aiLearning/aiLearning' + self.inputDataPath,  # 読み込みたいファイルのパス
                               delimiter=",",       # ファイルの区切り文字
                               skiprows=0,          # 先頭の何行を無視するか
                               dtype=np.float32
                               )

        outputData = np.loadtxt('/Users/yusuke/Desktop/AI/aiLearning/aiLearning' + self.outputDataPath,  # 読み込みたいファイルのパス
                                delimiter=",",        # ファイルの区切り文字
                                skiprows=0,           # 先頭の何行を無視するか
                                dtype=np.float32
                                )

        # データをランダムに並び替える
        originalData = np.c_[outputData, inputData]
        originalData = np.random.permutation(originalData)

        inputData = originalData[:, 1:]
        outputData = originalData[:, :1]

        # 教師データと判定データにわける
        input_testing_size = int((self.testSize/100)*len(inputData))
        output_testing_size = int((self.testSize/100)*len(outputData))

        train_x = inputData[:][:(-input_testing_size)]
        test_x = inputData[:][(-input_testing_size):]
        train_y = outputData[:][:(-output_testing_size)]
        test_y = outputData[:][(-output_testing_size):]

        return train_x, test_x, train_y, test_y

    def model_create(self, train_x, train_y):
        model = Sequential()

        # 隠れ層を作成
        for n in range(self.hiddenLayer):
            if n == 0:
                model.add(Dense(self.node, input_dim=train_x.shape[1]), name=('dense' + (n + 1)))
                model.add(Activation('relu', name=('relu' + (n + 1))))
            else:
                model.add(Dense(self.node, name=('dense' + (n + 1))))
                model.add(Activation('relu', name=('relu' + (n + 1))))

        # model.add(Dense(20, input_dim=train_x.shape[1], name='dense1'))
        # model.add(Activation('relu', name='relu1'))
        # # model.add(Dropout(0.2, name='dropout1'))

        # # 隠れ層２を作成
        # model.add(Dense(20, name='dense2'))
        # model.add(Activation('relu', name='relu2'))
        # # model.add(Dropout(0.2, name='dropout2'))

        # 出力層を定義
        model.add(Dense(train_y.shape[1], name='dense3'))
        # model.add(Activation('softmax', name='softmax1'))

        # モデルコンパイル
        model.compile(loss='mean_squared_error',
                      optimizer='adam',
                      metrics=['acc'])
        model.summary()

        return model

    def save(self, result):
        model = result['model']
        history = result['history']
        loss = result['loss']
        acc = result['acc']

        # モデル・重み保存用の名前取得
        filepath = pathlib.Path(self.inputDataPath)
        filename = filepath.stem

        # モデル保存
        model_json = model.to_json()
        jsonFile = pathlib.Path(self.MODELDIR) / pathlib.Path(filename + '.json')
        with jsonFile.open(mode='w') as jfile:
            jfile.write(model_json)

        # 重み保存
        weightFile = pathlib.Path(self.WEIGHTDIR) / pathlib.Path(filename + '.hdf5')
        model.save_weights(weightFile)

        return jsonFile, weightFile

    def train_model(self, data, model):

        train_x, test_x, train_y, test_y = data

        history = model.fit(train_x,
                            train_y,
                            batch_size=self.batchSize,
                            epochs=self.epoch,
                            verbose=1,
                            validation_data=(test_x, test_y))

        loss, acc = model.evaluate(test_x, test_y, verbose=0)
        result = {'model': model, 'history': history, 'loss': loss, 'acc': acc}

        return result


class Prediction():
    
    def __init__(self, contexts):
        self.contexts = contexts

    def main(self):

        # 関数クラスのインスタンス作成
        m = Method(contexts)

        # 教師データ、テストデータの読み込み
        data = m.create_datasets_and_labels(0.2)

        # モデル作成
        model = m.model_create(data[0], data[2])

        # 学習実行
        result = m.train_model(data, model)

        # 各種データの保存
        jsonpath, weightpath = m.save(result)

        return jsonpath, weightpath
