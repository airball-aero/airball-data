
class ProbeFixture:
    '''Represents a probe on a test fixture.'''

    def __init__(self):
        pass

    def moveto(self, az_el):
        '''Move probe to a given azimuth and elevation in degrees.'''
        pass

    def read(self, n):
        '''Read a given number of $A data sentences. Returns a list of strings.'''
        pass
