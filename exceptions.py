class Errors(Exception):
    def languageNotSet(self):

        raise Errors('Language isn\'t set use setLanguage() and languages() to check list of avaiable langauges')

    def languageWrongValue(self):

        raise Errors('Provided language is not correct. Try to use languages() to check avaiable languages')
    
    def championWrongName(self):

        raise Errors('Provided champion value is not correct.')