import image_cytof
import pytest
import pandas as pd


def test_cytof_read_data():
    name_testfile = './testdata/YZ11.03.21_0269 B1-2_0269B1-2_001_1.txt'
    df_cytof = image_cytof.hyperion_preprocess.cytof_read_data(name_testfile)
    isinstance(df_cytof, pd.core.frame.DataFrame)