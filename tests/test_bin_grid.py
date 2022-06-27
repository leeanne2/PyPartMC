####################################################################################################
# This file is a part of PyPartMC licensed under the GNU General Public License v3 (LICENSE file)  #
# Copyright (C) 2022 University of Illinois Urbana-Champaign                                       #
# Authors: https://github.com/open-atmos/PyPartMC/graphs/contributors                              #
####################################################################################################

import numpy as np
import PyPartMC as ppmc


class TestBinGrid:
    @staticmethod
    def test_ctor():
        # arrange
        pass

        # act
        sut = ppmc.BinGrid(123, "log", 1, 100)

        # assert
        assert sut is not None

    @staticmethod
    def test_len():
        # arrange
        grid_size = 666
        sut = ppmc.BinGrid(grid_size, "log", 1, 100)

        # act
        size = len(sut)

        # assert
        assert size == grid_size

    @staticmethod
    def test_bin_edges_len():
        # arrange
        grid_size = 100
        sut = ppmc.BinGrid(grid_size, "log", 1, 100)

        # act
        edges = sut.edges

        # assert
        assert grid_size + 1 == len(edges)

    @staticmethod
    def test_bin_edges_values():
        # arrange
        n_bins = 10
        left_edge = 1
        right_edge = 100
        sut = ppmc.BinGrid(n_bins, "log", left_edge, right_edge)

        # act
        edges = sut.edges

        # assert
        np.testing.assert_array_almost_equal(
            np.logspace(np.log10(left_edge), np.log10(right_edge), n_bins+1),
            edges
        )

    @staticmethod
    def test_bin_centers_len():
        # arrange
        grid_size = 44
        sut = ppmc.BinGrid(grid_size, "log", 1, 100)

        # act
        centers = sut.centers

        # assert
        assert grid_size == len(centers)

    @staticmethod
    def test_bin_centers_values():
        # arrange
        n_bins = 10
        left_edge = 1
        right_edge = 100
        sut = ppmc.BinGrid(n_bins, "log", left_edge, right_edge)

        # act
        centers = sut.centers

        # assert
        np.testing.assert_array_almost_equal(
            np.logspace(np.log10(left_edge), np.log10(right_edge), 2*n_bins+1)[1:-1:2],
            centers
        )

    @staticmethod
    def test_invalid_grid():
        grid_size = 100
        try:
            _ = ppmc.BinGrid(grid_size, "X", 1, 100)
        except ValueError as error:
            assert str(error) == "Invalid grid spacing."

    @staticmethod
    def test_histogram_1d():
        n_data = 1000
        grid = ppmc.BinGrid(100,"linear",0,1000)
        vals = np.random.random(n_data)*1000
        weights = np.ones(n_data)
        data = ppmc.histogram_1d(grid, vals, weights)
        hist,bin_edges = np.histogram(vals,bins=grid.edges)
        np.testing.assert_array_almost_equal(data,hist/(bin_edges[1]-bin_edges[0]))

    @staticmethod
    def test_histogram_2d():
        n_data = 1000
        x_grid = ppmc.BinGrid(15,"linear",0,1000)
        y_grid = ppmc.BinGrid(12,"linear",0,500)
        x_vals = np.random.random(n_data)*1000
        y_vals = np.random.random(n_data)*500
        weights = np.random.random(n_data)
        data = ppmc.histogram_2d(x_grid, x_vals, y_grid, y_vals, weights)
        data_numpy, bin_edges_x, bin_edges_y = np.histogram2d(x_vals,y_vals,
             bins=[x_grid.edges,y_grid.edges],weights=weights)
        cell_size = (x_grid.edges[1]-x_grid.edges[0])*(y_grid.edges[1]-y_grid.edges[0])
        np.testing.assert_array_almost_equal(np.array(data),data_numpy/cell_size,decimal=15)
