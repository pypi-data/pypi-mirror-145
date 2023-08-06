from io import StringIO

import pandas as pd

from ..core import load_object


def save_dataset(dataset, path):
    dataset.to_csv(path)


def load_dataset(dataset_path: str, index_col=None):
    """
     # TODO: Extend to different types of datasets
    :param model_dataset:
    :return:
    """

    dataset_str = load_object(dataset_path, as_bytes=False)
    dataset_stream = StringIO(dataset_str)
    return pd.read_csv(dataset_stream, index_col=index_col)


def dataset_hash(dataset, project) -> str:
    return str(hash(pd.util.hash_pandas_object(dataset) + project))
