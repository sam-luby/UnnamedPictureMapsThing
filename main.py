import exifread as ef
import re

pic = 'images/phone_pic.jpg'


def get_gps_coords(file):
    with open(pic, 'rb') as f:
        tags = ef.process_file(f)
        lat = str(tags.get('GPS GPSLatitude'))
        lat_ref = str(tags.get('GPS GPSLatitudeRef'))
        lon = str(tags.get('GPS GPSLongitude'))
        lon_ref = str(tags.get('GPS GPSLongitudeRef'))
        lat = [lat, lat_ref]
        lon = [lon, lon_ref]
        return lat, lon


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


def main():
    lat, lon = get_gps_coords(pic)
    print(DMS_to_DD(lat))
    print(DMS_to_DD(lon))


if __name__ == '__main__':
    main()
