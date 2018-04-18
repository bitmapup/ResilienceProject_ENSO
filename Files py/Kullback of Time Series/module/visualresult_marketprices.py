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
    def create_list(data: pd.DataFrame, date_start: str, date_end: str, field: str) -> (list, list):
        print(data)
        data_dummy = data[(data.index.get_level_values(0) >= date_start) & (data.index.get_level_values(0) <= date_end)]
        full_range_dummy = pd.date_range(data_dummy.index.min(), data_dummy.index.max())
        print(full_range_dummy)
        size = len(data_dummy)
        i = 0
        list_dist = list()
        while i + 6 < size:
            list_dist.append(
                data_dummy.loc[full_range_dummy[i].strftime("%Y-%m-%d"):full_range_dummy[i + 6].strftime("%Y-%m-%d")])
            i += 1

        assert len(list_dist) != 0
        list_kl = list()
        list_ax = list()
        j = 0
        #print(list_dist)
        while j + 1 < len(list_dist):
            print(list_dist[j][field])
            #print(list_dist[j][fiend])
            p = TransformData.kl(list_dist[j][field], list_dist[j + 1][field])
            mi = list_dist[j][fieldd].index.min().month
            di = list_dist[j][fiend].index.min().day
            mf = list_dist[j+1][fiend].index.min().month
            df = list_dist[j+1][fiend].index.min().day
            range_text = str(mi) + "-" + str(di) + "/" + str(mf) + "-" + str(df)
            list_ax.append(range_text)
            list_kl.append(p)
            if p == np.inf:
                print("Hola################################")
                print(list_dist[j][fiend])
                print(list_dist[j+1][fiend])
                ax = list_dist[j]['Price'].plot(kind='bar', x=list_dist[j].index,
                                                 stacked=True, color='#00BEC5', title='P of range {}'.format(range_text))
                ticklabels = [item.strftime('%Y-%m-%d') for item in list_dist[j].index]
                ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
                plt.gcf().autofmt_xdate()
                plt.show()

                ax2 = list_dist[j+1]['Price'].plot(kind='bar', x=list_dist[j+1].index,
                                                    stacked=True, color='#F9746A', title='Q of range {}'.format(range_text))
                ticklabels = [item.strftime('%Y-%m-%d') for item in list_dist[j+1].index]
                ax2.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
                plt.gcf().autofmt_xdate()
                plt.show()
            j += 1

        return list_ax, list_kl

