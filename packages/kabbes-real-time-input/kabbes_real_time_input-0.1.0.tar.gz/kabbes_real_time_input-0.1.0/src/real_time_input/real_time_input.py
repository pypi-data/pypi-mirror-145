from parent_class import ParentClass
import platform
import sys

key_mapping = {
  'Windows': {
    '\r': 'ENTER', #all values need to be longer than one character to not confuse with an input
    '\t': 'TAB',
    '\x08': 'BACKSPACE'
  },
  'Darwin': {
    '\n': 'ENTER',
    '\t': 'TAB',
    '\x7f': 'BACKSPACE',
    '\x1b': 'ESCAPE'
  }
}

# First, see what kind of platform we are running on
platform_system = platform.system()
if platform_system == 'Darwin' or platform_system == 'Linux': # Linux and Mac behave the same
    platform_system = 'Darwin'
    import termios
    import tty

elif platform_system == 'Windows':
    import msvcrt

phonetic_alphabet = ['alpha','bravo','charlie','delta','echo','foxtrot','golf','hotel',
    'india','juliett','kilo','lima','mike','november','oscar','papa','quebec','romeo',
    'sierra','tango','uniform','victor','whiskey','xray','yankee','zulu']


class RealTimeInput( ParentClass ):

    def __init__(self, **kwargs):

        ParentClass.__init__( self )
        self.catalog = phonetic_alphabet

        self.set_atts( kwargs )
        self.platform_system = platform_system

    def get_input( self, return_raw_key = False ):

        '''returns the key that was pressed by the user, function does not terminate until a key is pressed'''

        def Darwin():

            filedescriptors = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
            key = sys.stdin.read(1)[0]
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN,filedescriptors)
            return key

        def Windows():

            while True:
                if msvcrt.kbhit(): #key is pressed
                    key = msvcrt.getwch() #decode
                    return key

        #call Darwin() or Windows()
        key = eval( self.platform_system + '()' )

        # if given that is contained in key_mappings
        if key in key_mapping[ self.platform_system ] and not return_raw_key:
            return key_mapping[ self.platform_system ][ key ] #returns ENTER, TAB, etc.

        # something was input that is not in key_mapping, like a regular character
        else:
            return key

    def show_key_encoding( self ):

        '''to find what key values are in your operating system, execute this function'''

        key = self.get_input( return_raw_key = True )
        print ('KEY PRESSED: ' + str(key))

        key_encoded = key.encode('utf-8')
        print ('KEY ENCODED: ' + str(key_encoded))

    def prepare_autocomplete( self ):

        '''returns the string which shows the autocomplete prompt'''

        if len(self.suggestions) == 0:
            self.display = self.string + ' - (0)'

        else:
            self.display = '{string} - ({i}/{n}) - {suggestion}'.format( string = self.string, i = self.suggestion_index+1, n = len(self.suggestions), suggestion = self.suggestions[self.suggestion_index] )

    def search( self ):

        '''returns a list of strings contained in "catalog" which contain "string" '''

        self.suggestions = []
        if len(self.string) > 0:
            for word in self.catalog:
                if self.string.lower() in word.lower():
                    self.suggestions.append( word )

    def print_updated( self ):

        '''overwrites the contents of the screen from the last time something was printed'''

        blank = ' ' * len(self.prior_display)
        print (blank, end = '\r')
        print (self.display, end = '\r')

    def get_one_input( self ):

        self.suggestion_index = 0
        self.string = ''
        self.prior_display = ''
        self.suggestions = []

        while True:

            key = self.get_input()

            #input is a key code
            if len(key) > 1:
                if key == 'ENTER':
                    break
                elif key == 'TAB':
                    self.suggestion_index += 1
                elif key == 'BACKSPACE':
                    self.string = self.string[:-1]
                    self.suggestion_index = 0
                else:
                    pass

            #input was a regular string
            else:
                self.suggestion_index = 0
                self.string += key

            # find which words contain "string"
            self.search()
            if len(self.suggestions) > 0:
                self.suggestion_index = self.suggestion_index % len(self.suggestions)

            # prepare autocomplete and display the feedback
            self.prepare_autocomplete()
            self.print_updated()
            self.prior_display = self.display

        print ()
        if len(self.suggestions) > 0:
            self.suggestion = self.suggestions[self.suggestion_index]
        else:
            self.suggestion = None

        return  self.suggestion, self.string

    def get_multiple_inputs( self ):

        '''given a list of strings to be searched, let the user search for the words using autocomplete'''

        self.selections = []
        while True:

            self.suggestion, self.string= self.get_one_input()

            if self.suggestion != None:
                self.selections.append( self.suggestion )
                print ('Adding new selection: ' + str(self.suggestion) )

            else:
                break

        return self.selections, self.string

if __name__ == '__main__':

    rti = RealTimeInput()
    rti.get_multiple_inputs()
