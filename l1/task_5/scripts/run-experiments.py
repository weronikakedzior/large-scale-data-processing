"""Script for time measurement experiments on linear regression models."""

import argparse
import pickle
import time
from typing import List
from typing import Tuple
from typing import Type

import pandas as pd
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plot

import lr


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--datasets-dir',
        required=True,
        help='Name of directory with generated datasets',
        type=str,
    )

    return parser.parse_args()


def run_experiments(
    models: List[Type[lr.base.LinearRegression]],
    datasets: List[Tuple[List[float], List[float]]],
) -> pd.DataFrame:
    """Runs experiments for all models and datasets."""
    data = pd.DataFrame()
    for model in models:
        for dataset in datasets:
            x = dataset[0]
            y = dataset[1]
            start_time = time.time()
            model.fit(model, x, y)
            t = time.time() - start_time
            d = {"model": model.__name__, "data_size": len(x), "time": t}
            data = data.append(d, ignore_index=True)
    return data


def make_plot(results: pd.DataFrame) -> None:
    """Makes time plots."""
    fig, ax = plot.subplots()
    for key, grp in results.groupby('model'):
        ax = grp.plot(ax=ax, kind='line', x='data_size', y='time', label=key,
                      style='.-', title='Execution time')
    plot.savefig('./plots/plot1.png')


def main() -> None:
    """Runs script."""
    args = vars(get_args())

    models = [
        lr.LinearRegressionNumpy,
        lr.LinearRegressionProcess,
        lr.LinearRegressionSequential,
        lr.LinearRegressionThreads,
    ]
    datasets = []
    dir = args['datasets_dir']
    data_files = [f for f in listdir(dir) if isfile(join(dir, f))]
    for file in data_files:
        with open(dir + "/" + file, "rb") as f:
            dataset = pickle.load(f)
            datasets.append(dataset)
    results = run_experiments(models, datasets)
    print(results)
    make_plot(results)


if __name__ == '__main__':
    main()
