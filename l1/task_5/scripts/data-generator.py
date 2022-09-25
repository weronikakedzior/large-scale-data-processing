"""Script for generation of artificial datasets."""

import argparse
import pickle
from typing import List
from typing import Tuple
from sklearn.datasets import make_regression


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--num-samples',
        required=True,
        help='Number of samples to generate',
        type=int,
    )
    parser.add_argument(
        '--out-dir',
        required=True,
        help='Name of directory to save generated data',
        type=str,
    )

    return parser.parse_args()


def generate_data(num_samples: int) -> Tuple[List[float], List[float]]:
    """Generates datasets."""
    X, y = make_regression(n_samples=num_samples, n_features=1, noise=0.2)
    return list(X.flatten()), list(y)


def main() -> None:
    """Main."""
    args = vars(get_args())
    data_len = args['num_samples']
    data = generate_data(data_len)
    directory = args['out_dir']
    with open(directory + "/data_" + str(data_len), 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    main()
