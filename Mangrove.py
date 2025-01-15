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

def export_feature(feat, description: str, export_name: str,) -> None:
    """Export an Earth Engine feature or feature collection to an asset."""

    task_args = {
        'collection': feat,
        'description': description,
        'fileNamePrefix': export_name,
        'fileFormat' : 'CSV',
    }

    task = ee.batch.Export.table.toDrive(**task_args)
    task.start()

def clip_to_shape(map, shape: ee.feature.Feature) -> type(map):
    """Clip either an Image or an ImageCollection to a shape."""
    if type(map) is ee.image.Image:
        return map.clip(shape)
    elif type(map) is ee.imagecollection.ImageCollection:
        return map.map(lambda img: img.clip(shape))
    elif type(map) is ee.featurecollection.FeatureCollection:
        return map.filterBounds(shape)


# Uncomment last line and execute.

gee_project = ''
initialize(gee_project)

# Panama Shape
pan_shape = ee.FeatureCollection('FAO/GAUL/2015/level0').filter(ee.Filter.eq('ADM0_NAME', 'Panama')) # Uses FAO Country shapes from GEE
pan_box = ee.Geometry.BBox(-83.055, 7.2, -77.15, 9.7) # Coordinates taken and adjusted from https://gist.github.com/graydon/11198540

# Mangrove
# Source: https://www.globalmangrovewatch.org/
# Download: https://zenodo.org/records/12756047
mangrove = ee.FeatureCollection('projects/ee-samisugiarta/assets/Mangroves') # Leave as is, the file is held with open access here. 
mangrove = clip_to_shape(mangrove, pan_box)


# export_feature(mangrove, 'ExportMangrove', 'PanamaMangroves')