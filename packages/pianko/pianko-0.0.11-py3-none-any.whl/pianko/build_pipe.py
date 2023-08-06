from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def build_pipe(model, **transformers):
    res_transformers = []
    for key, val in transformers.items():
        res_transformers.append((key, val.transformers, val.features))

    preprocess = ColumnTransformer(
        res_transformers
    )

    pipe = Pipeline(
        steps=[
            ('preprocessing', preprocess),
            ('model', model)
        ]
    )
    return pipe