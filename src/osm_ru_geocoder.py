"""
/***************************************************************************
 RuGeocoder
                                 A QGIS plugin
 Geocode your csv files to shp
                             -------------------
        begin                : 2012-02-20
        copyright            : (C) 2012 by Nikulin Evgeniy
        email                : nikulin.e at gmail
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import json
import urllib2
import urllib
from qgis.core import QgsPoint 
#from PyQt4.QtGui import QMessageBox


class OsmRuGeocoder():
    url = 'http://www.openstreetmap.ru/api/search?q='

    def _construct_search_str(self, region, rayon, city, street, house_number):
        search_str = ''
        if region:
            search_str += region +', '
        if rayon:
            search_str += rayon+', '
        if city:
            search_str += city+', '
        if street:
            search_str += street+', '
        if house_number:
            search_str += house_number
        search_str = search_str.rstrip().rstrip(',')
        #QMessageBox.information(None, "Geocoding debug", search_str)
        return search_str

    def _search(self, region, rayon, city, street, house_number):
        full_addr = self._construct_search_str(region, rayon, city, street, house_number)
        full_addr = urllib.quote(full_addr.encode("utf-8"))
        full_url = unicode(self.url) + unicode(full_addr, "utf-8")
        #QMessageBox.information(None, "Geocoding debug", full_url)
                
        f = urllib2.urlopen ( full_url.encode("utf-8") )
        resp_str = unicode( f.read(),  'utf-8')
        resp_json = json.loads(resp_str)
                
        if not resp_json["find"]:
            #0 results
            return None
        else:
            #hm... no way to find right result :( weight, addr_type_it, this_poi????
            #now get first
            res0 = resp_json["matches"][0]
            pt = QgsPoint( float(res0["lon"]), float(res0["lat"] ))
            return pt, res0["display_name"]

    def geocode(self, region, rayon, city, street, house_number):
        #try to search as is
        res = self._search(region, rayon, city, street, house_number)
        if res != None:
            return res  
        
        #try to search street:
        res = self._search(region, rayon, city, street, None)
        if res != None:
            return res
        
        #try to search settlement:
        res = self._search(region, rayon, city, None, None)
        if res != None:
            return res
        
        #try to search district:
        res = self._search(region, rayon, None, None, None)
        if res != None:
            return res
        
        #try to search region:
        res = self._search(region, None, None, None, None)
        if res != None:
            return res
        
        #hm. wtf?
        pt = QgsPoint( 0, 0)
        return pt, "Not found"
        