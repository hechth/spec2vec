from gensim.models import KeyedVectors
import json
import numpy as np
import scipy.sparse
from typing import Union


class Word2VecLight:
    """
    A lightweight version of :class:`~gensim.models.Word2Vec`. The objects of this class follow the interface of the
    original :class:`~gensim.models.Word2Vec` to the point necessary to calculate Spec2Vec scores. The model cannot be
    used for further training.
    """

    def __init__(self, model: dict, weights: Union[np.ndarray, scipy.sparse.csr_matrix, scipy.sparse.csc_matrix]):
        """

        Parameters
        ----------
        model:
            A dictionary containing the model's metadata.
        weights:
            A numpy array or a scipy sparse matrix containing the model's weights.
        """
        self.wv = self._KeyedVectorsBuilder().from_dict(model).with_weights(weights).build()

    class _KeyedVectorsBuilder:
        def __init__(self):
            self.weights = None
            self.key_to_index = None
            self.index_to_key = None
            self.vector_size = None

        def build(self) -> KeyedVectors:
            keyed_vectors = KeyedVectors(self.vector_size)
            keyed_vectors.vector_size = self.vector_size
            keyed_vectors.index_to_key = self.index_to_key
            keyed_vectors.key_to_index = self.key_to_index
            keyed_vectors.vectors = self.weights
            return keyed_vectors

        def from_dict(self, dictionary: dict):
            self.vector_size = dictionary["vector_size"]
            self.index_to_key = dictionary["index_to_key"]
            self.key_to_index = dictionary["key_to_index"]
            return self

        def with_weights(self, weights: Union[np.ndarray, scipy.sparse.csr_matrix, scipy.sparse.csc_matrix]):
            self.weights = weights
            return self


def import_model(model_file, weights_file) -> Word2VecLight:
    """
    Read a lightweight version of a :class:`~gensim.models.Word2Vec` model from disk.

    Parameters
    ----------
    model_file:
        A path of json file to load the model.
    weights_file:
        A path of npy or npz file to load the model's weights.

    Returns
    -------
    :class:`~spec2vec.serialization.model_importing.Word2VecLight` – a lightweight version of a
    :class:`~gensim.models.Word2Vec`
    """
    with open(model_file, "r") as f:
        model: dict = json.load(f)

    weights = load_weights(model, weights_file)
    return Word2VecLight(model, weights)


def load_weights(model, weights_file):
    weights = np.load(weights_file, allow_pickle=False)

    if not (model["__numpys"] or model["__scipys"] or model["__ignoreds"]):
        raise ValueError("The model's weights format is undefined.")
    elif model["__scipys"]:
        sparse_array_builder = {"csr_matrix": scipy.sparse.csr_matrix, "csc_matrix": scipy.sparse.csc_matrix}
        weights = sparse_array_builder[model["__weights_format"]](weights)

    return weights
