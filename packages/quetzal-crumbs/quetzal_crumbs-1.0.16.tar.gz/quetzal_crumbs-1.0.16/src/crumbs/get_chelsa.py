#!/usr/bin/python

import requests
import os
import rasterio
from rasterio import mask as msk
import fiona
from shapely.geometry import shape, Point, Polygon
from optparse import OptionParser
from tqdm import tqdm
from osgeo import gdal
from pathlib import Path;
from os import walk
from os.path import exists
import re
import glob

def tryfloat(s):
    try:
        return float(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryfloat(c) for c in re.split('_(-*\d+)_' , s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    return l


def bounds_to_polygon(shapefile, margin):
    """ Computes a bounding box around points in the shapefile, adding a margin.
        Returns a spatial polygon.
    """
    import fiona
    import numpy as np
    with fiona.open(shapefile) as file:
        shapes = list(file)
        coords = [p['geometry']['coordinates'] for p in shapes]
        bot_left_x, bot_left_y, top_right_x, top_right_y = bounding_box_naive(coords)
        bbox = to_polygon(bot_left_x, bot_left_y, top_right_x, top_right_y, margin)
        return bbox

def bounding_box_naive(points):
    """returns a list containing the bottom left and the top right
    points in the sequence.
    Here, we use min and max four times over the collection of points.
    """
    bot_left_x = min(point[0] for point in points)
    bot_left_y = min(point[1] for point in points)
    top_right_x = max(point[0] for point in points)
    top_right_y = max(point[1] for point in points)

    return bot_left_x, bot_left_y, top_right_x, top_right_y

def to_polygon(long0, lat0, long1, lat1, margin=0.0):
    """ Convert the given points into a polygon, adding a margin.
    """
    return Polygon([[long0 - margin , lat0 - margin],
                    [long1 + margin , lat0 - margin],
                    [long1 + margin , lat1 + margin],
                    [long0 - margin , lat1 + margin]])

def clip(inputFile, shape, outputFile):
    """ Clip the input file by the shape given, saving the output file.
    """
    # read source
    with rasterio.open(inputFile) as source :
        out_image, out_transform = msk.mask(source, [shape], crop=True)
        out_meta = source.meta
        # udate metadata
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

    with rasterio.open(outputFile, "w", **out_meta) as dest:
        dest.write(out_image)


def resume_download(fileurl, resume_byte_pos):
    """ Resume the download of the file given its url
    """
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    return requests.get(fileurl, headers=resume_header, stream=True,  verify=True, allow_redirects=True)

def download(url, output_dir):
    """ Downloads bio and orog variables from CHELSA-TraCE21k – 1km climate timeseries since the LG
    """
    print(url)
    #  Retrievethe filename from the URL so we have a local file to write to
    filename = output_dir + "/" + get_filename(url)
    path = Path(filename)
    if path.is_file():
        resume_byte = path.stat().st_size
        print("World file exists, resuming download to byte", resume_byte)
    else:
        print("World file does not exist, starting download from scratch.")
        resume_byte = 0.0

    try:
        with open(filename, 'ab') as file:
            response = resume_download(url, resume_byte)

            # progress bar
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            # download progress
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
        return filename
    except requests.RequestException as e:
        print(e)
    return

def expand_bio(variables):
    bioset = set(variables) - set(['dem','glz'])
    if( len(bioset) > 0 ) :
        if bioset == set(['bio']):
            bioset = set(['bio' + str(i).zfill(2) for i in range(1, 19, 1)])
    return list(bioset.union(set(variables)) - set(['bio']))

def generate_urls(variables, timesID):
    """ Generate the expected CHELSA TraCE21k urls given the variables and the time IDS to retrieve.
    """
    assert len(variables) > 0 , "Unable to generate URL fom an empty variables list"
    assert len(timesID) > 0 , "Unable to generate URL from an empty timesID list"

    urls = []
    implemented = implemented_variables()

    if( set(variables).issubset(set(implemented)) or set(variables) - set(['dem','glz']) == set(['bio'])  ) :

        if(set(['dem']).issubset(set(variables))):
            for timeID in timesID :
                url = "https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V1/chelsa_trace/orog/CHELSA_TraCE21k_dem_"+ str(timeID) + "_V1.0.tif"
                urls.append(url)

        if(set(['glz']).issubset(set(variables))):
            for timeID in timesID :
                url = "https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V1/chelsa_trace/orog/CHELSA_TraCE21k_glz_"+ str(timeID) + "_V1.0.tif"
                urls.append(url)

        bioset = set(variables) - set(['dem','glz'])
        if( len(bioset) > 0 ) :
            if bioset == set(['bio']):
                bioset = set(['bio' + str(i).zfill(2) for i in range(1, 19, 1)])
            for bio in bioset:
                for timeID in timesID :
                    url = "https://os.zhdk.cloud.switch.ch/envicloud/chelsa/chelsa_V1/chelsa_trace/bio/CHELSA_TraCE21k_" + bio + "_"+ str(timeID) + "_V1.0.tif"
                    urls.append(url)

    else:
        not_implemented = set(variables) - set(variables).intersection(set(implemented))
        raise ValueError(" ".join([str(i) for i in not_implemented]) + " not implemented. Implemented CHELSA variables are: " + " ".join([str(i) for i in implemented]))

    # Post condition: at least one workable URL
    assert len(urls) > 0 , "Unable to generate URL."
    return urls

def to_vrt(inputFiles, outputFile='stacked.vrt'):
    """ Converts the list of input files into an output VRT file, that can be converted to geoTiff
    """
    print("    ... converting bands to VRT file:", outputFile)
    gdal.BuildVRT(outputFile, inputFiles,
        separate=True,
        #callback=gdal.TermProgress_nocb
        )
    vrt_options = gdal.BuildVRTOptions(separate=True,
                                        #callback=gdal.TermProgress_nocb,
                                        resampleAlg='average')
    my_vrt = gdal.BuildVRT(outputFile, inputFiles, options=vrt_options)
    my_vrt = None
    return(outputFile)

def to_geotiff(vrt, outputFile='stacked.tif'):
    """ Converts the VRT files to a geotiff file
    """
    print('    ... converting', vrt, 'to GeoTiff file:', outputFile)
    ds = gdal.Open(vrt)
    ds = gdal.Translate(outputFile, ds)
    ds = None

def create_folders_if_dont_exist(output_dir, clipped_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(clipped_dir):
        os.makedirs(clipped_dir)
    return

def read_urls(inputFile):
    with open(inputFile, 'r') as input:
        urls = input.readlines()
        return [url.strip() for url in urls]

def get_filename(url):
    #  splits the url into a list, starting from the right and get last element
    filename = url.rsplit('/', 1)[-1].strip()
    return filename

def download_and_clip(url, output_dir, clip_shape, clipped_file, cleanup):
    import rasterio
    downloaded = download(url, output_dir)
    clip(downloaded, clip_shape, clipped_file)
    if cleanup is True: os.remove(downloaded)
    return

def remove_chelsa_dir_if_empty(output_dir):
    if len(os.listdir(output_dir)) == 0:
        os.rmdir(output_dir)
    else:
        import warnings
        warnings.warn("Directory " + output_dir + " is not empty and will not be deleted.")
    return

def implemented_variables():
    return ['dem', 'glz', *['bio' + str(i).zfill(2) for i in range(1, 19, 1)]]

def retrieve_variables(urls):
    matched = []
    for variable in implemented_variables():
        if any(variable in s for s in urls):
            matched.append(variable)
    return matched

def get_chelsa(inputFile=None, variables=None, timesID=None, points=None, margin=0.0, chelsa_dir='CHELSA_world', clip_dir='CHELSA_cropped', geotiff='chelsa_stack.tif', cleanup=False):
    """ Downloads bio and orog variables from CHELSA-TraCE21k –
        1km climate timeseries since the LG and clip to spatial extent of sampling points, converting the output into a geotiff file
    """
    print("- Quetzal-CRUMBS - CHELSA-TraCE21k data access for iDDC modeling")
    if points is not None:
        bounding_box = bounds_to_polygon(points, margin)
        print('    ... rasters will be cropped to bounding box infered from points:', bounding_box)

    create_folders_if_dont_exist(chelsa_dir, clip_dir)

    if inputFile is None:
        variables = expand_bio(variables)
        urls = generate_urls(variables, timesID)
    else:
        urls = read_urls(inputFile)
        variables = retrieve_variables(urls)

    assert len(urls) != 0 , "no URL generated or read in file."

    clip_files = []
    for url in urls:
        clip_file = clip_dir + "/" + get_filename(url)
        clip_files.append(clip_file)
        if not exists(clip_file): download_and_clip(url, chelsa_dir, bounding_box, clip_file, cleanup)

    if cleanup is True: remove_chelsa_dir_if_empty(chelsa_dir)

    for variable in variables:
        matching = [s for s in clip_files if variable in s]
        filename = geotiff.rsplit('.', 1)[-2]  + "_" + variable
        VRT = to_vrt(sort_nicely(matching), filename + ".vrt"  )
        to_geotiff(VRT,  filename + ".tif")

def get_variables_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def get_timesID_args(option, opt, value, parser, type='int'):
    setattr(parser.values, option.dest, [int(s) for s in value.split(',')])

def main(argv):

    parser = OptionParser()

    parser.add_option("-i", "--input", type="str", dest="input", help="Input urls file, one url by line")

    parser.add_option("-v", "--variables",
                        dest="variables",
                        type='str',
                        action='callback',
                        callback=get_variables_args,
                        help="If no input given, comma-separated CHELSA TraCE21k variables to download. Possible options: dem, glz, bio01 to bio19 or bio for all")

    parser.add_option("-t", "--timesID",
                        dest="timesID",
                        type='str',
                        action='callback',
                        callback=get_timesID_args,
                        help="CHELSA_TraCE21k_ times IDs to download. Default: 20 (present) to -200 (LGM)")

    parser.add_option("-p", "--points", type="str", dest="points", default=None, help="Shapefile of spatial points around which a bounding box will be drawn to clip the CHELSA tif. Example: all DNA samples coordinates, or 4 coordinates defining a bounding box.")
    parser.add_option("-m", "--margin", type="float", dest="margin", default=0.0, help="Margin to add around the bounding box, in degrees.")
    parser.add_option("-d", "--dir", type="str", dest="chelsa_dir", default = "CHELSA_world", help="Output directory for CHELSA files. Default: CHELSA_world.")
    parser.add_option("-c", "--clip_dir", type="str", dest="clip_dir", default = "CHELSA_cropped", help="Output directory for clipped CHELSA files. Default: CHELSA_cropped.")
    parser.add_option("-o", "--geotiff", type="str", dest="geotiff", default = "chelsa_stack.tif", help="Produces a geotiff.")
    parser.add_option("--cleanup", dest="cleanup", default = False, action = 'store_true', help="Remove downloaded CHELSA world files, but keep clipped files.")
    parser.add_option("--no-cleanup", dest="cleanup", action = 'store_false', help="Keep downloaded CHELSA files on disk.")
    (options, args) = parser.parse_args(argv)
    try:
        return get_chelsa(
            inputFile = options.input,
            variables = options.variables,
            timesID = options.timesID,
            points = options.points,
            margin = options.margin,
            chelsa_dir = options.chelsa_dir,
            clip_dir = options.clip_dir,
            geotiff = options.geotiff,
            cleanup = options.cleanup)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
