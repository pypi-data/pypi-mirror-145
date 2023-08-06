import pandas as pd
import subprocess



def load_validated_breath_dataset():


    url = 'https://drive.google.com/file/d/1LUBsw5nIW_VSDGucxeudCrzDy4ntC1gW/view?usp=sharing'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]


    return pd.read_csv(url, index_col=0)


def get_data(data='validated_breath_data'):
    """Loads data into a dataframe

    Args:
        data (str, optional): name of data to be loaded. Defaults to 'validated_breath_data'.

    Returns:
        pandas dataframe: 
    """


    if data == 'validated_breath_data':
        # url = 'https://drive.google.com/file/d/1LUBsw5nIW_VSDGucxeudCrzDy4ntC1gW/view?usp=sharing'
        url = 'https://drive.google.com/file/d/1CJ3e8NKS2KgUidZMLBFP0ktq2_y87eHb/view?usp=sharing'
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]


    elif data == 'lab_data':
        url = 'https://drive.google.com/file/d/1dz3vrsOLbqiedSIslxbioUhS82MB96WS/view?usp=sharing' 
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]


    elif data == 'repeat_experiment':
        url = 'https://drive.google.com/file/d/1r83aSt_LJ-nGVLXohFKbk8oUlGwtJ4Gi/view?usp=sharing'
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]



    elif data == 'handheld_data':
        url = 'https://drive.google.com/file/d/1YZ6PDQpT9QkeVBLuRK6hThgaI54av6sf/view?usp=sharing'
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]


    else:
        return 'Data not available'


    return pd.read_csv(url, index_col=0)