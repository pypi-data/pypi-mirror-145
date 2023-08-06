import pickle, datetime, os, struct
import pandas as pd
import numpy as np

from SWaN_accel import config
from SWaN_accel import utils
from SWaN_accel import feature_set
pd.options.mode.chained_assignment = None  # default='warn'

G_VAL = 9.80

col = ["HEADER_TIME_STAMP","X_ACCELERATION_METERS_PER_SECOND_SQUARED",
       "Y_ACCELERATION_METERS_PER_SECOND_SQUARED","Z_ACCELERATION_METERS_PER_SECOND_SQUARED"]

def get_feature_sleep(tdf, sampling):
    X_axes = utils.as_float64(tdf.values[:, 1:])
    result_axes = feature_set.compute_extra_features(X_axes, sampling)
    return result_axes

# def get_df_from_baf(file):
#     # step_log.write(get_log_msg("BAF_TO_DF", str(file) + "\n"))
#     col = ["HEADER_TIME_STAMP", "X_ACCELERATION_METERS_PER_SECOND_SQUARED",
#            "Y_ACCELERATION_METERS_PER_SECOND_SQUARED", "Z_ACCELERATION_METERS_PER_SECOND_SQUARED"]
#     tz = os.path.basename(file).split('.')[2].split('-')[-1]
#
#     hourdiff = int(tz[1:3])
#     minutediff = int(tz[3:])
#
#     if tz[0] == 'M':
#         hourdiff = -int(tz[1:3])
#         minutediff = -int(tz[3:])
#
#     in_file = open(file, "rb")
#     b = in_file.read(20)
#     diction = {}
#     i = 0
#     while len(b) >= 20:
#         t = int.from_bytes(b[0:8], byteorder='big')
#         x = struct.unpack('>f', b[8:12])[0]
#         y = struct.unpack('>f', b[12:16])[0]
#         z = struct.unpack('>f', b[16:20])[0]
#         diction[i] = {'time': t, 'x': x, 'y': y, 'z': z}
#         i = i + 1
#         b = in_file.read(20)
#
#     df = pd.DataFrame.from_dict(diction, "index")
#     df.columns = col
#     df['HEADER_TIME_STAMP'] = pd.to_datetime(df['HEADER_TIME_STAMP'], unit='ms') + \
#                               datetime.timedelta(hours=hourdiff) + datetime.timedelta(minutes=minutediff)
#     df['X_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['X_ACCELERATION_METERS_PER_SECOND_SQUARED'] / G_VAL
#     df['Y_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['Y_ACCELERATION_METERS_PER_SECOND_SQUARED'] / G_VAL
#     df['Z_ACCELERATION_METERS_PER_SECOND_SQUARED'] = df['Z_ACCELERATION_METERS_PER_SECOND_SQUARED'] / G_VAL
#     return df

def main(df=None, file_path=None,sampling_rate=None):

    if(df is None) or (file_path is None) or (sampling_rate is None):
        print("One or all input arguments missing.")
        return

    try:
        import importlib.resources as pkg_resources
    except ImportError:
        # Try backported to PY<37 `importlib_resources`.
        import importlib_resources as pkg_resources

    # trainedModel = pickle.load(open(config.modelPath, "rb"))
    # standardScalar = pickle.load(open(config.scalePath, "rb"))

    trainedModel = pickle.load(pkg_resources.open_binary(__package__,config.modelPath))
    standardScalar = pickle.load(pkg_resources.open_binary(__package__,config.scalePath))

    time_grouper = pd.Grouper(key='HEADER_TIME_STAMP', freq='30s')
    grouped_df = df.groupby(time_grouper)

    print("Computing features...")
    feature_df = pd.DataFrame()
    for name, group in grouped_df:
        if len(group) > sampling_rate * 15:
            op = get_feature_sleep(group, sampling_rate)
            op['HEADER_TIME_STAMP'] = name
            feature_df = pd.concat([feature_df, op], ignore_index=True)

    final_feature_df = feature_df.dropna(how='any', axis=0, inplace=False)
    if final_feature_df.empty:
        print("No feature row computed or remaining after dropping zero rows. So not moving to prediction.")
        return

    final_feature_df.rename(columns={'HEADER_TIME_STAMP': 'START_TIME'}, inplace=True)
    final_feature_df['HEADER_TIME_STAMP'] = final_feature_df['START_TIME']
    final_feature_df['STOP_TIME'] = final_feature_df['START_TIME'] + pd.Timedelta(seconds=30)

    print(datetime.datetime.now().strftime("%H:%M:%S") + " Performing window-level classification...")
    final_feature_df = final_feature_df.dropna()

    subfdata = final_feature_df[config.feature_lis]
    sfdata = standardScalar.transform(subfdata)
    prediction_prob = trainedModel.predict_proba(sfdata)
    prediction = np.argmax(prediction_prob, axis=1)
    p = prediction.reshape((-1, 1))
    final_feature_df["PREDICTED"] = p
    final_feature_df['PROB_WEAR'] = prediction_prob[:, 0]
    final_feature_df['PROB_SLEEP'] = prediction_prob[:, 1]
    final_feature_df['PROB_NWEAR'] = prediction_prob[:, 2]



    final_feature_df.to_csv(file_path, index=False, float_format="%.3f", compression='infer')
    print("Created prediction file:" + file_path)

    return


# if __name__ == "__main__":
#     inPath = 'C:/Users\BINOD\Documents/tmp\missing_watch_data_binod\data-watch/' \
#              '2020-07-24/13-EDT\AndroidWearWatch-AccelerationCalibrated-NA.020000000000-AccelerationCalibrated.2020-07-24-13-19-58-165-M0400.sensor.baf'
#     idf = get_df_from_baf(inPath)
#     fPath = 'C:/Users\BINOD\Documents/tmp\missing_watch_data_binod\data-watch/' \
#              '2020-07-24/13-EDT/tmp.csv'
#     samp_rate = 50
#     main(idf,fPath,samp_rate)
