import requests
import json
import os


class MapPlot(object):

    def __init__(self, center_lat, center_lng, zoom, apikey=''):
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.apikey = str(apikey)
        self.icons = []
        self.imgs = os.path.join(os.path.dirname(__file__), '%s')

    def icon(self, img):
        lat = img.coords[0]
        lon = img.coords[1]
        name = img.name
        img_loc = img.portrait_loc
        img_dims = img.dimensions
        title = img.title
        self.icons.append((lat, lon, name, img_loc, img_dims, title))

    def plot_icons(self, file):
        for icon in self.icons:
            print(icon)
            self.plot_icon(file, icon[0], icon[1], icon[2], icon[3], icon[4], icon[5])

    def plot_icon(self, file, lat, lon, img_name, img_loc, img_dims, title):
        file.write('\t\tvar latlng = new google.maps.LatLng({0}, {1});\n'.format(lat, lon))
        img = os.path.join(self.imgs % img_loc)
        # print(img)
        img = img.replace('\\','/')
        file.write('\t\tvar img = {\n')
        file.write('\t\turl: "{0}",\n'.format(img))
        file.write('\t\tscaledSize: new google.maps.Size(80, 80)};\n')
        file.write('\t\tvar marker = new google.maps.Marker({\n')
        file.write('\t\ttitle: "%s",\n' % title)
        file.write('\t\ticon: img,\n')
        file.write('\t\tposition: latlng\n')
        file.write('\t\t});\n')
        file.write('\t\tmarker.addListener("click", toggleBounce);\n')
        file.write('\t\tmarker.setMap(map);\n')
        file.write('\n')

    def create_map(self, file_name):
        file = open(file_name, 'w')
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
        file.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
        file.write('<title>Sams Map</title>\n')
        file.write('<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false&key={0}"></script>\n'.format(self.apikey))
        file.write('<script type="text/javascript">\n')
        file.write('\tfunction initialize() {\n')
        file.write('\t\tvar centerlatlng = new google.maps.LatLng({0}, {1});\n'.format(self.center[0], self.center[1]))
        file.write('\t\tvar myOptions = {\n')
        file.write('\t\t\tzoom: %d,\n' % (self.zoom))
        file.write('\t\t\tcenter: centerlatlng,\n')
        file.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
        file.write('\t\t};\n')
        file.write('\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        file.write('\n')
        self.plot_icons(file)

        # function for bouncing icons
        file.write('\t\tfunction toggleBounce() {\n')
        file.write('\t\t\tif (marker.getAnimation() !==null) {\n')
        file.write('\t\t\t\tmarker.setAnimation(null);\n')
        file.write('\t\t\t} else {\n')
        file.write('\t\t\t\tmarker.setAnimation(google.maps.Animation.BOUNCE);\n')
        file.write('\t\t\t}\n')
        file.write('\t\t}\n')

        file.write('\t}\n')
        file.write('</script>\n')
        file.write('</head>\n')
        file.write('<body style="margin:0px; padding:0px;" onload="initialize()">\n')
        file.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
        file.write('</body>\n')
        file.write('</html>\n')
        file.close()
