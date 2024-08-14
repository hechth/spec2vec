import numpy as np
import pytest
from matchms import Spectrum
from spec2vec import SpectrumDocumentWithLosses


@pytest.fixture
def spectrum() -> Spectrum:
    mz = np.array([10, 20, 30, 40], dtype="float")
    intensities = np.array([0, 0.01, 0.1, 1], dtype="float")
    metadata = {"precursor_mz": 100.0}
    return Spectrum(mz=mz, intensities=intensities, metadata=metadata)

def test_spectrum_document_init_default_with_losses(spectrum: Spectrum):
    """Use default n_decimal and add losses."""
    spectrum_document = SpectrumDocumentWithLosses(spectrum)

    assert spectrum_document.n_decimals == 2, "Expected different default for n_decimals"
    assert len(spectrum_document) == 8
    assert spectrum_document.words == [
        "peak@10.00", "peak@20.00", "peak@30.00", "peak@40.00",
        "loss@60.00", "loss@70.00", "loss@80.00", "loss@90.00"
    ]
    assert next(spectrum_document) == "peak@10.00"


def test_spectrum_document_init_n_decimals_1(spectrum: Spectrum):
    """Use n_decimal=1 and add losses."""
    spectrum_document = SpectrumDocumentWithLosses(spectrum, n_decimals=1)

    assert spectrum_document.n_decimals == 1
    assert len(spectrum_document) == 8
    assert spectrum_document.words == [
        "peak@10.0", "peak@20.0", "peak@30.0", "peak@40.0",
        "loss@60.0", "loss@70.0", "loss@80.0", "loss@90.0"
    ]
    assert next(spectrum_document) == "peak@10.0"

def test_spectrum_document_losses_getter(spectrum: Spectrum):
    """Test losses getter"""
    spectrum_document = SpectrumDocumentWithLosses(spectrum, n_decimals=2)
    assert np.all(spectrum_document.losses.mz == np.array([60., 70., 80., 90.])), \
        "Expected different losses"
    assert np.all(spectrum_document.losses.intensities == spectrum.intensities[::-1]), \
        "Expected different losses"


def test_losses(spectrum: Spectrum):
    loss_mz_from = 10
    loss_mz_to = 30
    expected = spectrum.compute_losses(loss_mz_from, loss_mz_to)

    spectrum_document = SpectrumDocumentWithLosses(spectrum, n_decimals=2, loss_mz_from=loss_mz_from, loss_mz_to=loss_mz_to)
    actual = spectrum_document.losses

    assert actual == expected

