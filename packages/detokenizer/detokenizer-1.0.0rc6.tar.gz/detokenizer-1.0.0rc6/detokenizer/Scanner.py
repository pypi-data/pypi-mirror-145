import io

class Scanner:

    def __init__(self, token, nextToken):
        self.token = token
        self.nextToken = nextToken

    def getToken(self):
        return self.token

    def getTokenLength(self):
        return len(self.token)

    def addChar(self, char):
        pass

    def nextScanner(self):
        pass

    def getData(self):
        pass


class ScannerText(Scanner):

    def __init__(self, token, nextToken):
        Scanner.__init__(self, token, nextToken)

        self.data = ""

    def addChar(self, char):
        self.data += char

    def nextScanner(self):
        return ScannerToken(self.nextToken, self.token)

    def getData(self):
        return self.data

class ScannerToken(Scanner):

    def __init__(self, token, nextToken):
        Scanner.__init__(self, token, nextToken)

        self.key = ""
        self.value = ""

    def addChar(self, char):
        self.key += char

    def nextScanner(self):
        return ScannerText(self.nextToken, self.token)

    def getData(self):
        return self.value

    def getKey(self):
        return self.key

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value
