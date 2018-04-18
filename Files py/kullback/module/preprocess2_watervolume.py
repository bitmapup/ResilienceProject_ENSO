import sys

from module.Kullback2_caudal import TransformData
import pandas as pd
import matplotlib.pyplot as plt


def inicio() -> (list,list):
    # FilterData.clear_data("SJL")
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
    data1 = pd.read_csv("/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/caudalrimac16_kl.csv", sep=",",
                        names=['date', 'Flow'],
                        date_parser=dateparse, squeeze=True)
    data2 = pd.read_csv("/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/caudalrimac17_kl.csv", sep=",",
                        names=['date', 'Flow'],
                        date_parser=dateparse, squeeze=True)


    print(data1)
    #print(data1)

    data1.set_index('date',inplace=True)
    data2.set_index('date', inplace=True)

    print('#######')
    #print(data1.index.min())
    full_range = pd.date_range(data1.index.min(), data1.index.max())


    data1 = data1.reindex(full_range, fill_value=0)
    data2 = data2.reindex(full_range, fill_value=0)

    #print(data1)


    print(data1)


    axes_x, result = TransformData.create_list(data1, data2, '1970-03-01', '1970-04-30', 'Flow')

    #print('#######lenresult')

    #print(len(result))

    data_kullback = pd.DataFrame(result, index=axes_x,columns=["KL"])

    print(data_kullback)

    #print(data_kullback['1-30/1-31':])

    print('#######')

    # return axes_x, result
    ax = data_kullback.plot(kind='line', color='#55007f', legend=False, linewidth=3)
    ax.margins(.05)
    ax.tick_params(labelsize=15)
    ax.set_xlabel('Weekly Window', fontsize=15)
    ax.set_ylabel("Coefficient of Divergence", fontsize=15)

    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(top=0.98, right=0.98, left=0.055, bottom=0.15)
    plt.grid()
    plt.show()





if __name__ == '__main__':
    sys.exit(inicio())