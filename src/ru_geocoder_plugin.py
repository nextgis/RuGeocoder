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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QAction, QIcon
#from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from batch_geocoding_dialog import BatchGeocodingDialog
from converter_dialog import ConverterDialog

class RuGeocoderPlugin:
    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

    def initGui(self):
        # Setup signals
        self.action_convert = QAction(QIcon(":/plugins/rugeocoderplugin/convert.png"), \
            "Convert CSV to SHP", self.iface.mainWindow())
        QObject.connect(self.action_convert, SIGNAL("triggered()"), self.run_convert)

        self.action_batch_geocoding = QAction(QIcon(":/plugins/rugeocoderplugin/icon.png"), \
            "Batch geocoding", self.iface.mainWindow())
        QObject.connect(self.action_batch_geocoding, SIGNAL("triggered()"), self.run_batch)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action_convert)
        self.iface.addPluginToMenu("&RuGeocoder", self.action_convert)

        self.iface.addToolBarIcon(self.action_batch_geocoding)
        self.iface.addPluginToMenu("&RuGeocoder", self.action_batch_geocoding)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("&RuGeocoder", self.action_convert)
        self.iface.removeToolBarIcon(self.action_convert)

        self.iface.removePluginMenu("&RUGeocoder", self.action_batch_geocoding)
        self.iface.removeToolBarIcon(self.action_batch_geocoding)

    def run_convert(self):
        dlg = ConverterDialog()
        dlg.show()
        dlg.exec_()

    def run_batch(self):
        dlg = BatchGeocodingDialog()
        dlg.show()
        dlg.exec_()
