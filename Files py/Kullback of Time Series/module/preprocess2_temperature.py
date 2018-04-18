import sys

from module.Kullback2_temp import TransformData
import pandas as pd
import matplotlib.pyplot as plt


def inicio(variable: str,data16: str, data17: str) -> (list,list):
    # FilterData.clear_data("SJL")
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
    data1 = pd.read_csv(data16, sep=",",
                        names=['date', variable],
                        date_parser=dateparse, squeeze=True)
    data2 = pd.read_csv(data17, sep=",",
                        names=['date', variable],
                        date_parser=dateparse, squeeze=True )


    #print(data1)
    #print(data1)

    data1.set_index('date',inplace=True)
    data2.set_index('date', inplace=True)

    #print(data1.index.min())
    full_range = pd.date_range(data1.index.min(), data1.index.max())


    data1 = data1.reindex(full_range, fill_value=0)
    data2 = data2.reindex(full_range, fill_value=0)



    #print(data1)


    axes_x, result = TransformData.create_list(data1, data2, '1970-01-01', '1970-04-30', variable)


    print(axes_x)

    data_kullback = pd.DataFrame(result, index=axes_x,columns=["KL"])

    #print(data_kullback)

    #print(data_kullback['1-30/1-31':])


    # return axes_x, result
    ax = data_kullback.plot(kind='line', color='#55007f', legend=False, linewidth=3)
    ax.set_title("CAUDAL", loc='center',fontweight='bold')
    ax.margins(.05)
    ax.tick_params(labelsize=15)
    ax.set_xlabel('Weekly Window', fontsize=15)
    ax.set_ylabel("Coefficient of Divergence", fontsize=15)


    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(top=0.98, right=0.98, left=0.055, bottom=0.15)
    plt.grid()
    plt.show()





if __name__ == '__main__':
    #sys.exit(inicio("/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/data16_huarmey_kl.csv","/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/data17_huarmey_kl.csv"))
    sys.exit(inicio("caudal","/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/mala_caudalkl16.csv","/Users/gabriela/Documents/datamining/resilience_project-kl/kullback/data/mala_caudalkl17.csv"))
