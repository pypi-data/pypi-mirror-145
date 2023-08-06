"""

"""
import os
import io
import requests
import numpy as np
import pandas as pd
import xarray as xr
from time import sleep
import traceback
import tethys_utils as tu
from tethysts import Tethys, utils


##########################################################
### Functions for Hilltop data extraction


def convert_site_names(names, rem_m=True):
    """
    Function to convert water usage site names.
    """

    names1 = names.str.replace('[:\.]', '/')
#    names1.loc[names1 == 'L35183/580-M1'] = 'L35/183/580-M1' What to do with this one?
#    names1.loc[names1 == 'L370557-M1'] = 'L37/0557-M1'
#    names1.loc[names1 == 'L370557-M72'] = 'L37/0557-M72'
#    names1.loc[names1 == 'BENNETT K38/0190-M1'] = 'K38/0190-M1'
    names1 = names1.str.upper()
    if rem_m:
        list_names1 = names1.str.findall('[A-Z]+\d*/\d+')
        names_len_bool = list_names1.apply(lambda x: len(x)) == 1
        names2 = names1.copy()
        names2[names_len_bool] = list_names1[names_len_bool].apply(lambda x: x[0])
        names2[~names_len_bool] = np.nan
    else:
        list_names1 = names1.str.findall('[A-Z]+\d*/\d+\s*-\s*M\d*')
        names_len_bool = list_names1.apply(lambda x: len(x)) == 1
        names2 = names1.copy()
        names2[names_len_bool] = list_names1[names_len_bool].apply(lambda x: x[0])
        names2[~names_len_bool] = np.nan

    return names2


def get_hilltop_results(param, station_mtype_corrections=None, quality_codes=True, public_url=None, save_interval_hours=336, modified_date=True, local_tz='Etc/GMT-12', add_ref_as_name=False):
    """

    """
    # import requests
    from hilltoppy import web_service as ws

    try:

        ### Read in parameters
        base_url = param['source']['api_endpoint']
        hts = param['source']['hts']

        datasets = param['source']['datasets']
        processing_code = param['source']['processing_code']
        version = param['source']['version']

        s3_remote = param['remote']

        if isinstance(public_url, str):
            file_remote = {'bucket': s3_remote['bucket'], 'connection_config': public_url}
        else:
            file_remote = s3_remote.copy()

        ### Initalize
        # run_date = pd.Timestamp.today(tz='utc').round('s')
        # # run_date_local = run_date.tz_convert(ts_local_tz).tz_localize(None).strftime('%Y-%m-%d %H:%M:%S')
        # run_date_key = run_date.strftime('%Y%m%dT%H%M%SZ')

        titan = tu.titan.Titan()

        ### Create dataset_ids, check if datasets.json exist on remote, and if not add it
        titan.load_dataset_metadata(datasets)

        titan.load_connection_params(s3_remote['connection_config'], s3_remote['bucket'], public_url, version=version)

        titan.load_run_date(processing_code, save_interval_hours=save_interval_hours)

        ## Reprocess if necessary
        # for i, dataset in enumerate(titan.dataset_list):
        #     print(i)
        #     # if i in [15, 16]:
        #     dataset.update({'spatial_distribution': 'sparse', 'geometry_type': 'Point', 'grouping': 'none'})
        #     if 'result_type' in dataset:
        #         dataset.pop('result_type')
        #     tu.s3.reprocess_datasets(dataset, s3_remote['connection_config'], s3_remote['bucket'], file_remote['connection_config'], threads=20)


        ### Create dataset_ids
        # dataset_list = tu.processing.process_datasets(datasets)

        # run_date_dict = tu.s3.process_run_date(processing_code, dataset_list, remote, save_interval_hours=save_interval_hours)
        # max_run_date_key = max(list(run_date_dict.values()))

        for meas in datasets:
            print('----- Starting new dataset group -----')
            print(meas)

            ### Pull out stations
            stns1 = ws.site_list(base_url, hts, location='LatLong') # There's a problem with Hilltop that requires running the site list without a measurement first...
            stns1 = ws.site_list(base_url, hts, location='LatLong', measurement=meas)
            stns2 = stns1[(stns1.lat > -47.5) & (stns1.lat < -34) & (stns1.lon > 166) & (stns1.lon < 179)].dropna().copy()
            stns2.rename(columns={'SiteName': 'ref'}, inplace=True)

            if add_ref_as_name:
                stns2['name'] = stns2['ref']

            ## Process stations
            stns3 = titan.process_sparse_stations_from_df(stns2, datasets[meas][0]['dataset_id'], file_remote['connection_config'], s3_remote['bucket'], version)
            # stns3 = tu.processing.process_stations_df(stns2, datasets[meas][0]['dataset_id'], file_remote)

            ### Get the Hilltop measurement types
            print('-- Running through station/measurement combos')

            mtypes_list = []
            for s in stns3.ref.values:
                print(s)
                try:
                    meas1 = ws.measurement_list(base_url, hts, s)
                except:
                    print('** station is bad')
                mtypes_list.append(meas1)
            mtypes_df = pd.concat(mtypes_list).reset_index()
            mtypes_df = mtypes_df[mtypes_df.Measurement == meas].rename(columns={'Site': 'ref'})
            mtypes_df = pd.merge(mtypes_df, stns3.to_dataframe().reset_index(), on='ref')

            ## Make corrections to mtypes
            mtypes_df['corrections'] = False

            if station_mtype_corrections is not None:
                for i, f in station_mtype_corrections.items():
                    mtypes_df.loc[(mtypes_df.ref == i[0]) & (mtypes_df.Measurement == i[1]), 'From'] = f
                    mtypes_df.loc[(mtypes_df.ref == i[0]) & (mtypes_df.Measurement == i[1]), 'corrections'] = True

            if not mtypes_df.empty:

                ## Make sure there are no geometry duplicates
                mtypes_df['days'] = (mtypes_df.To - mtypes_df.From).dt.days
                mtypes_df = mtypes_df.sort_values(['geometry', 'days'], ascending=False)
                mtypes_df = mtypes_df.drop_duplicates(['geometry'], keep='first')

                stns3 = stns3.where(stns3.station_id.isin(mtypes_df.station_id), drop=True)

                ##  Iterate through each stn
                print('-- Iterate through each station')
                for i, row in mtypes_df.iterrows():
                    print(row.ref)

                    ## Get the station data
                    stn = stns3.sel(geometry=row.geometry).expand_dims('geometry')

                    ## Get the data out
                    # print('- Extracting data...')

                    bad_error = False
                    timer = 5
                    while timer > 0:
                        # ts_data_list = []

                        try:
                            # sleep(1)
                            if row.Measurement == 'Abstraction Volume':
                                if row['corrections']:
                                    ts_data1 = ws.get_data(base_url, hts, row.ref, row.Measurement, from_date=str(row.From), to_date=str(row.To), agg_method='Total', agg_interval='1 day')[1:]
                                else:
                                    ts_data1 = ws.get_data(base_url, hts, row.ref, row.Measurement, agg_method='Total', agg_interval='1 day')[1:]
                            else:
                                if row['corrections']:
                                    ts_data1 = ws.get_data(base_url, hts, row.ref, row.Measurement, from_date=str(row.From), to_date=str(row.To), quality_codes=quality_codes, dtl_method='half')
                                else:
                                    ts_data1 = ws.get_data(base_url, hts, row.ref, row.Measurement, quality_codes=quality_codes, dtl_method='half')

                            break
                        except requests.exceptions.ConnectionError as err:
                            print(row.ref + ' and ' + row.Measurement + ' error: ' + str(err))
                            timer = timer - 1
                            sleep(30)
                        except ValueError as err:
                            print(row.ref + ' and ' + row.Measurement + ' error: ' + str(err))
                            bad_error = True
                            break
                        except Exception as err:
                            print(str(err))
                            timer = timer - 1
                            sleep(30)

                        if timer == 0:
                            raise ValueError('The Hilltop request tried too many times...the server is probably down')

                    if bad_error:
                        continue

                    ## Pre-process time series data
                    parameter = datasets[meas][0]['parameter']
                    ts_data1 = ts_data1.reset_index().rename(columns={'DateTime': 'time', 'Value': parameter, 'QualityCode': 'quality_code'}).drop(['Site', 'Measurement'], axis=1)

                    if (row['Measurement'] == 'Water Level') and (row['Units'] == 'mm'):
                        ts_data1[parameter] = pd.to_numeric(ts_data1[parameter].values, errors='ignore') * 0.001
                    else:
                        ts_data1[parameter] = pd.to_numeric(ts_data1[parameter].values, errors='ignore')

                    ts_data1['height'] = 0
                    ts_data1['geometry'] = stn['geometry'].values[0]
                    ts_data1['time'] = ts_data1['time'].dt.tz_localize(local_tz).dt.tz_convert('UTC').dt.tz_localize(None)

                    ts_data1.set_index(['geometry', 'height', 'time'], inplace=True)

                    mod_date = pd.Timestamp.today(tz='utc').round('s').tz_localize(None)

                    if modified_date:
                        ts_data1['modified_date'] = mod_date

                    # obs3 = ts_data1.to_xarray()
                    obs4 = xr.combine_by_coords([ts_data1.to_xarray(), stn], data_vars='minimal')

                    ###########################################
                    ## Package up into the data_dict
                    if not ts_data1.empty:
                        if parameter in ['precipitation', 'water_use']:
                            discrete = False
                        else:
                            discrete = True

                        for ds in datasets[meas]:
                            titan.load_results(obs4, ds['dataset_id'], run_date=mod_date, other_closed='right', discrete=discrete)

                    del ts_data1
                    # del obs3
                    del obs4
                    # ts_data = pd.DataFrame()
                    ts_data1 = pd.DataFrame()
                    # obs3 = xr.Dataset()
                    obs4 = xr.Dataset()

                ########################################
                ### Save results and stations
                titan.update_results(30)

    except Exception as err:
        # print(err)
        print(traceback.format_exc())
        tu.misc.email_msg(param['remote']['email']['sender_address'], param['remote']['email']['sender_password'], param['remote']['email']['receiver_address'], 'Failure on Hilltop extraction for ' + base_url + hts, traceback.format_exc(), param['remote']['email']['smtp_server'])

    try:

        ### Aggregate all stations for the dataset
        print('Aggregate all stations for the dataset and all datasets in the bucket')

        titan.update_aggregates()

        print('--Success!')

    except Exception as err:
        # print(err)
        print(traceback.format_exc())
        tu.misc.email_msg(param['remote']['email']['sender_address'], param['remote']['email']['sender_password'], param['remote']['email']['receiver_address'], 'Failure on Hilltop extraction for ' + base_url + hts, traceback.format_exc(), param['remote']['email']['smtp_server'])




###################################################
### Testing

# for k, v in data_dict1.items():
#     print(k)
#     nc1 = xr.load_dataset(utils.read_pkl_zstd(v[0]))
#     print(nc1)




























