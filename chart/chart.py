import matplotlib.pyplot as plt
import pandas as pd
import os
from module.loadData import loadJsonData
from io import BytesIO

class drawChart():
    _jsonData = None
    _data : pd.DataFrame = None
    
    def __init__(self, jsonData):
        self._jsonData = jsonData
        self._data = loadJsonData(self._jsonData)
        # print(self._data)

    # draw graph
    def drawGraph(self, graphType : str = None, graphStyle : plt.style.available = 'ggplot'):
        
        plt.style.use(graphStyle)
        data = self._data

        convBase64 = BytesIO()

        # Default Line Graph
        if graphType == None:
            dfGraph = data.T
            fig = plt.figure(figsize=(14, 5))
            
            ax = fig.add_subplot(1, 1, 1)
            
            plt.xlabel('Day')
            plt.ylabel("Count")
            plt.xticks(rotation = 45)
            
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker='o',
                    markersize=10,
                    lw=2,
                    label=f'{self._data.columns[i]}',
                )
            plt.legend(loc='best')
            
        # Line & Bar Graph
        elif graphType == 'twin':
            dfGraph = data.T
            
            # Bar Graph
            ax1 = data.plot(
                kind = 'bar',
                figsize=(12, 5),
                width = 0.7,
                stacked=True,
            )
            
            ax = ax1.twinx()
            
            plt.xlabel('Day')
            plt.ylabel("Count")
            plt.xticks(rotation = 45)
            
            # Line Graph
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker='o',
                    markersize=10,
                    lw=2,
                    label=f'{self._data.columns[i]}',
                )
            ax1.legend(loc='best')
        
        # Bar, Pie Graph
        else:
            # Bar Graph
            if graphType == 'bar':
                data.plot(
                    kind = graphType,
                    figsize=(12, 5),
                    width = 0.7,
                    stacked=True,
                )
                plt.legend(loc='best')
                
            # Pie Graph
            else:
                dfGraph = data
                dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum(axis=0)
                dfGraph = dfGraph.T
                dfGraph.drop('NULL', axis=0, inplace=True)
                
                dfGraph['Total'].plot(
                    kind='pie',
                    figsize=(20, 12),
                    autopct='%.2f%%',    # %% : % 출력
                    startangle=10,
                )
                plt.xlabel(f'{dfGraph.columns[0]} ~ {dfGraph.columns[-2]} Status Pie Chart')
                plt.legend(labels = data.columns, loc='best')
        
        plt.savefig(convBase64, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        import base64
        
        convBase64 = base64.b64encode(convBase64.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % convBase64        
