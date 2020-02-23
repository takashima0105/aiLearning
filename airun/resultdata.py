import numpy as np
from django.core.files.storage import default_storage as ds
import plotly.offline as plt   # オフライン用
import plotly.graph_objs as go
import os.path as path


class ResultGraph():

    def __init__(self, inputdata, outputdata, resultdata):
        self.input = inputdata
        self.output = outputdata
        self.result = resultdata

    def Create(self):
        indexList = []
        scriptlist = []
        for index in range(self.input.shape[1]):

            trace = go.Scatter(
                        x=self.input[:, index],
                        y=self.output,
                        name='ThisTeacherData',
                        mode='markers',
                        marker=dict(size=10, color='rgb(0, 134, 255)'))
            
            result = go.Scatter(
                        x=self.input[:, index],
                        y=self.result,
                        name='ThisTeacherData',
                        mode='markers',
                        marker=dict(size=10, color='rgb(0, 219, 0)')) 

            layout = go.Layout(
                        title='ThisTeacherDataGraph',
                        xaxis=dict(title=('FitureValue-' + str(index))),
                        yaxis=dict(title='OutputValue'),
                        height=450,
                        showlegend=True)

            data = [trace, result]
            fig = dict(data=data, layout=layout)
            indexList.append((index, '特徴量：' + str(index)))

            # オフラインでプロット
            scriptlist.append(plt.plot(fig, output_type='div'))

        return indexList, scriptlist