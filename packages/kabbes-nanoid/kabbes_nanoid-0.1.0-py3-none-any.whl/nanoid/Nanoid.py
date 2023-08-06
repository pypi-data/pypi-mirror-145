from parent_class import ParentClass
import random

class Nanoid( ParentClass ):

    """Nanoid class used for generating a NanoID"""

    DEFAULT_ALPHABET = '-_1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    DEFAULT_SIZE = 21

    def __init__( self, alphabet = DEFAULT_ALPHABET, size = DEFAULT_SIZE ):

        """Initializes the class with default attributes"""

        ParentClass.__init__( self )

        self.alphabet = alphabet
        self.size = size
        self.nanoid = None

        #Generate the NanoID string
        self.generate()

    def print_imp_atts(self, **kwargs):

        return self._print_imp_atts_helper( atts= ['nanoid','size','alphabet'], **kwargs )

    def print_one_line_atts(self, **kwargs):

        return self._print_one_line_atts_helper( atts = ['type','nanoid'], **kwargs )  

    def generate( self ):

        """Generates a Nanoid from stored 'size' and 'alphabet' attributes, stores in 'nanoid' attribute """

        string = ''
        for i in range(self.size):
            string += ( random.choice( self.alphabet ) )

        self.nanoid = string


def generate( **kwargs ):

    """generates a Nanoid class and returns the nanoid attribute"""

    return Nanoid( **kwargs ).nanoid

