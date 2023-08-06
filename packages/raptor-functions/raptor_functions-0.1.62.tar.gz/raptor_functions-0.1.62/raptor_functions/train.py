# Importing the Packages:
import optuna
import argparse
import joblib
import tempfile
import pandas as pd
from sklearn import linear_model
from sklearn import datasets
from sklearn import model_selection
import sklearn.ensemble as ensemble
import mlflow
import random
import os
from pycaret.classification import *
# import sktime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.metrics import recall_score
# from raptor_functions.feature_selection import get_train_features
from sklearn.pipeline import Pipeline
# from sktime.classification.compose import ColumnEnsembleClassifier
# from sktime.classification.interval_based import TimeSeriesForestClassifier
# from sktime.classification.dictionary_based import BOSSEnsemble
# # from sktime.classification.shapelet_based import MrSEQLClassifier
# from sktime.transformations.panel.compose import ColumnConcatenator
from sklearn.model_selection import train_test_split
# from sktime.datatypes._panel._convert import (
#     from_multi_index_to_nested,
#     from_nested_to_multi_index,
# )

# from raptor_functions.raptor_data import load_validated_breath_dataset

# df = load_validated_breath_dataset()



SENSORS_FEATURES = ['sensor_1','sensor_2','sensor_3','sensor_4','sensor_5',
 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13',
 'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23', 'sensor_24']

STAGES = ['baseline', 'absorb', 'pause', 'desorb', 'flush']
TARGET_COL = 'result'

# artifact_path = 's3://raptor-mlflow-data/mlartifacts/1/83318437749c4e59a4950f55a98b2ad6/artifacts'
# artifact_path = 's3://raptor-mlflow-data'

def aslist(x):
    """Checks and ensures variable is a list

    Args:
        x (str or list): 

    Returns:
        list: 
    """

    if isinstance(x, list):
        return x
    else:
        return [x]





def get_stages(stages='pause', N_STAGES=None):
    """get the stages of experiment to be used for model training

    Args:
        stages (str or list, optional): Can take any of ('baseline', 'absorb', 'pause', 'desorb', 'flush') as a str or combination as a list. 
                                        Can also take str 'all' for all stages and 'random' for random stage or stages. Defaults to 'pause'.
        N_STAGES (int, optional): if 'random' is chosen for stages, the number of stages to use. Defaults to None.

    Returns:
        list: a list of stages to be used for training
    """

    if stages== 'pause':
        return aslist('pause')
    elif stages == 'all':
        return aslist(STAGES)
    elif stages=='random':
        return np.random.choice(STAGES, N_STAGES, False).tolist()
    else:
        return stages




def get_sensors(sensors='12', N_SENSORS=None):
    """_summary_

    Args:
        sensors (str, optional): Can take any of ('sensor_1', 'sensor_2', 'sensor_3'.....'sensor_24') as a str or combination as a list. 
                                        Can also take str '24' for all sensors, '12' for 1st 12 sensors, '12r' for last 12 sensors and 'random' for random sensor or sensors. Defaults to '12'.
        N_SENSORS (_type_, optional): if 'random' is chosen for sensors, the number of sensors to use. Defaults to None.

    Returns:
        list: a list of sensors to be used for training
    """

    if sensors=='24':
        return SENSORS_FEATURES
    elif sensors=='12':
        return SENSORS_FEATURES[:12]
    elif sensors=='12r':
        return SENSORS_FEATURES[-12:]
    elif sensors=='random':
        return np.random.choice(SENSORS_FEATURES, N_SENSORS, False).tolist()
    else:
        return sensors

def get_train_features(df, sensor='12', stage='pause', use_average = False):
    
    """Selects the features to be used for model training

    Args:
        df (pandas dataframe): dataframe of cyclic sensor data
        sensor (str, optional): Can take any of ('sensor_1', 'sensor_2', 'sensor_3'.....'sensor_24') as a str or combination as a list. 
                                 Can also take str '24' for all sensors, '12' for 1st 12 sensors, '12r' for last 12 sensors and 'random' for random sensor or sensors. Defaults to '12'.        stage (str, optional): _description_. Defaults to 'pause'.
        stage (str or list, optional): Can take any of ('baseline', 'absorb', 'pause', 'desorb', 'flush') as a str or combination as a list. 
                                        Can also take str 'all' for all stages and 'random' for random stage or stages. Defaults to 'pause'.
        use_average (bool, optional): if True, uses average of stages selected. Defaults to False.


    Returns:
        data(pandas dataframe): _description_
    """

    target_col='result'

    N_SENSORS = random.randint(1,len(SENSORS_FEATURES))
    N_STAGES = random.randint(1,len(STAGES))

    stages_to_use = get_stages(stage, N_STAGES)
    sensors_to_use = get_sensors(sensor, N_SENSORS)


    if use_average:
        data = df.groupby(['measurement_stage', 'result', 'exp_unique_id']).mean().loc[stages_to_use].reset_index()[sensors_to_use+[target_col]]
        return data, sensors_to_use, stages_to_use

    else:
        data = df.loc[df['measurement_stage'].isin(stages_to_use)][sensors_to_use+[target_col]]
        return data, sensors_to_use, stages_to_use


# def log_artifact(filepath):
#     print('fp: ', filepath)
#     with tempfile.TemporaryDirectory() as tmp:
#         path = os.path.join(tmp, filepath)
#         print('tp: ', path)
#         mlflow.log_artifact(path)        

def get_plots(model):

    model_attributes = dir(model)

    plot_model(model, plot = 'confusion_matrix', save=True)
    cm = os.path.join(os.getcwd(), 'Confusion Matrix.png')
    mlflow.log_artifact(cm)
    # log_artifact(cm)

    plot_model(model, plot = 'class_report', save=True) 
    cr = os.path.join(os.getcwd(), 'Class Report.png')
    mlflow.log_artifact(cr)  
    # log_artifact(cr)
    


    if 'predict_proba' in model_attributes:
        try:
            plot_model(model, plot = 'auc', save=True)
            auc = os.path.join(os.getcwd(), 'AUC.png')
            mlflow.log_artifact(auc) 

            plot_model(model, plot = 'pr', save=True) 
            pr = os.path.join(os.getcwd(), 'Precision Recall.png')
            mlflow.log_artifact(pr)

            plot_model(model, plot = 'calibration', save=True) 
            cc = os.path.join(os.getcwd(), 'Calibration Curve.png')
            mlflow.log_artifact(cc)
        except:
            pass
  

    
    if 'feature_importances_' in model_attributes:  
        plot_model(model, plot = 'feature', save=True)  
        fi = os.path.join(os.getcwd(), 'Feature Importance.png')
        mlflow.log_artifact(fi)

def specificity(actual, pred, pos_label=0):
    return recall_score(actual, pred, pos_label=pos_label)


def objective(trial, df, study_name, stage, sensor, use_average, model_mode, suggest, custom_features):

        mlflow.set_experiment(study_name)

        # artifact_path = mlflow.get_artifact_uri()

        mlflow.start_run()
    # with mlflow.start_run():
        if suggest:
            stage = trial.suggest_categorical("stages", ["pause", "all", 'random'])
            sensor = trial.suggest_categorical("sensor", ["24", "12", '12r','random'])
            use_average = trial.suggest_categorical("use_average", [True, False])
            model_mode = trial.suggest_categorical("model_mode", ["random", "compare"])



        if custom_features:
            data = df
        else:
            data, sensors_to_use, stages_to_use = get_train_features(df, sensor=sensor, stage=stage, use_average=use_average)
        # except:
        #     data = df
        #     sensors_to_use, stages_to_use = df.columns, None


        clf = setup(data, target = 'result', silent=True, log_plots=True, experiment_name=study_name, preprocess=False)
                                                                    # log_experiment=True,
        add_metric('specificity', 'Specificity', specificity)
        remove_metric('MCC')
        remove_metric('Kappa')

        MODELS = dict(models()['Name'])



        if model_mode == 'random':

            # MODELS = models().index.tolist()
            model_id = trial.suggest_categorical("model", list(MODELS.keys()))
            model_name = MODELS[model_id]
            model = create_model(model_id)
            predict_model(model)
            metrics = pull().iloc[:,1:]
            keys = metrics.columns
            values = metrics.values[0]
            metrics = dict(zip(keys, values))


            get_plots(model)
            mlflow.sklearn.log_model(model, artifact_path=model_name)
           
        elif model_mode == 'xgb':

            model = create_model('xgb')
            predict_model(model)
            metrics = pull().iloc[:,1:]
            keys = metrics.columns
            values = metrics.values[0]
            metrics = dict(zip(keys, values))
            

            get_plots(model)
            mlflow.sklearn.log_model(model, artifact_path=model_name)
                    
        else:

            model = compare_models()

            model_name = model.__class__.__name__
            predict_model(model)
            metrics = pull().iloc[:,1:]
            keys = metrics.columns
            values = metrics.values[0]
            metrics = dict(zip(keys, values))


            get_plots(model)
            mlflow.sklearn.log_model(model, artifact_path=model_name)

            


        
        # print(mlflow.get_artifact_uri())
        
        model_params = model.get_params()
        


        mlflow.log_metrics(metrics)

        try:
            mlflow.set_tag('sensor_cols', sensors_to_use)
            mlflow.set_tag('stage', stages_to_use)
            mlflow.set_tag('use_average', use_average)
        except:
            pass

        mlflow.set_tag('model_name', model_name)
        mlflow.set_tag('model_params', model_params)
        
        mlflow.set_tag('model_mode', model_mode)
        mlflow.set_tag('suggest', suggest)

        print('Click on this link to track experiments: ', mlflow.get_tracking_uri())
        mlflow.end_run()







def train_experiments(df, study_name='raptor', direction='maximize', stage='pause', sensor='12', use_average=False, model_mode='random', n_trials=5, custom_features=False, suggest=False, remote_tracking=True):
    """trains several models during different trials and logs them. Experiemnt can be tracked on "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"


    Args:
        df (pandas dataframe): dataframe of cyclic sensor data to be used for training
        study_name (str, optional): optuna study name to use. Defaults to 'raptor'.
        direction (str, optional): dirtection of objective. Defaults to 'maximize'.
        stage (str or list, optional): Can take any of ('baseline', 'absorb', 'pause', 'desorb', 'flush') as a str or combination as a list. 
                                        Can also take str 'all' for all stages and 'random' for random stage or stages. Defaults to 'pause'.        sensor (str, optional): _description_. Defaults to '12'.
        use_average (bool, optional): if True, uses average of stages selected. Defaults to False.
        model_mode (str, optional): _description_. Defaults to 'random'.
        n_trials (int, optional): number of times to run experiments. Defaults to 5.
        suggest (bool, optional): if True, suggest features, stage, model mode to use for training. Defaults to False.
    """    
    
    if remote_tracking:
        mlflow.set_tracking_uri(
        # "http://ec2-13-40-214-238.eu-west-2.compute.amazonaws.com:5000/"
        # "http://ec2-13-40-86-186.eu-west-2.compute.amazonaws.com:5000/"
        "http://ec2-3-10-175-206.eu-west-2.compute.amazonaws.com:5000/"
        )
    else:
        mlflow.set_tracking_uri("http://localhost:5000")
    #     uri = os.path.join(os.getcwd(), "sqlite:///mlruns.db")
    #     mlflow.set_tracking_uri(uri)


    # Initialize client
    # client = MlflowClient()

    # print(mlflow.get_artifact_uri())
    # print(mlflow.get_tracking_uri())

    study = optuna.create_study(study_name=study_name, direction=direction)
    study.optimize(lambda trial: objective(trial, df, study_name, stage, sensor, use_average, model_mode, suggest, custom_features), n_trials=n_trials)

    # return mlflow.get_artifact_uri(), mlflow.get_tracking_uri()
        


# if __name__ == '__main__':

#     args = argparse.ArgumentParser()


#     # stage = trial.suggest_categorical("stages", ["pause", "all", 'random'])
#     # sensor = trial.suggest_categorical("sensor", ["24", "12", '12r','random'])
#     # use_average = trial.suggest_categorical("use_average", [True, False])
#     # model_mode = trial.suggest_categorical("model_mode", ["random", "compare"])

#     # default_config_path = os.path.join("config", "params.yaml")
#     args.add_argument("--stage", default='pause')
#     args.add_argument("--sensor", default='12')

#     args.add_argument("--use-average", default=True)
#     args.add_argument("--model-mode", default='random')
#     args.add_argument("--suggest", default=False)
#     args.add_argument("--n_trials", default=5)


#     parsed_args = args.parse_args()

#     stage = parsed_args.stage
#     sensor = parsed_args.sensor
#     use_average = parsed_args.use_average
#     model_mode = parsed_args.model_mode
#     suggest = parsed_args.suggest
#     n_trials = int(parsed_args.n_trials)


    # study = optuna.create_study(study_name='raptor', direction="maximize")
    # study.optimize(lambda trial: objective(trial, stage, sensor, use_average, model_mode, suggest), n_trials=n_trials)
