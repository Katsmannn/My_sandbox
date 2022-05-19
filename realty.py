# Выборка из файла INPUT_FILE объектов, которые были проданы более одого раза

import dask.dataframe as dd


INPUT_FILE = 'pp-complete.csv'
RESULT_FILE = 'sales_gt_1.csv'

realty_list = dd.read_csv(
    INPUT_FILE,
    names=[
        'identifier',
        'price',
        'date_of_transfer',
        'postcode',
        'property_type',
        'old_new',
        'duration',
        'paon',
        'saon',
        'street',
        'locality',
        'town',
        'district',
        'county',
        'ppd_category',
        'status',
    ],
    dtype={
        'paon': str,
        'saon': str
    },
    na_filter=False,
)
realty_list = realty_list.assign(
    address=realty_list['paon'] + ', '
    + realty_list['saon'] + ', '
    + realty_list['street'] + ', '
    + realty_list['locality'] + ', '
    + realty_list['town'] + ', '
    + realty_list['district'] + ', '
    + realty_list['county']
).address
realty_list = realty_list.groupby(realty_list).count()
realty_list = realty_list[
    realty_list > 1
].compute().to_csv(
    RESULT_FILE, single_file=True
)
