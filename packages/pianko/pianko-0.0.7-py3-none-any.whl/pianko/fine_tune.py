from pianko.build_pipe import build_pipe
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

def fine_tune(models, X_train, Y_train, strategy, search_params, transformers):
    fine_tune_res = {}

    for name, model, param_grid in models:
        print(search_params)
        pipe = build_pipe(model, **transformers)

        if strategy == 'GridSearchCV':
            search_res = GridSearchCV(
                estimator=pipe,
                param_grid=param_grid,
                **search_params
            )

        elif strategy == 'RandomizedSearchCV':
            search_res = RandomizedSearchCV(
                pipe,
                param_grid,
                **search_params
            )
        search_res.fit(X_train, Y_train)
        fine_tune_res[name] = search_res

    return dict(sorted(fine_tune_res.items(), reverse=True, key=lambda x: x[1].best_score_))