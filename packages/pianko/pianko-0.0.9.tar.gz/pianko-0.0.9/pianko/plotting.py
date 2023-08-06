import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

def plot_learning_curve(model, X, y, train_sizes, cv, scoring):
    train_sizes, train_scores, validation_scores = learning_curve(
        estimator = model,
        X = X,
        y = y,
        train_sizes = train_sizes,
        cv = cv,
        scoring = scoring
    )
    plt.figure(figsize=(10, 10))
    plt.plot(train_sizes, train_scores.mean(axis=1), label='train err')
    plt.plot(train_sizes, validation_scores.mean(axis=1), label='val error')
    plt.ylabel('Error')
    plt.xlabel('X train size')
    plt.title('Learning curve')
    plt.legend()