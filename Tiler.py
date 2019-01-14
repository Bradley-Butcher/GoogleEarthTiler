import os
import math
from scipy.ndimage import imread
from scipy.misc import imresize, imsave
from pyproj import Proj, transform


class Tiler:
    """Given an image and associated coordinates, return/save array of tiled images + tile IDs"""

    def __init__(self, image_filename, zoom_to, tile_input_size, tile_output_size, tile_suffix):
        self.zoom_to = zoom_to
        self.tile_size = tile_input_size
        self.tile_output_size = tile_output_size
        self.tl_tile = None
        self.tile_suffix = tile_suffix
        self.image = imread(image_filename)

    def __crop_tl__(self, xy):
        return list(map(math.ceil, xy))

    def __crop_br__(self, xy):
        return list(map(math.floor, xy))

    def to_boundary(self, xy, position):
        method_name = '__crop_' + position + '__'
        method = getattr(self, method_name)
        return method(xy)

    def cut_off(self, x1, x2):
        return int(abs(x1 - x2) * self.tile_size)

    def crop_image(self, image, tl, br):
        w = image.shape[1]
        h = image.shape[0]

        tl_tile = Tiler.web_merc_to_tile(tl[0], tl[1], self.zoom_to)
        br_tile = Tiler.web_merc_to_tile(br[0], br[1], self.zoom_to)

        tl_crop = self.to_boundary(tl_tile, 'tl')
        br_crop = self.to_boundary(br_tile, 'br')

        self.tl_tile = tl_crop

        return image[self.cut_off(tl_tile[1], tl_crop[1]):h - self.cut_off(br_tile[1], br_crop[1]),
                     self.cut_off(tl_tile[0], tl_crop[0]):w - self.cut_off(br_tile[0], br_crop[0])
                     ]

    def slice_image(self, cropped_image):
        images = []
        labels = []
        for i in range(int(cropped_image.shape[1] / self.tile_size)):
            for j in range(int(cropped_image.shape[0] / self.tile_size)):
                im = cropped_image[j * self.tile_size:(j + 1) * self.tile_size,
                                   i * self.tile_size:(i + 1) * self.tile_size]
                im = imresize(im, (self.tile_output_size, self.tile_output_size))
                images.append(im)
                labels.append('{}-{}-{}-{}'.format(self.tl_tile[0] + i,
                                                   self.tl_tile[1] + j,
                                                   self.zoom_to,
                                                   self.tile_suffix))
        return {'images': images, 'labels': labels}

    def tile_image(self, tl, br):
        cropped_image = self.crop_image(self.image, tl, br)
        slices = self.slice_image(cropped_image)
        return slices

    @staticmethod
    def save_tiles(tiles, save_location):
        if not os.path.exists(save_location):
            os.makedirs(save_location)
        for im, label in zip(tiles['images'], tiles['labels']):
            imsave('{}/{}.png'.format(save_location, label), im)
        print('Saved {} images to {}'.format(len(tiles['images']), save_location))

    @staticmethod
    def to_tile_xy(lat, lng, zoom):
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x_tile = (lng + 180.0) / 360.0 * n
        y_tile = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n
        return [x_tile, y_tile]

    @staticmethod
    def web_merc_to_tile(merc_x, merc_y, zoom):
        lng, lat = transform(Proj(init='epsg:3857'),
                             Proj(init='epsg:4326'),
                             merc_x, merc_y)
        return Tiler.to_tile_xy(lat, lng, zoom)
