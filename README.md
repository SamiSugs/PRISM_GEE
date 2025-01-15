# README

For PRSIM 2024, please note that the DEM included in these scripts is ***not*** the same DEM processed for the workshop. The workshop used the Copernicus GLO-30 DEM, this one uses the USGS SRTM 30m DEM. This makes it possible to use the native gee ee.Terrain.slope() function to compute a slope from the DEM, which could not be figured out in time for the workshop. The slope will therefore differ as well, since to compute the slope for PRISM, yet another DEM was used, whose source is included in the documentation.

## Running Scripts

I had trouble installing the packages required to authenticate the Google account and run the scripts locally (could not figure it out in fact), so as a work around, you can run the script in Colab (Cloud compute notebook available with standard Google account). To do this, copy the code from the file and paste it in Colab.

Here is a non-technical guide to running each script.

Quick notes:

-   for each script, you must enter a GEE project (by default, this looks like 'ee-yourname'). The file will download to the Google Drive of the account associated with the project.

-   Uncommenting a line of code means deleting the hash symbol and the space that follows that are at the beginning of the line. For example if the original line was:

    \# export_image(coral, 'Coral Export', 'Coral', pan_box)

    Uncommenting it would mean leaving it as:

    export_image(coral, 'Coral Export', 'Coral', pan_box)

-   When running one of these scripts, you will usually be prompted to authenticate the google account. Simply click 'yes' or 'continue' or similar and sign in if prompted. This step is skipped if the authentication is cached (i.e. you have authenticated recently).

### Coral:

This file is small enough to download on the fly (\~12 seconds to download to Drive)

1.  Once the script is in Colab and a valid project name is entered, uncomment the very last line of code and run the script.
2.  Authenticate if necessary.
    -   File will be called Coral.tif

### Mangrove:

This file is small enough to download on the fly (\~11 seconds to download to Drive)

1.  Once the script is in Colab and a valid project name is entered, uncomment the very last line of code and run the script.
2.  Authenticate if necessary.
    -   File will be called PanamaMangroves.csv

### Monthly LANDSAT Average:

These files would be very impractical and slow to download on the fly

-   This script will download multiple files, each one representing the average LANDSAT for one month in the desired range.
-   The script returns all the months for the given calendar years. If you want Oct. 2020 - Jun. 2021, you will have to download all of 2020 and 2021 and choose the appropriate files once they have downloaded.

1.  Once the script is in Colab and a valid project name is entered, fill in the values of 'args' (lines 80-84). ***Do not delete the commas.***
    -   'collection' is the specific LANDSAT collection that the files will download from. The file imports 5, 7, and 8. Choose which collection you want based on the dates you need and the dates for which each collection is available (I left the years available as comments above each). To fill in the value, write "LANDSAT5", "LANDSAT7", or "LANDSAT8", ***without the quotation marks.***

        -   If your desired range is covered by two collections, the newer one is likely best.

        -   If your desired range cannot be covered by one collection, run the script twice, once to get as much as possible from the newer collection, and again to get the missing ones from the older collection.

        -   IMPORTANT: avoid requesting the first or last year of any collection. They begin and end at arbitrary times in the year, which could lead to undesired results

        -   e.g. if I want 2012 - 2023, I would run the script once with LANDSAT8 for 2014-2023 and once with LANDSAT7 for 2012-2013.

    -   'year' is the first year in your desired range. Write it as a number with no quotations

    -   'num_years' is the number of years in your desired range. Write it as a number with no quotations

        -   e.g. if I wanted 2018-2020 (inclusive), 'year' would be 2018,

    -   'region' should be left as is for the whole of Panama, otherwise you will need to create a new object to define the boundary, which will require familiarity with Python and the Python GEE API.

    -   'scale' controls the resolution of the downloaded files. It is set to the finest resolution (30m x 30m), but can be adjusted to any value greater than 30. Measured in meters.

    -   'export_name' can be left as is or modified. This will be the core of the file name of the downloaded files. If modifying, be sure to not delete the apostrophes.
2.  Uncomment the final line of code and execute the script.
    -   File names will be the export_name you defined, and the month/year of the file.

        -   e.g. the file containing information for February 2023 will be called export_nameFeb2023.tif
3.  Authenticate if necessary.

### Yearly LANDSAT NDVI Average

These files would be very impractical and slow to download on the fly

-   This script will download multiple files, each one representing the average LANDSAT for one year in the desired range.

1.  Once the script is in Colab and a valid project name is entered, fill in the values of 'args' (lines 86-92). ***Do not delete the commas.***
    -   'collection' has the same function as above, but you may also choose NDVI in addition to the LANDSAT options from before. If choosing NDVI, please read the rest of the guide carefully.

    -   'year' is identical to the description above.

    -   'num_years' is similar to the description above, but instead of being the number of years in your desired range, it is simply the number of years desired. See 'step' for clarification.

    -   'export_name' has the same function as above, but if you are seeking to download NDVI, I highly recommend you do not leave it as is (I suggest replacing 'LANDSAT' with 'NDVI').

    -   'region' is identical to its corresponding description above.

    -   'scale' has the same function as above, but beware for NDVI: the smallest resolution for NDVI is 250, so you must adjust the value to at least 250 if downloading NDVI data.

    -   'step' is the interval (in years) at which the program will compute and download data. It allows you to download the data for every x-*th* year.
2.  Uncomment the final line of code and execute the script.
    -   The file names will be similar to above, but will not contain the month, only the year.
3.  Authenticate if necessary.

### Slope and DEM

These files would not be practical to download on the fly. Downloads a 30m x 30m resolution.

1.  Once the script is in Colab and a valid project name is entered, uncomment either line 59 for the DEM or line 62 for the slope (or both, if desired), and execute the code.
2.  Authenticate if necessary.
    -   File name will be DEM.tif for DEM, and Slope.tif for slope.

Note: the slope is not a dataset that exists, it is computed using the DEM using a function in the gee package (ee.Terrain.products(DEM).select('slope')). See Google's documentation for more.
