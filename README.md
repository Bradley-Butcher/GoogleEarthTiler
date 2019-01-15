# GoogleEarthTiler

Given a large image with Web Mercator coordiates, create Google Map Compatible tiles (Pseudo Mercator) with the label format (X, Y, Zoom)

```
#Import tiler class
from Tiler import Tiler

#Zoom to = Zoom level to output image @ in pseudo mercator
# Tile input size = size to slice images at, different to output size if doesnt match exact zoom level
# Tile suffix added to tile name if is required
tiler = Tiler(image_filename='filename.jpg',
              zoom_to=18,
              tile_input_size=344,
              tile_output_size=256,
              tile_suffix=1999)

# Top Left in Web Mercator (Generated from Google Earth Pro .points)
tl = [12696031, 3587499]
# Bottom Right in Web Mercator (Generated from Google Earth Pro .points)
br = [12702688,3582791]

#Tile using loaded image and coordinates, stored in dict['images'] dict['labels'] with direct correspondence
tiles = tiler.tile_image(tl, br)

#Save tiles to files with filenames = labels
Tiler.save_tiles(tiles, 'output_folder')
```
