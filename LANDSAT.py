# based on Ana's GEE code

import ee
import geemap

def initialize(proj_name: str) -> None:
    """Initialize and authenticate Earth Engine."""
    try:
        ee.Initialize(project=proj_name)
    except Exception as e:
        ee.Authenticate()
        ee.Initialize(project=proj_name)

def export_image(img: ee.image.Image, description: str, export_name: str, scale=None, crs='EPSG:4326', crsTransform=None) -> None:
    """Export an Earth Engine image to an asset."""

    task_args = {
        'image': img,
        'description': description,
        'fileNamePrefix': export_name,
        'crs': crs,
        'maxPixels': 4e12,
        'region': pan_box
    }

    if scale is not None:
        task_args['scale'] = scale
    if crsTransform is not None:
        task_args['crsTransform'] = crsTransform

    task = ee.batch.Export.image.toDrive(**task_args)
    task.start()

class MapManager:
    """Manage map visualization for Earth Engine data."""
    def __init__(self, center, zoom):
      self.center = center
      self.zoom = zoom

    def init_map(self) -> None:
        Map = geemap.Map(center=self.center, zoom=self.zoom)
        return Map

def clipToShape(map, shape) -> type(map):
    """Clip either an Image or an ImageCollection to a shape."""
    if type(map) is ee.image.Image:
        return map.clip(shape)
    elif type(map) is ee.imagecollection.ImageCollection:
        return map.map(lambda img: img.clip(shape))


usermap = ''

initialize(usermap)

# Panama Shape
pan_shape = ee.FeatureCollection('FAO/GAUL/2015/level0').filter(ee.Filter.eq('ADM0_NAME', 'Panama')) # Uses FAO Country shapes from GEE
pan_box = ee.Geometry.BBox(-83.055, 7.2, -77.15, 9.7) # Coordinates taken and adjusted from https://gist.github.com/graydon/11198540

# LANDSAT  red green near-IR bands
LANDSAT = ee.ImageCollection('LANDSAT/LE07/C02/T1_RT').select('B1', 'B2', 'B3', 'B4') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_RT
panLANDSAT = clipToShape(LANDSAT, pan_shape)

# LANDSAT for yearly mean 1990. All reflectance bands
LANDSAT5 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2
panLANDSAT5 = clipToShape(LANDSAT5, pan_shape)

# LANDSAT for yearly means 2000, 2010, 2020. All reflectance bands
LANDSAT7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2
panLANDSAT7 = clipToShape(LANDSAT7, pan_shape)

# LANDSAT for detailed 2021, 2022. All reflectance bands
LANDSAT8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B6', 'SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2
panLANDSAT8 = clipToShape(LANDSAT8, pan_shape)

def get_maps_yearly_mean(collection, start_year: int, end_year: int, step=1, export_name='LANDSAT') -> None:
    """Downloads a map of the mean values over the desired years to user's Google Drive. Includes end_year.
    Note: to download the map for a single year, set start_year and end_year to the desired year"""

    for year in range(start_year, end_year + 1, step):
        year = str(year)
        start = year + '-01-01'
        end = year + '-12-31'
        LANDSAT_year_img = panLANDSAT.filterDate(start, end).reduce(ee.Reducer.mean())
        export_image(LANDSAT_year_img, 'ExportLANDSAT' + year,
            export_name + year, 30, 'EPSG:4326')


def get_each_image(collection, start_year: int, end_year: int, export_name='LANDSAT') -> None:
    """Downloads each image taken over the desired years to user's Google Drive. Includes end_year.
    Do not pre-filter the collection by date."""

    start = str(start_year) + '-01-01'
    start = ee.Date(start)
    end = str(end_year) + '-12-31'

    while start.format().getInfo() < end:
        img = collection.filterDate(start, '2030-01-01').first()
        date_of_img = img.date()
        date = date_of_img.format('YYYYMMdd').getInfo()
        export_image(img, 'ExportLANDSAT', export_name + date, 30)
        start = date_of_img.advance(1, 'day')
