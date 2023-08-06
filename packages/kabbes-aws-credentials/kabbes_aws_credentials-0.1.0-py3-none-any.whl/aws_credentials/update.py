import py_starter.py_starter as ps
import aws_credentials
import time

def update():

    ### Using option 2 from the AWS console
    new_Cred = aws_credentials.AWS_Creds.AWS_Cred( string = ps.paste() )
    new_Cred.print_atts()

    if not new_Cred.role != None:
        print ()
        print ('------------')
        print ('ERROR: Errant AWS selection. Did not find correct format')
        print ('------------')
        print ()
        return False

    print()
    print ('Current Credentials at ' + str( aws_credentials.creds_Path.p ))
    og_Creds = aws_credentials.AWS_Creds.import_Creds( aws_credentials.creds_Path.p )
    #og_Creds.print_atts()

    print ()
    og_Creds.print_atts()
    og_Creds.add_new_Cred( new_Cred )

    print ('Writing merged credentials to ' + str( aws_credentials.creds_Path.p ))
    og_Creds.export_to_path( aws_credentials.creds_Path.p )

    print ()
    print ('------------')
    print ('SUCCESS: AWS Credentials successfully updated')
    print ('------------')
    print ()
    return True


if __name__ == '__main__':

    SUCCESS_SLEEPY_TIME = 0.5
    ERROR_SLEEPY_TIME = 5
    
    if update():
        time.sleep( SUCCESS_SLEEPY_TIME )
    else:
        time.sleep( ERROR_SLEEPY_TIME )
