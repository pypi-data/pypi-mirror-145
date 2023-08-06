#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import km3compass as kc
import matplotlib.pyplot as plt


class test_summary_plot(unittest.TestCase):
    def setUp(self):
        self.reader = kc.readerCSK("tests/DOM_0801.csk")

    def test_plot_raw_results(self):
        fig = kc.plot_raw_results(self.reader.df)
        assert isinstance(fig, plt.Figure)

    def test_append_AHRS(self):
        kc.append_AHRS(self.reader.df)

    def test_append_spherical(self):
        kc.append_spherical(self.reader.df)
