"""A minimal, runnable ML pipeline: load -> prepare -> train -> evaluate.

Runs end to end against a small built-in dataset (sklearn's iris), so it
needs no external data file. Swap `load_data()` for a real data source
when you have one — everything downstream reads (X, y) arrays and doesn't
care where they came from.

Usage:
    python src/pipeline.py
    python src/pipeline.py --plot metrics.png
"""

import argparse

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_data():
    """Load the toy iris dataset. Returns (X, y) as numpy arrays."""
    data = load_iris()
    return data.data, data.target


def prepare_features(X, y, test_size=0.2, random_state=42):
    """Deterministic train/test split.

    Isolated from load/train/evaluate so it can be tested directly: same
    inputs + random_state always produce the same split.
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def train_model(X_train, y_train, random_state=42):
    model = LogisticRegression(max_iter=200, random_state=random_state)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    return {"accuracy": accuracy_score(y_test, predictions)}


def run_pipeline():
    X, y = load_data()
    X_train, X_test, y_train, y_test = prepare_features(X, y)
    model = train_model(X_train, y_train)
    return evaluate_model(model, X_test, y_test)


def plot_results(metrics, output_path):
    """Save a bar chart of the pipeline's metrics. Optional — not run by default."""
    import matplotlib

    matplotlib.use("Agg")  # headless: no display needed, works in CI
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.bar(metrics.keys(), metrics.values())
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    fig.savefig(output_path)
    plt.close(fig)


def build_parser():
    parser = argparse.ArgumentParser(prog="pipeline", description="Run the example ML pipeline")
    parser.add_argument("--plot", help="Path to save a metrics bar chart (optional)")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    metrics = run_pipeline()
    print(metrics)
    if args.plot:
        plot_results(metrics, args.plot)


if __name__ == "__main__":
    main()
