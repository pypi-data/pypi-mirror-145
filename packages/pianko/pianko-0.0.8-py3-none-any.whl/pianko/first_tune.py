from pianko.build_pipe import build_pipe
from sklearn.model_selection import cross_val_score
from numpy import mean

def first_tune(models, scoring, X_train, Y_train, transformers):
    res = dict()
    for name, model in models:
        model_pipeline = build_pipe(model, **transformers)
        cv_scores = cross_val_score(model_pipeline, X_train, Y_train, scoring=scoring)
        res[name] = cv_scores

    return dict(sorted(res.items(), reverse=True, key=lambda x: mean(x[1])))