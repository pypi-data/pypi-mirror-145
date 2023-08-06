from parent_class import ParentClass

BEGIN_ROLE = '['
END_ROLE = ']'

class AWS_Cred (ParentClass) :

    """Class for storing one instance of a singular AWS Role and its associated credentials
    role: AWS role associated 
    dict: contains each key-value combination for each environment variable and its value
    string: contains a string representation of the dictionary, "key=value"
    """

    def __init__( self, role = None, dict = {}, string = ''):

        """If initialized with a dict, role must be provided
        if initialized with a string, the role must be contained in [square brackets up to]"""

        ParentClass.__init__( self )

        self.role = role
        self.dict = dict
        self.string = string

        if string != '' and dict == {}:
            self._string_to_dict()
        elif dict != {} and string == '':
            self._dict_to_string()
        elif string == '' and dict == {}:
            #Not given credentials string or dictionary
            pass

    def print_imp_atts( self, **kwargs ):

        return self._print_imp_atts_helper( atts = ['role','string','dict'], **kwargs )

    def print_one_line_atts( self, **kwargs ):

        return self._print_one_line_atts_helper( atts = ['type','role'], **kwargs )

    def _dict_to_string( self ):

        """turns the Creds dictionary into a string"""

        lines = [ BEGIN_ROLE + str(self.role) + END_ROLE ]

        for key in self.dict:
            value = self.dict[key]
            lines.append(str(key) + '=' + str(value) )

        string = '\n'.join(lines)
        self.string = string
        return string

    def _string_to_dict( self ):

        """turns the dictionary of the creds into a string"""

        role_dict = {}
        role = None

        for line in self.string.split( '\n' ):

            line = line.strip()

            if line == '':
                continue

            elif line_is_role( line ):
                role = get_role_from_line( line )
                self.role = role

            else:
                if role != None:
                    key, value = get_key_value_from_line( line )
                    role_dict[key] = value

        self.dict = role_dict
        return role_dict

class AWS_Creds (ParentClass) :

    """A class that contains all possible AWS Roles and their respective credentials
    Creds: Dictionary where key is a role and value is an AWS_Cred class instance
    string: string which contains the exported version of the AWS_Creds"""

    FILENAME = 'aws_creds.txt'

    def __init__( self, list_of_Creds = []):

        ParentClass.__init__( self )

        self.Creds = {} #key is the role, value is the AWS_Cred object
        self.string = ''

        for Cred in list_of_Creds:
            self.Creds[ Cred.role ] = Cred

        self._Creds_to_string()

    def print_imp_atts( self, print_off = True ):

        string = self.print_class_type(print_off = False) + '\n'
        string += 'Creds:\n'

        for role in self.Creds:
            string += ( self.Creds[role].print_one_line_atts(print_off=False) + '\n' )
        string = string[:-1]

        return self.print_string( string, print_off = print_off )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['type'], print_off = print_off, leading_string = leading_string )

    def _Creds_to_string( self ):

        """Export all the Cred objects to string, concat into one big string"""

        string = ''
        for role in self.Creds:
            string += self.Creds[role].string + '\n'

        self.string = string

    def add_new_Cred( self, new_Cred ):

        """take a new Creds class instance, and add/overwrite the existing credentials"""

        if new_Cred.role not in self.Creds:
            self.Creds[ new_Cred.role ] = new_Cred

        self.Creds[ new_Cred.role ].dict = new_Cred.dict
        self.Creds[ new_Cred.role ]._dict_to_string()

    def export_to_path( self, path ):

        """export the string contents to a given text file"""

        self._Creds_to_string()

        file = open( path, 'w' )
        file.write( self.string )
        file.close()

    def get_Cred_from_role( self, Cred_role ):

        if Cred_role in self.Creds:
            return self.Creds[Cred_role]
        else:
            print ('Could not find role ' + str(Cred_role) + ' in AWS_Creds object')
            return None

    def import_from_path( self, path ):

        """read the contents of a text file, populate the Creds dictionary with all roles"""

        file = open( path, 'r' )

        lines = []
        for line in file.readlines():
            lines.append( line.strip() )

        ### Loop through each line
        role_dict = {}
        current_role = None

        for i in range(len(lines)):

            line = lines[i].strip()

            if line_is_role( line ):

                #First, export the current role if it exists
                if current_role != None:
                    self.add_new_Cred( AWS_Cred( role = current_role, dict = role_dict ) )

                role_dict = {}
                current_role = get_role_from_line( line )

            elif line_is_key_value( line ):
                if current_role != None:
                    key, value = get_key_value_from_line(line)
                    role_dict[key] = value

        # after looping through all lines, export the current Cred info
        if current_role != None:
            self.add_new_Cred( AWS_Cred( role = current_role, dict = role_dict ) )

        self._Creds_to_string()


def is_Cred( Cred_inst ):

    """returns a boolean if the Cred instance is of type AWS_Cred"""

    return type(Cred_inst) == type(ex_Cred)

def is_Creds( Creds_inst ):

    """returns a boolean if the Cred instance is of type AWS_Creds"""

    return type(Creds_inst) == type(ex_Creds)

def line_is_role( line ):

    """If given a role like [AWS_ROLE-1234], return TRUE"""

    if line[0] == BEGIN_ROLE and line[-1] == END_ROLE:
        return True
    return False

def line_is_key_value( line ):

    """If given a line like "key=value", return True"""

    if '=' in line:
        return True
    return False

def get_role_from_line( line ):

    """Given [AWS_ROLE-1234], return AWS_ROLE-1234"""

    return line[ len(BEGIN_ROLE) : -1*len(END_ROLE) ]

def get_key_value_from_line( string ):

    """Takes a string, splits by the FIRST equal sign and sets it equal to key, value
    aws_session_token=1234ASDF=B returns ("aws_session_token", "1234ASDF=B") """

    split_by_equal = string.split('=')
    key = split_by_equal[0]

    if len(split_by_equal) > 1:
        value = '='.join( split_by_equal[1:] )
    else:
        value = None

    return key, value

def import_Creds( path ):

    """import the Creds object from a given path"""

    Creds = AWS_Creds()
    Creds.import_from_path( path )
    return Creds

def import_Cred( role, path = '', Creds = None ):

    """import the Cred object from a given path and specifying a role"""

    if Creds == None:
        Creds = import_Creds( path )

    return Creds.get_Cred_from_role( role )

ex_Cred = AWS_Cred()
ex_Creds = AWS_Creds()
