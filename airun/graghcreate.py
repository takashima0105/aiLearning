import numpy as np
from django.core.files.storage import ds
import plotly.offline as plt   # オフライン用
import plotly.graph_objs as go
import os.path as path


class GraphCreate():

    def __init__(self, inputpath, outputpath):
        self.input = path.join(ds.path('inputs'), path.basename(inputpath))
        self.output = path.join(ds.path('outputs'), path.basename(outputpath))

    def Create(self):
        inputData = np.loadtxt(self.input,
                               delimiter=',',
                               skiprows=0,
                               dtype=np.float32
                               )

        outputData = np.loadtxt(self.output,     # 読み込みたいファイルのパス
                                delimiter=',',       # ファイルの区切り文字
                                skiprows=0,          # 先頭の何行を無視するか
                                dtype=np.float32
                                )

        indexList = []
        for index in range(inputData.shape[1]):

            trace = go.Scatter(
                        x=inputData[:, index],
                        y=outputData,
                        name='ThisTeacherData',
                        mode='markers',
                        marker=dict(size=10, color='rgb(255, 0, 255)'))

            layout = go.Layout(
                        title='ThisTeacherDataGraph',
                        xaxis=dict(title=('FitureValue-' + str(index))),
                        yaxis=dict(title='OutputValue'),
                        showlegend=True)

            data = [trace]
            fig = dict(data=data, layout=layout)
            indexList.append((index, '特徴量：' + str(index)))

            # オフラインでプロット
            plt.plot(fig, filename='TeacherData_Value' + str(index) +
                     '.html', auto_open=True)

        return indexList
