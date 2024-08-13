from .SpectrumDocument import SpectrumDocument

class SpectrumDocumentWithLosses(SpectrumDocument):
    def __init__(self, spectrum, n_decimals: int = 2, loss_mz_from: int = 10, loss_mz_to: int = 200):
        self._loss_mz_from = loss_mz_from
        self._loss_mz_to = loss_mz_to
        super().__init__(spectrum, n_decimals)


    def _make_words(self):
        """Create word from peaks (and losses)."""
        peak_words = [f"peak@{mz:.{self.n_decimals}f}" for mz in self._obj.peaks.mz]
        loss_words = [f"loss@{mz:.{self.n_decimals}f}" for mz in self.losses.mz]
        self.words = peak_words + loss_words
        return self


    def _add_weights(self):
        """Add peaks (and loss) intensities as weights."""
        assert self._obj.peaks.intensities.max() <= 1, "peak intensities not normalized"

        peak_intensities = self._obj.peaks.intensities.tolist()
        loss_intensities = self.losses.intensities.tolist()
        self.weights = peak_intensities + loss_intensities
        return self


    @property
    def losses(self):
        """Return losses of original spectrum."""
        return self._obj.compute_losses(self._loss_mz_from, self._loss_mz_to)