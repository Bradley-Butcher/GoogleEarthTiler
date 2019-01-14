from unittest import TestCase
import numpy as np

from Tiler import Tiler


class TestTiler(TestCase):

    def setUp(self):
        self.Tiler = Tiler(18, 256, '2018')
        self.Tiler.tl_tile = [1, 1]

    def test_slice_image(self):
        large_image = np.zeros([2560, 2560, 3])
        sliced_images = self.Tiler.slice_image(large_image)
        self.assertEqual(len(sliced_images['images']), 100)
