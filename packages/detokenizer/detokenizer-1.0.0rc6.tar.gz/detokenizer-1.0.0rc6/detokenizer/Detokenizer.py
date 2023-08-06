import os
import io
import sys
import argparse
import yaml

from timeit import default_timer as timer


import detokenizer as meta
from detokenizer.Scanner import ScannerText, ScannerToken

class Detokenizer:
    def __init__(self):

        args = self.parserCommandLine()

        self.chrono = timer()

        print(meta.__name__ + ' ' + meta.__version__)
        print("Source file: " + self.sourceFile)
        print("Config file: " + self.configFile)
        print("Properties: " + self.propFile)

        self.loadConfig()

        self.properties = {}
        self.loadProperties()

        print("Tokens: " + self.startToken + "..." + self.endToken)

        self.scanners = []

        self.parseSource()
        self.injectProperties()
        self.writeOutput()

        print( meta.__name__ +
                ' processing finished: %.5f seconds' %
                (timer() - self.chrono))


    def parserCommandLine(self, additionalArgs=[]):
        parser = argparse.ArgumentParser(description="detokenizer")

        parser.add_argument('-v', '--version', action='version',
                            version=meta.__version__)

        parser.add_argument(dest="source", help="Source file")
        parser.add_argument(dest="target", help="Output file")
        parser.add_argument(dest="config", help="Configuration file")
        parser.add_argument(dest="properties", help="Properties file")

        for arg in additionalArgs:
            parser.add_argument(**arg)

        args = parser.parse_args()

        self.configFile = self.buildFullPath( args.config)
        self.sourceFile = self.buildFullPath( args.source)
        self.targetFile = self.buildFullPath( args.target)
        self.propFile = self.buildFullPath( args.properties)

    def buildFullPath(self, filepath):
        return os.path.join(os.getcwd(), filepath)

    def loadConfig(self):
        filename = os.path.normpath(self.configFile)
        try:
            with open(filename, encoding='utf-8') as data_file:
                data = yaml.load(data_file, Loader=yaml.FullLoader)

                self.startToken = data['start-token']
                self.endToken = data['end-token']
        except Exception as e:
            print("Could not read yaml file: " + str(e))
            raise

    def loadProperties(self):
        filename = os.path.normpath(self.propFile)
        try:
            propertiesFile = open(filename, "r", encoding='utf-8')

        except Exception as e:
            print("Could not read properties file: " + str(e))
            raise


        while True:
            line = propertiesFile.readline()
            if line == '':
                break

            if '=' in line:
                pair = line.split('=',1)
                self.properties[pair[0]] = pair[1].rstrip()



    def parseSource(self):
        filename = os.path.normpath(self.sourceFile)
        try:
            self.sourceStream = open(filename, "r", encoding='utf-8')

        except Exception as e:
            print("Could not read source file: " + str(e))
            raise

        pos = 0
        scanner = ScannerText(self.startToken, self.endToken)
        while True:
            self.sourceStream.seek(pos)
            scan = self.sourceStream.read(scanner.getTokenLength())

            if scan == scanner.getToken():
                self.scanners.append(scanner)
                pos += scanner.getTokenLength()
                scanner = scanner.nextScanner()
            elif scan == '':
                self.scanners.append(scanner)
                break
            else:
                scanner.addChar(scan[0])
                pos += 1

    def injectProperties(self):
        for scanner in self.scanners:
            if isinstance(scanner, ScannerToken):
                scanner.setValue(self.properties[scanner.getKey()])


    def writeOutput(self):

        targetfolder = os.path.split(self.targetFile)[0]
        print(targetfolder)

        if not os.path.exists(targetfolder):
            os.mkdir(targetfolder)

        with open( self.targetFile, 'w') as outfile:
            for scanner in self.scanners:
                outfile.write(scanner.getData())
