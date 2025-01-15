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

# Fill out project name, uncomment desired function and execute.

gee_project = ''
initialize(gee_project)

# Panama Shape
pan_shape = ee.FeatureCollection('FAO/GAUL/2015/level0').filter(ee.Filter.eq('ADM0_NAME', 'Panama')) # Uses FAO Country shapes from GEE
pan_box = ee.Geometry.BBox(-83.055, 7.2, -77.15, 9.7) # Coordinates taken and adjusted from https://gist.github.com/graydon/11198540

# DEM
DEM = ee.Image('USGS/SRTMGL1_003').select('elevation') # https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003
DEM = clip_to_shape(DEM, pan_box)

# Slope
slope = ee.Terrain.products(DEM).select('slope') # GEE function that computes slope


# Uncomment the following line and execute for DEM.
# export_image(DEM, 'DEM Export', 'DEM', pan_box, 30)

# Uncomment the following line and execute for Slope
# export_image(slope, 'Slope Export', 'Slope', pan_box, 30)