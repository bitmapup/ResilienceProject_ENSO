import sys

from module.Kullback_temp import TransformData
import pandas as pd
import matplotlib.pyplot as plt


def inicio() -> (list,list):
    # FilterData.clear_data("SJL")
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
    data = pd.read_csv("/Users/gabriela/Documents/datamining/TEMP_HUARMEY_2017.csv", sep=",", date_parser=dateparse, squeeze=True)
    print('#######')
    data.set_index('date',inplace=True)
    
    print(data)
    print('------------')

    full_range = pd.date_range(data.index.min(), data.index.max())

    #print(full_range)
    data = data.reindex(full_range, fill_value=0)
    axes_x, result = TransformData.create_list(data, '2017-01-01', '2017-08-30', 'Temperature')


    print('------------len')
    print(len(result))

    print('------------')

    data_kullback = pd.DataFrame(result, index=axes_x,columns=["KL"])


    print(data_kullback['1-30/1-31':])
    # return axes_x, result
    ax = data_kullback.plot(kind='line', color='#55007f', legend=False, linewidth=3)
    ax.margins(.05)
    ax.tick_params(labelsize=15)
    ax.set_xlabel('Weekly Window', fontsize=15)
    ax.set_ylabel("Coefficient of Divergence", fontsize=15)

    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(top=0.98, right=0.98, left=0.055, bottom=0.15)
    plt.show()



if __name__ == '__main__':
    sys.exit(inicio())