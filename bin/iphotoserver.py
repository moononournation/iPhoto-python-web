#!/usr/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import SimpleHTTPServer
import SocketServer
import urllib

PORT = 8000

import appledata.iphotodata as iphotodata

print "Reading iPhoto Library, please wait..."
album_xml_file = iphotodata.get_album_xmlfile('/app/iPhotoLibrary')
data = iphotodata.get_iphoto_data(album_xml_file, ratings=None, verbose=None, aperture=None)
albums = data.root_album.albums
print data
face_albums = data.getfacealbums()

class iphotoHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  # def do_GET(self):
  #   SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

  def do_POST(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    content_length = int(self.headers['Content-Length'])
    post_data_bytes = self.rfile.read(content_length)
    post_data_str = urllib.unquote(post_data_bytes).decode("UTF-8")
    list_of_post_data = post_data_str.split('&')
    post_data_dict = {}
    for item in list_of_post_data:
      variable, value = item.split('=')
      post_data_dict[variable] = value

    html = '<!doctype html><html><head><meta charset="utf-8"><title>iPhoto Server</title><link rel="icon" type="image/x-icon" href="/favicon.ico"></head><body><h1>iPhoto Server</h1>'

    if post_data_dict["album"] > "":
      searchvalue = post_data_dict["album"].decode("UTF-8").upper()
      html += '<h2>Search album: ' + searchvalue + '</h2>'
      for album in albums:
        if album.name.upper().find(searchvalue) >= 0:
          html += '<p>' + album.name + '</p>'
          for image in album.images:
            html += '<a href="/iPhotoLibrary' + image.getimagepath()[34:] + '" />'
            html += '<img height=200 src="/iPhotoLibrary' + image._getthumbpath()[34:] + '" />'
            html += '</a>'
    elif post_data_dict["person"] > "":
      searchvalue = post_data_dict["person"].decode("UTF-8").upper()
      html += '<h2>Search person: ' + searchvalue + '</h2>'
      for album in face_albums:
        if album.name.upper().find(searchvalue) >= 0:
          html += '<p>' + album.name + '</p>'
          for image in album.images:
            html += '<a href="\/iPhotoLibrary' + image.getimagepath()[34:] + '" />'
            html += '<img height=200 src="/iPhotoLibrary' + image._getthumbpath()[34:] + '" />'
            html += '</a>'
    elif post_data_dict["face"] > "":
      searchvalue = post_data_dict["face"].decode("UTF-8").upper()
      html += '<h2>Search face: ' + searchvalue + '</h2>'
      for album in face_albums:
        if album.name.upper().find(searchvalue) >= 0:
          html += '<p>' + album.name + '</p>'
          for image in album.images:
            for face_index in image.face_indexes:
              if (image.face_indexes[face_index] == album.name):
                html += '<a href="\/iPhotoLibrary' + image.getimagepath()[34:] + '" />'
                html += '<img height=200 src="/iPhotoLibrary' + image._getthumbpath()[34:-4] + '_face' + str(face_index) + '.jpg" />'
                html += '</a>'

    html += '</body></html>'
    self.wfile.write(html)

httpd = SocketServer.TCPServer(("", PORT), iphotoHandler)
print "serving at port", PORT
httpd.serve_forever()
