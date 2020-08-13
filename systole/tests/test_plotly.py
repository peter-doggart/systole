# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

import pandas as pd
import numpy as np
import unittest
from unittest import TestCase
from systole.plotly import plot_raw, plot_shortLong, plot_ectopic, \
    plot_subspaces, plot_frequency, plot_nonlinear, plot_timedomain
from systole import import_ppg, import_dataset
from systole.utils import simulate_rr

rr = simulate_rr()
ppg = import_ppg()
signal_df = pd.DataFrame({'time': np.arange(0, len(ppg[0]))/75,
                          'ppg': ppg[0]})


class TestInteractive(TestCase):

    def test_plot_raw(self):
        """Test plot_raw function"""
        plot_raw(signal_df)
        plot_raw(signal_df.ppg.to_numpy())
        ecg_df = import_dataset()[:20*2000]
        plot_raw(ecg_df, type='ecg')
        plot_raw(ecg_df.ecg.to_numpy(), type='ecg', sfreq=2000)

    def test_plot_shortLong(self):
        """Test plot_shortLong function"""
        plot_shortLong(rr)
        with self.assertRaises(ValueError):
            plot_shortLong(rr=None, artefacts=None)

    def test_plot_ectopic(self):
        """Test plot_ectopic function"""
        plot_ectopic(rr)
        with self.assertRaises(ValueError):
            plot_ectopic(rr=None, artefacts=None)

    def test_plot_subspaces(self):
        """Test nnX function"""
        plot_subspaces(rr)

    def test_plot_frequency(self):
        """Test nnX function"""
        plot_frequency(rr)

    def test_plot_nonlinear(self):
        """Test nnX function"""
        plot_nonlinear(rr)

    def test_plot_timedomain(self):
        """Test nnX function"""
        plot_timedomain(rr)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
