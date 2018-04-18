import pandas as pd

import module.constant as const


class FilterData:

    @staticmethod
    def clear_data(district: str):
        dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
        data_td = pd.read_csv(const.path_data_input + "distric_lima_{}_complete_all.csv".format(district),
                              sep="|", parse_dates={'DAY': ['_source.FECHA_OPER']}, squeeze=True)

        data_tc = pd.read_csv(const.path_data_input + "distric_lima_{}_complete_tc_all.csv".format(district),
                              sep="|", parse_dates={'DAY': ['_source.FECHA_OPER']}, squeeze=True)

        data_all = data_td.append(data_tc)
        data_filter = data_all[["DAY", "_source.CLIENTE1", "_source.CODGIRO", "_source.TRX", "_source.MONTO"]]
        # Sort by day
        data_sort = data_filter.sort_values("DAY")
        data_sort['DAY'] = pd.to_datetime(data_sort['DAY'].dt.strftime('%Y-%m-%d'))
        data_result = (data_sort.rename(columns={'_source.CLIENTE1': 'CLIENT',
                                                 '_source.CODCLIAINGRESO': 'INGRESO_CLIENTE',
                                                 '_source.MONTO': 'AMOUNT', '_source.CODGIRO': 'CATEGORY',
                                                 '_source.TRX': 'TRX'}))

        data_filter_all = pd.DataFrame()
        for category in const.list_categories:
            df_filter = data_result[data_result['CATEGORY'] == category]
            df_filter = df_filter[['DAY', 'TRX', 'AMOUNT']]
            data_filter_all.append(df_filter)

        data_result = data_filter_all.groupby(['DAY']).sum()
        data_result.to_csv(const.path_data_input + "district_lima_SJL_filter.csv", sep="|")


    @staticmethod
    def week_windows(data: pd.DataFrame, field: str, windows: int) -> pd.DataFrame:
        ds_length = len(data.values)
        list_result = list()
        for a in range(ds_length):
            if a + windows > ds_length:
                list_data = data.values[a:ds_length]
                repeat = a + windows - ds_length
                list_result.append(float((np.sum(list_data) + repeat * data.values[a]) / windows))
            else:
                list_data = data.values[a:a + windows]
                list_result.append(float(np.sum(list_data) / windows))
        return pd.DataFrame({field: list_result}, index=data.index)

