# --------------------------------------------------------------------------- #
#                              Import Libraries                               #
# --------------------------------------------------------------------------- #

import sys
from n_e_mail import EmailMessage, EMailServer

# --------------------------------------------------------------------------- #
#                             Unit Test Functions                             #
# --------------------------------------------------------------------------- #


def test_e_mail(provider: str, user: str, password: str):

    """Function that performs test on all command of
    EmailMessage and EmailServer class"""

    # Test create EmailMessage object
    message = EmailMessage('Test send email using python')
    # Test add message
    message.add_message('Test message')
    # Test add file
    message.add_file('NAP.jpg')

    # Test create EmailServer object
    server = EMailServer(provider, user, password)

    print('Test send email via normal procedure')
    if server.connect() == 'Success':
        print('Connection success')
        if server.send_mail(user, message) == 'Success':
            print('Send email success')
        else:
            print('Send email failed')
        print(server.disconnect())
    else:
        print('Connection failed')

    print('Test send quick email')
    print(server.quick_mail(user, message))

# --------------------------------------------------------------------------- #
#                               Main Executions                               #
# --------------------------------------------------------------------------- #


if __name__ == '__main__':

    # Get all command line arguments
    arg = sys.argv

    # Check if there are 4 arguments
    # (this filename, provider, email, and password) or not
    if len(arg) == 4:

        # Use credentials from the arguments
        print('Use given credentials')
        test_provider = arg[1]
        test_user = arg[2]
        test_password = arg[3]

        # Call unit test function
        test_e_mail(test_provider, test_user, test_password)

    else:
        # Invalid credentials, nothing to do
        print('Invalid credentials,',
              'specify email provider, email and password to test the process')

# --------------------------------------------------------------------------- #
