# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 16:34:54 2018

@author: marti
"""

# Funktionalität
## Done
# - lesen Koordinaten SAC-cabinn ab csv-File
# - SAC-Hütten suchen (nach Namen)
# - SAC-Hütten auflisten
# - SAC-Hütte als besucht markieren inkl Besuchsdatum
# - SAC-Hütte wieder austragen, wenn fehlerhaft registiert
# - besucht SAC-Hütten auflisten

## Backlog
# - SAC-Hütten suchen (nach Kanton)
# - GPX-Datei für SAC-Hütten erstellen

import pandas as pd
import numpy as np
import sys

import getopt

import gpxpy
#import gpxpy.gpx

class SacHuette():


    class debug():

        def __init__(self,debugFlag, printLine):
            self.debugFlag = debugFlag
            self.printLine = printLine

            self.show(self.debugFlag, self.printLine)

        def show(self,debugFlag, printLine):
            self.debugFlag = debugFlag
            self.printLine = printLine

            if self.debugFlag:
                print(printLine)

    ####################

    def __init__(self):
        self.filename = ''
        self.searchString = ''
        self.option = ''
        self.visitdate = ''
        self.argv = []
        self.debugFlag = False

        self.debug = SacHuette.debug(False, None)

    def get(self):
        sac_df = pd.read_csv(sac.filename, sep = ';')

        sac_df['visitdate'] = pd.to_datetime(sac_df.visitdate, format='%Y-%m-%d')
        # print(sac.debugFlag, sac_df.info())
        return sac_df

    def put(self, sac_df):
        print('save csv file %s' % sac.filename)
        sac_df.to_csv(sac.filename, sep=';', index=False)


    def list(self, sac_df):
        print('List of SAC cabins:')
        print(sac_df[['cabin', 'visitdate']])

    def search(self, sac_df, searchString):
        print('SAC cabins search result for: %s' % searchString)
        sac_search_df = sac_df[sac_df.cabin.str.contains(searchString, case=False)==True]
        print(sac_search_df[['cabin', 'places', 'website', 'visitdate']])

    def visited(self, sac_df):
        print('visited SAC cabins:')
        sac_search_df = sac_df[sac_df.visited==True]
        print(sac_search_df[['cabin', 'visitdate']])

    def addVisit(self, sac_df, cabin, visitdate):
        print('you visited cabin %s at %s ' % (cabin, visitdate))
        # hütte in DF suchen
        # prüfen ob schon auf visited gesetzt, wenn ja Fehlermelung ausgeben
        # visited auf True setzen
        sac_df.loc[sac_df['cabin'] == cabin, 'visited'] = True

        # visitdate setzen
        sac_df.loc[sac_df['cabin'] == cabin, 'visitdate'] = visitdate

        # save dataframe to csv file
        self.put(sac_df)
        # list cabin with visitdate
        self.search(sac_df, cabin)


    def deleteVisit(self, sac_df, cabin):
        print('will delete visit at cabin %s ' % cabin)
        # hütte in DF suchen
        # prüfen ob schon auf visited gesetzt, wenn ja Fehlermelung ausgeben
        # visited auf False setzen
        sac_df.loc[sac_df['cabin'] == cabin, 'visited'] = False

        # visitdate entfernen
        sac_df.loc[sac_df['cabin'] == cabin, 'visitdate'] = None

        # save dataframe to csv file
        self.put(sac_df)
        # list cabin with visitdate
        self.search(sac_df, cabin)

    def help(self):
        print('Help for SAC cabins')
        print(sys.argv[0], '[-h] [-n cabin] [-l|-a|-d|-v]')
        print('-h = help')
        print('-l = list')
        print('-a = add visit')
        print('-d = delete existing visit')
        print('-v = visited cabins')
        print('')
        print('-t = run module in test mode (for development use only)')

    def arguments(self):
        try:
          opts, args = getopt.getopt(sac.argv,"a:dghln:tv")
    #      print("opts, args:",opts, " --- ",args)
        except getopt.GetoptError:
          print(sac.help())
          sys.exit(2)
        for opt, arg in opts:
    #      print(opt, arg)
            if opt == '-h':
                print(sac.help())
                sys.exit(0)
            elif opt in ("-n"):
                sac.searchString = arg
            elif opt in ("-l"):
                sac.option = 'list'
            elif opt in ("-a"):
                sac.option = 'add'
                sac.visitdate = arg
            elif opt in ("-d"):
                sac.option = 'delete'
            elif opt in ("-g"):
                sac.option = 'gpx'
            elif opt in ("-t"):
                sac.testFlag = True
            elif opt in ("-v"):
                sac.option = 'visited'
        sac.debug.show(sac.debugFlag, 'search String = ' + sac.searchString)
        sac.debug.show(sac.debugFlag, 'Option = ' + sac.option)

    def writeGpx(self, sac_df):

        # Creating a new file:
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        # Create points:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, elevation=1234))
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235))
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(2.1236, 5.1236, elevation=1236))

        # You can add routes and waypoints, too...

        print('Created GPX:', gpx.to_xml())

###############################################################################
##### MAIN
###############################################################################
if __name__ == "__main__":
    sac = SacHuette()

    # get arguments form commandline
    sac.argv = sys.argv[1:]

    # specify filename
    sac.filename = 'Clubhuettenverzeichnis.csv'

    # split commandline arguments to single values of Class SacHuette
    sac.arguments()


    if sac.option == "":
      print(sac.help())
      sys.exit(3)

    # read SAC Huetten CSV file
    sac_df = sac.get()

    ## list Hütte with wildcards
    if sac.option == 'list':
        sac.search(sac_df, sac.searchString)
        sys.exit(0)

    ## visited hütten auflisten
    if sac.option == 'visited':
        sac.visited(sac_df)
        sys.exit(0)

    ## Hütte auf visited setzen
    if sac.option == 'add':
        sac.addVisit(sac_df, sac.searchString, sac.visitdate)
        sys.exit(0)

    ## visit von Hütte entfernen
    if sac.option == 'delete':
        sac.deleteVisit(sac_df, sac.searchString)
        sys.exit(0)

    ## alle Hütten in GPX-File schreiben
    if sac.option == 'gpx':
        sac.writeGpx(sac_df)
        sys.exit(0)

    ## handle not specified option
    print('SAC cabins:')
    print('option "%s" not handled yet' % sac.option)