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

def export_image(img: ee.image.Image, description: str, export_name: str, region, scale=None, crs='EPSG:4326') -> None:
    """Export an Earth Engine image to an asset."""

    task_args = {
        'image': img,
        'description': description,
        'fileNamePrefix': export_name,
        'crs': crs,
        'maxPixels': 4e12,
        'region': region
    }

    if scale is not None:
        task_args['scale'] = scale

    task = ee.batch.Export.image.toDrive(**task_args)
    task.start()

def clip_to_shape(map, shape: ee.feature.Feature) -> type(map):
    """Clip either an Image or an ImageCollection to a shape."""
    if type(map) is ee.image.Image:
        return map.clip(shape)
    elif type(map) is ee.imagecollection.ImageCollection:
        return map.map(lambda img: img.clip(shape))
    elif type(map) is ee.featurecollection.FeatureCollection:
        return map.filterBounds(shape)

def get_maps_yearly_mean(collection, year: int, num_years: int, export_name: str, region, scale: int, step: int) -> None:
    """Downloads a map of the mean values over the desired years to user's Google Drive.
    Note: to download the map for a single year, set start_year and end_year to the desired year"""


    start = ee.Date(str(year) + '-01-01')
    end = ee.Date(str(year) + '-12-31')

    for i in range(num_years):
        LANDSAT_year_img = collection.filterDate(start, end).reduce(ee.Reducer.mean())
        
        export_image(LANDSAT_year_img, 'Export' + export_name + start.format('YYYY').getInfo(),
            export_name + start.format('YYYY').getInfo(), region, scale, 'EPSG:4326')

        start = start.advance(step, 'year')
        end = end.advance(step, 'year')


# Fill out following variables, uncomment last line and execute code

gee_project = ''
initialize(gee_project)

# Panama Shape
pan_shape = ee.FeatureCollection('FAO/GAUL/2015/level0').filter(ee.Filter.eq('ADM0_NAME', 'Panama')) # Uses FAO Country shapes from GEE
pan_box = ee.Geometry.BBox(-83.055, 7.2, -77.15, 9.7) # Coordinates taken and adjusted from https://gist.github.com/graydon/11198540

# LANDSAT 1984-2012. All reflectance bands
LANDSAT5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2").select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LT05_C02_T1_L2
LANDSAT5 = clip_to_shape(LANDSAT5, pan_shape)

# LANDSAT 1999-2021. All reflectance bands
LANDSAT7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C02_T1_L2
LANDSAT7 = clip_to_shape(LANDSAT7, pan_shape)

# LANDSAT 2013-. All reflectance bands
LANDSAT8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").select('SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5','SR_B6', 'SR_B7') # https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2
LANDSAT8 = clip_to_shape(LANDSAT8, pan_shape)

# NDVI Available from 2000-02-18 @ 250m scale
NDVI = ee.ImageCollection("MODIS/061/MOD13Q1").select('NDVI') # https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1
NDVI = clip_to_shape(NDVI, pan_shape)


args = {
    'collection' : , # select based on desired years (see comments) and data
    'start_year' : ,
    'num_years' : ,
    'export_name' : 'LANDSAT', # Replace name for NDVI
    'region' : pan_box, # Can choose some other region if desired.
    'scale' : 30, # Set to 250 for NDVI!
    'step' : 1
}

# get_maps_yearly_mean(*args.values())