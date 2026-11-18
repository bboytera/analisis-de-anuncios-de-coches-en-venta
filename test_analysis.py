import unittest
import numpy as np
import pandas as pd
from analysis import prepare_data, without_outliers, summarize_types

class AnalysisRegressionTests(unittest.TestCase):
    def test_scalar_imputation_and_zero_age(self):
        raw = pd.DataFrame({'model':['a','a','b'],'cylinders':[4,np.nan,np.nan],
            'model_year':[2020]*3,'odometer':[10,20,30], 'paint_color':['red',None,None],
            'is_4wd':[1,None,0],'date_posted':['2020-01-01']*3,'price':[10,20,30],'days_listed':[1,2,3]})
        result = prepare_data(raw)
        self.assertEqual(result.cylinders.tolist(),[4,4,4])
        self.assertEqual(result.paint_color.tolist(),['red','unknown','unknown'])
        self.assertTrue(result.annual_mileage.isna().all())

    def test_iqr_is_independent(self):
        data = pd.DataFrame({'price':[10,11,12,13,1000], 'odometer':[1000,10,11,12,13]})
        self.assertEqual(without_outliers(data,'price').index.tolist(),[0,1,2,3])
        self.assertEqual(without_outliers(data,'odometer').index.tolist(),[1,2,3,4])

    def test_popularity_uses_count(self):
        data = pd.DataFrame({'type':['cheap']*51+['costly']*50+['rare'],'price':[1]*51+[100]*50+[1000]})
        self.assertEqual(summarize_types(data).index.tolist(),['cheap','costly'])

if __name__ == '__main__':
    unittest.main()
