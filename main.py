import exifread as ef
import re
import os
import plotter
from datetime import datetime
# from config import API_KEY

pic = 'images/img1.jpg'

class ImagesData(object):
    def __init__(self):
        self.images = []
       

    def add_img(self, img_name, coords, dimensions):
        self.images.append((img_name, coords, dimensions))


def get_gps_coords(file, tags):
   
   
    # print(tags)
    lat = str(tags.get('GPS GPSLatitude'))
    lat_ref = str(tags.get('GPS GPSLatitudeRef'))
    lon = str(tags.get('GPS GPSLongitude'))
    lon_ref = str(tags.get('GPS GPSLongitudeRef'))
    lat = DMS_to_DD([lat, lat_ref])
    lon = DMS_to_DD([lon, lon_ref])
    return lat, lon

def get_date(file, tags):
   
    datetime = str(tags.get('Image DateTime'))
    date = format_date(datetime)
    return date

def get_dimensions(file, tags):
    x = str(tags.get('EXIF ExifImageWidth'))
    y = str(tags.get('EXIF ExifImageLength'))
    return x, y

def format_date(date):
    date, time = date.split(' ')
    date = date.split(':')
    date.reverse()
    date = ('/').join(date)
    print(date)

def DMS_to_DD(dms_ref):
    dms = dms_ref[0]
    ref = dms_ref[1]
    dms = dms.translate({ord(c): None for c in '[!@#$]'})
    split_dms = str(dms).split(',')
    degree = int(split_dms[0])
    minute = int(split_dms[1])
    second_num, second_den = split_dms[2].split('/')
    second = float(float(second_num)/float(second_den))
    dd = round(degree + (minute/60) + (second/3600), 4)
    if ref=='S' or ref=='W':
        dd = 0 - dd
    return dd

def load_images(directory, images_data):
    directory = 'images'
    images = os.listdir(directory)
    for index, image in enumerate(images):
        with open(os.path.join(directory, image), 'rb') as f:
            tags = ef.process_file(f)
            coords = get_gps_coords(f, tags)
            x, y = get_dimensions(f, tags)
            # print(image, coords, (x, y))
            images_data.add_img('pic_{0}'.format(index), coords, (x, y))
        f.close()
    return images_data


def main():
    images_data = ImagesData()
    images_data = load_images('images', images_data)
    images_data = images_data.images

    for im  in images_data:
        print(im)
   





    # lat, lon = get_gps_coords(pic)
    # lat = DMS_to_DD(lat)
    # lon = DMS_to_DD(lon)
    # x, y = get_dimensions(pic)

    # gmap = plotter.MapPlot(36.1, -115.2, 13, apikey=API_KEY)
    # gmap.icon(lat, lon, pic, (x,y),title='hello')
    # gmap.create_map("my_map.html")
    # date = get_date(pic)
    # format_date(date)

    


if __name__ == '__main__':
    main()
