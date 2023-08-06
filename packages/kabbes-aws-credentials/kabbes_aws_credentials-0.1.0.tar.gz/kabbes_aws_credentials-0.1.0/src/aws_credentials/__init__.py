from . import AWS_Creds
from .update import update

import os
from dir_ops import dir_ops as do

Dir = do.Path( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
src_Dir = Dir.ascend()                                  #src Dir that is one above
repo_Dir = src_Dir.ascend()                             #root Dir for the actual repository

# Make the creds_Path exists
creds_Path = do.Path( Dir.join(  AWS_Creds.AWS_Creds.FILENAME  ) )
if not creds_Path.exists():
    creds_Path.create()

# Load the AWS_Creds instance
Creds = AWS_Creds.import_Creds( creds_Path.p ).Creds
# access a role's Credentials with aws_credentials.Creds[ role ]
