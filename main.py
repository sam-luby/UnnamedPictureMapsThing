import exifread as ef
import re
from gmplot import gmplot
from datetime import datetime

pic = 'images/phone_pic.jpg'


def get_gps_coords(file):
    with open(pic, 'rb') as f:
        tags = ef.process_file(f)
        # print(tags)
        lat = str(tags.get('GPS GPSLatitude'))
        lat_ref = str(tags.get('GPS GPSLatitudeRef'))
        lon = str(tags.get('GPS GPSLongitude'))
        lon_ref = str(tags.get('GPS GPSLongitudeRef'))
        lat = [lat, lat_ref]
        lon = [lon, lon_ref]
        f.close()
    return lat, lon


def get_date(file):
    with open(pic, 'rb') as f:
        tags = ef.process_file(f)
        date = str(tags.get('Image DateTime'))
        print(date)
        f.close()
    return date


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


def add_marker(map, lat, lon):
    map.marker(lat, lon, 'cornflowerblue', title='test marker')



def main():
    lat, lon = get_gps_coords(pic)
    lat = DMS_to_DD(lat)
    lon = DMS_to_DD(lon)

    gmap = gmplot.GoogleMapPlotter(36.1, -115.2, 13)
    add_marker(gmap, lat, lon)
    gmap.draw("my_map.html")

    date = get_date(pic)
    format_date(date)



if __name__ == '__main__':
    main()
