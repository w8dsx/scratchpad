#!/usr/bin/env python3
"""
test development file for initial objects

Author: Wm. Smith - w8dsx
Copyright ©2019 2synergetic LLC, All rights reserved.

NMEA Sentence Types
GPGGA 	Global positioning system fix data (time, position, fix type data)
GPGLL 	Geographic position, latitude, longitude
GPVTG 	Course and speed information relative to the ground
GPRMC 	Time, date, position, course and speed data
GPGSA 	GPS receiver operating mode, satellites used in the position solution, and DOP values.
GPGSV 	The number of GPS satellites in view satellite ID numbers, elevation, azimuth and SNR values.
GPMSS 	Signal to noise ratio, signal strength, frequency, and bit rate from a radio beacon receiver.
GPTRF 	Transit fix data
GPSTN 	Multiple data ID
GPXTE 	cross track error, measured
GPZDA 	Date and time (PPS timing message, synchronized to PPS).
"""
from enum import Enum
import os
from pynmeagps.nmeareader import NMEAReader

#KNOTSCONV = {"MS": 0.5144447324, "FS": 1.68781084, "MPH": 1.15078, "KMPH": 1.852001}

class nmeaSentenceType(Enum):
    GPGGA = 1
    GPGLL = 2
    GPVTG = 3
    GPRMC = 4
    GPGSA = 5
    GPGSV = 6
    GPMSS = 7
    GPTRF = 8
    GPSTN = 9
    GPXTE = 10
    GPZDA = 11

class nmeaSentenceQuality(Enum):
    INVALID = 0
    GPS_FIX = 1
    DPGS_FIX = 2

class nmeaGPGSmodeAutoManual(Enum):
    M = 0
    A = 1

class nmeaGPGSmodeFix(Enum):
    FixNotAvailable = 1
    twoD = 2
    threeD = 3


path_init='/media/racebannon/6233-100F'


class fileSystemTroll():
    def __init(self):
        theDir=os.getcwd()
        for root, dirs, files in os.walk(path_init):
            for name in files:
                print(os.path.join(root, name))
                for name in dirs:
                    print(os.path.join(root, name))


class SourceDataType(Enum):
       file = 1
       usbconnection = 2
       network= 3


class SourceData():
    def __init__(self,in_source:SourceDataType):
        self.SourceDataType = in_source



class radio():
   def __init__(self, in_source:SourceDataType):
      self.SourceDataType=in_source


# the 2syn solution
class EasyReader():

    def __init__(self,fileName):
        print('init')
        sentences=[]
        sepr=','
        with open(fileName) as f:
            for line in f:
                #line_=f'{(line).split(sepr)}'
                dataProc=nmeaSentence(line)


class nmeaSentence():
    def __init__(self, in_raw_data):
        self.mtypes = {"GPGGA", "GPGSA", "GPRMC", "GPVTG"}
        sepr = ','
        raw_data_=in_raw_data.split(sepr)
        sentType_=raw_data_[0]
        sentenceType_=sentType_.replace('$',"")              # remove dollar sign from sentence thype
        if sentenceType_ in self.mtypes:
            procname=getattr(self,sentenceType_)                # derive pointer to subproce=raw_data_ss
            (procname)(raw_data_)                               # call subprocess to extract data


    def GPGGA(self,raw_data_):
        print('GPGGA')
        (sentType_, time_, lat_, NS_, lon_, EW_, quality_, numSV_, HDOP_, alt_, altUnit_, sep_, sepUnit_, diffAge_, diffStation_)=raw_data_
        self.time=f'{time_[0:2]}:{time_[2:4]}:{time_[4:6]}'
        self.latitutue=round(float(lat_[0:2])+(float(lat_[2:])/60),8)
        self.longitude=-1*round(float(lat_[0:3])+(float(lat_[3:])/60),8) if EW_=='W' else round(float(lat_[0:3])+(float(lat_[3:])/60),8)
        self.altitude=float(alt_)/(0.3048)
        self.quality=nmeaSentenceQuality(int(quality_))
        self.satellites=int(numSV_)

    def GPRMC(self,raw_data_):
        print('GPRMC')
        (sentType_, time_, status_, lat_, NS_, lon_,
         EW_, spd_, track_, date_, mv_, mvEw_, posModw ) = raw_data_
        self.time = f'{time_[0:2]}:{time_[2:4]}:{time_[4:6]}'
        self.latitutue = round(float(lat_[0:2]) + (float(lat_[2:]) / 60), 8)
        self.longitude = -1 * round(float(lat_[0:3]) + (float(lat_[3:]) / 60), 8) if EW_ == 'W' else round(float(lat_[0:3]) + (float(lat_[3:]) / 60), 8)
        self.date=f'{date_[2:4]}/{date_[4:6]}/{date_[0:2]}'
        self.mv=float(mv_)
        self.mvEw_=mvEw_.strip()
        self.posMode=posModw.strip()

    def GPGSA(self,raw_data_):
        print('GPGSA')
        svid_=['']*13
        (sentType_, modeAutoMan_, modeFix_,
         svid_[1], svid_[2], svid_[3], svid_[4], svid_[5],svid_[6],
         svid_[7], svid_[8], svid_[9], svid_[10], svid_[11], svid_[12], *_) = raw_data_
        self.svid=sorted([item for item in svid_ if item])
        self.opMode=modeAutoMan_.strip()
        self.modeFix = nmeaGPGSmodeFix(int(modeFix_))

#------------------------------------------------------------------------------------------
#   Sample Data 
#   $GPVTG,260.0,T,267.3,M,1.1,N,2.0,K,A*25
#  
# Item       Description                                                  raw
# ------------------------------------------------------------------------------------------  
#   1      track made godo (degrees true)                                 track_
#   2      T: track made good is relative to true north         
#   3      Track made good (degrees magnetic)
#   4      M: track made good is relative to magnetic north
#   5      Speed, in knots
#   6      N: speed is measured in knots
#   7      Speed over ground in kilometers/hour (kph)
#   8      K: speed over ground is measured in kph
#   9      Mode indicator: 
#          A: Autonomous mode
#          D: Differential mode
#          E: Estimated (dead reckoning) mode
#          M: Manual Input mode
#          S: Simulator mode
#          N: Data not valid
#   10     The checksum data, always begins with *
#

    def GPVTG(self,raw_data_):
        print('GPVTG')
        #todo copplete this messaging
        (sentType_, track_, status_, trackmag_, NS_, spdKnots_,
         spdKnotsInd_, spdKph_, spdKphInd_, *_) = raw_data_
        self.track=trackmag_
        self.trackStatus=status_
        self.trackMagnetic=trackmag_
        self.trackMagneticStatus=NS_
        self.speedKnots=spdKnots_
        self.speedKnotsIndicator=spdKnots_
        self.speedKph=spdKph_
        self.speedKphIndicator=spdKphInd_


class nmeaFile():
    def __init__(self, in_file):
        filename = in_file.strip('"')

        print(f"\nOpening file {filename}...\n")
        with open(filename, "rb") as fstream:
            self.readFile(fstream, self.errhandler)
        print("\nProcessing Complete")


    def validateFile(self):
        pass


    def errhandler(err):
        """
        Handles errors output by iterator.
        """
        print(f"\nERROR: {err}\n")


    def readFile(self, stream, errorhandler):
        """
        Reads and parses UBX message data from stream.
        """

        msgcount = 0

        nmr = NMEAReader(stream)
        for (raw, parsed_data) in nmr.iterate(
                nmeaonly=False, quitonerror=False, errorhandler=errorhandler
        ):
            print(parsed_data)
            msgcount += 1

        print(f"\n{msgcount} messages read.\n")


#theFile='/media/racebannon/6233-100F/IC-r30/Gps/20220614_214205.log'
theFile='/media/racebannon/9C33-6BBD/IC-R30/Gps/20220617_195611.log'

ezR=EasyReader(theFile)

#myFile=nmeaFile(theFile)