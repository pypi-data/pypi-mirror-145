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
# import sktime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# import xgboost as xgb
# from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from sklearn.metrics import recall_score
from sklearn.pipeline import Pipeline
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve, plot_det_curve

from sklearn.model_selection import train_test_split

from sklearn.utils import all_estimators
from sklearn.base import ClassifierMixin
# from sklearn.utils.testing import all_estimators
from sklearn.utils._testing import ignore_warnings




CLASSIFIERS = [est for est in all_estimators() if issubclass(est[1], ClassifierMixin)]


SENSORS_FEATURES = ['sensor_1','sensor_2','sensor_3','sensor_4','sensor_5',
 'sensor_6', 'sensor_7', 'sensor_8', 'sensor_9', 'sensor_10', 'sensor_11', 'sensor_12', 'sensor_13',
 'sensor_14', 'sensor_15', 'sensor_16', 'sensor_17', 'sensor_18', 'sensor_19', 'sensor_20', 'sensor_21', 'sensor_22', 'sensor_23', 'sensor_24']

STAGES = ['baseline', 'absorb', 'pause', 'desorb', 'flush']
TARGET_COL = 'result'
   

def get_plots(model, X_test, y_pred):

    model_attributes = dir(model)


    cfm_plot = plot_confusion_matrix(model, X_test, y_pred)
    cfm_plot.figure_.savefig("Confusion Matrix.png")
    cm = os.path.join(os.getcwd(), 'Confusion Matrix.png')
    mlflow.log_artifact(cm)

    


    if 'predict_proba' in model_attributes:
        try:


            roc_plot = plot_roc_curve(model, X_test, y_pred)
            roc_plot.figure_.savefig("AUC.png")
            auc = os.path.join(os.getcwd(), 'AUC.png')
            mlflow.log_artifact(auc)

            pr_plot = plot_precision_recall_curve(model, X_test, y_pred)
            roc_plot.figure_.savefig("Precision Recall.png")
            pr = os.path.join(os.getcwd(), 'Precision Recall.png')
            mlflow.log_artifact(pr)




            # reliability diagram
            fop, mpv = calibration_curve(y_test, probs, n_bins=10, normalize=True)
            # plot perfectly calibrated
            plt.plot([0, 1], [0, 1], linestyle='--')
            # plot model reliability
            plt.plot(mpv, fop, marker='.')
            plt.savefig('Calibration Curve.png')
            cc = os.path.join(os.getcwd(), 'Calibration Curve.png')
            mlflow.log_artifact(cc)

        except:
            pass
  

    
    if 'feature_importances_' in model_attributes:  
        feat_importances = pd.Series(model.feature_importances_) #, index=X.columns
        feat_importances.nlargest(20).plot(kind='barh')
        plt.savefig('Feature Importance.png')
        fi = os.path.join(os.getcwd(), 'Feature Importance.png')
        mlflow.log_artifact(fi)




def specificity(actual, pred, pos_label=0):
    return recall_score(actual, pred, pos_label=pos_label)




def objective(trial, df, study_name, stage, sensor, use_average, model_mode, suggest, custom_features, remote_tracking):

        mlflow.set_experiment(study_name)

        # artifact_path = mlflow.get_artifact_uri()

        mlflow.start_run()

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



    # with mlflow.start_run():
    

        X = df.drop('result', axis=1)
        y = df['result']

        model = RandomForestClassifier()
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = model.score(X_test, y_test)
        f1 = f1_score(y_test, y_pred, average="macro")
        precision = precision_score(y_test, y_pred, average="macro")
        sensitivity = recall_score(y_test, y_pred, average="macro")
        specificity = recall_score(y_test, y_pred, average="macro", pos_label=0)

        metrics = { 'accuracy': accuracy, 
                    'precision': precision, 
                    'sensitivity': sensitivity,
                    'specificity': specificity,
                    'f1': f1}


       
        get_plots(model, X_test, y_pred)
        mlflow.sklearn.log_model(model, artifact_path=model_name)

            


            
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

        return sensitivity







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
    
    


    study = optuna.create_study(study_name=study_name, direction=direction)
    study.optimize(lambda trial: objective(trial, df, study_name, stage, sensor, use_average, model_mode, suggest, custom_features, remote_tracking), n_trials=n_trials)