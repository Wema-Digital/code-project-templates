import numpy as np

from src.pipeline import load_data, prepare_features, run_pipeline


def test_prepare_features_is_deterministic():
    X, y = load_data()

    X_train_1, X_test_1, y_train_1, y_test_1 = prepare_features(X, y)
    X_train_2, X_test_2, y_train_2, y_test_2 = prepare_features(X, y)

    assert np.array_equal(X_train_1, X_train_2)
    assert np.array_equal(y_train_1, y_train_2)
    assert np.array_equal(X_test_1, X_test_2)
    assert np.array_equal(y_test_1, y_test_2)


def test_prepare_features_split_sizes():
    X, y = load_data()

    X_train, X_test, y_train, y_test = prepare_features(X, y, test_size=0.2)

    assert len(X_train) + len(X_test) == len(X)
    assert len(y_train) + len(y_test) == len(y)
    assert len(X_test) == round(len(X) * 0.2)


def test_run_pipeline_returns_accuracy():
    metrics = run_pipeline()

    assert "accuracy" in metrics
    assert 0.0 <= metrics["accuracy"] <= 1.0
