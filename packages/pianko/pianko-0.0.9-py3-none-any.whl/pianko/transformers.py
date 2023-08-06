from abc import abstractmethod
import numpy as np

class Transformer:
    def __init__(self):
        pass

    @abstractmethod
    def transform(self):
        pass

class CatEncoder(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, colname, dictionary):
        # dict with cat_feature_name: new_value
        # dict = {'FeatureA': 1} // encoded value
        series = df[colname]  # Series
        for f_name, new_val in dictionary.items():
            series[series == f_name] = new_val
        df[colname] = series

class ColumnKeeper(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, features_to_keep):
        df.drop(df.columns.difference(features_to_keep), 1, inplace=True)

class ColumnRemover(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, columns_to_remove):
        df.drop(columns=columns_to_remove, inplace=True)

class IQRRemover(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, columns, range_width=1.5):
        for c in columns:
            Q1 = df[c].quantile(0.25)
            Q3 = df[c].quantile(0.75)
            IQR = Q3 - Q1
            df = df[(df[c] < Q1 - range_width * IQR) &
                    (df[c] > Q3 + range_width * IQR)]
        return df

class LogTransformer(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, colnames, offset=0.001):
        for c in colnames:
            df[c] = df[c].map(lambda i: np.log(i) if i > 0 else np.log(i + offset))

class NanCatFiller(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, cols, val):
        for c in cols:
            df[c].fillna(value=val, inplace=True)

class NanNumFiller(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, cols, method):
        if method == 'median':
            for c in cols:
                df[c].fillna(value=df[c].median(), inplace=True)

class NanRemover(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, cols):
        df.drop(columns=cols, inplace=True)

class QuantileRemover(Transformer):
    def __init__(self):
        super().__init__()

    def transform(self, df, cols, percent_low, percent_high):
        for c in cols:
            q_low = df[c].quantile(percent_low)
            q_high = df[c].quantile(percent_high)
            df = df[df[c].between(q_low, q_high)]
            # return df[(df[c] > q_low) & (df[c] < q_high)]
        return df