import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class TransformData:

    @staticmethod
    def kl(p, q):
        p = np.asarray(p, dtype=np.float)
        q = np.asarray(q, dtype=np.float)
        pk = 1.0 * p / np.sum(p, axis=0)
        qk = 1.0 * q / np.sum(q, axis=0)
        theta = 1e-4

        if pk.min() == 0 or qk.min() == 0:
            print("##########################")
            print("Original P: %s" % pk)
            print("Original Q: %s" % qk)
            pk_alt = pk
            qk_alt = qk
            if pk.min() == 0:
                #Smoothing data
                num_not_zero = np.count_nonzero(pk)
                num_zero = len(pk) - num_not_zero
                pk_alt = np.where(pk != 0, pk-theta*num_zero/num_not_zero, pk)
                pk_alt = np.where(pk_alt == 0, pk_alt+theta, pk_alt)
                print("P with smoothing: %s" % pk_alt)
            if qk.min() == 0:
                #Smoothing data
                num_not_zero = np.count_nonzero(qk)
                num_zero = len(qk) - num_not_zero
                qk_alt = np.where(qk != 0, qk-theta*num_zero/num_not_zero, qk)
                qk_alt = np.where(qk_alt == 0, qk_alt+theta, qk_alt)
                print("Q with smoothing: %s" % qk_alt)

            kullback_value = np.sum(pk_alt * np.log(pk_alt / qk_alt))
            print(print("Kullback value: %s" % kullback_value))
        else:
            kullback_value = np.sum(pk * np.log(pk / qk))
        return kullback_value

    @staticmethod
    def create_list(data1: pd.DataFrame, data2: pd.DataFrame , date_start: str, date_end: str, field: str) -> (list, list):

        data_dummy1 = data1[(data1.index.get_level_values(0) >= date_start) & (data1.index.get_level_values(0) <= date_end)]
        data_dummy2 = data2[(data2.index.get_level_values(0) >= date_start) & (data2.index.get_level_values(0) <= date_end)]

        full_range_dummy1 = pd.date_range(data_dummy1.index.min(), data_dummy1.index.max())
        full_range_dummy2 = pd.date_range(data_dummy2.index.min(), data_dummy2.index.max())
        #print(full_range_dummy)
        size = len(data_dummy1)
        i = 0
        list_dist1 = list()
        list_dist2 = list()

        while i + 6 < size:
            list_dist1.append(
                data_dummy1.loc[full_range_dummy1[i].strftime("%Y-%m-%d"):full_range_dummy1[i + 6].strftime("%Y-%m-%d")])
            list_dist2.append(
                data_dummy2.loc[full_range_dummy2[i].strftime("%Y-%m-%d"):full_range_dummy2[i + 6].strftime("%Y-%m-%d")])
            i += 1

        assert len(list_dist1) != 0
        assert len(list_dist2) != 0

        list_kl = list()
        list_ax = list()


        j = 0
        #print(list_dist)
        while j + 1 < len(list_dist1):
            print(list_dist1[j]["Price"])
            #print(list_dist[j][fiend])
            p = TransformData.kl(list_dist1[j][field], list_dist2[j][field])
            mi = list_dist1[j][field].index.min().month
            di = list_dist1[j][field].index.min().day
            mf = list_dist2[j][field].index.min().month
            df = list_dist2[j][field].index.min().day
            range_text = str(mi) + "-" + str(di) + "/" + str(mf) + "-" + str(df)
            list_ax.append(range_text)
            list_kl.append(p)
            if p == np.inf:
                print("Hola################################")
                #print(list_dist[j][fiend])
                #print(list_dist[j+1][fiend])
                ax = list_dist1[j]['Price'].plot(kind='bar', x=list_dist1[j].index,
                                                 stacked=True, color='#00BEC5', title='P of range {}'.format(range_text))
                ticklabels = [item.strftime('%Y-%m-%d') for item in list_dist1[j].index]
                ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
                plt.gcf().autofmt_xdate()
                plt.show()

                ax2 = list_dist2[j]['Price'].plot(kind='bar', x=list_dist2[j].index,
                                                    stacked=True, color='#F9746A', title='Q of range {}'.format(range_text))
                ticklabels = [item.strftime('%Y-%m-%d') for item in list_dist2[j].index]
                ax2.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
                plt.gcf().autofmt_xdate()
                plt.show()
            j += 1

        return list_ax, list_kl

