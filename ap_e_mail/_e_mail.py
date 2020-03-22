# --------------------------------------------------------------------------- #
#                              Import Libraries                               #
# --------------------------------------------------------------------------- #

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from ap_e_mail._settings import settings

# --------------------------------------------------------------------------- #
#                              Class Definitions                              #
# --------------------------------------------------------------------------- #


class EmailMessage:

    """
    An object that stores email data including subject, body and files
    It has add_message, add_file and compile methods

    Parameter(s):
        subject : Subject of the e-mail

    Examples    :
        from ap_e_mail import EmailMessage

        # Create E-mail object
        message = EmailMessage("E-mail's subject")

        # Add text to e-mail's body
        message.add_message("E-mail's text body")

        # Add file to e-mail
        message.add_file('filename')
    """

    # Initial Method, Only save the message's subject
    def __init__(self, subject=None) -> None:

        self.subject = subject

        self.__object = []
        self.__email_message = None

    # ----------------------------------------------------------------------- #
    # Real Add Message Private Method, add message to MIMEMultipart object
    def __add_message(self, email_message: MIMEMultipart, message: str) \
            -> None:

        email_message.attach(MIMEText(message))

    # ----------------------------------------------------------------------- #
    def add_message(self, message: str) -> None:

        """
        Method use to add text to e-mail body
        Argument(s):
            message     : [String] Text to add
        """

        self.__object.append((self.__add_message, message))

    # ----------------------------------------------------------------------- #
    # Real Add File Private Method, add file to MIMEMultipart object
    def __add_file(self, email_message: MIMEMultipart, filename: str) -> None:

        with open(filename, 'rb') as file:

            part = MIMEApplication(file.read())

            part.add_header('Content-Disposition',
                            f'attachment; filename={filename}')

            email_message.attach(part)

    # ----------------------------------------------------------------------- #
    def add_file(self, filename: str) -> None:

        """
        Method use to add file to e-mail body
        Argument(s):
            filename    : [String] path to file to add
        """

        self.__object.append((self.__add_file, filename))

    # ----------------------------------------------------------------------- #
    def compile(self, sender: str, receiver: str) -> str:

        """
        Method use to compile everything specified before and
        return string that ready to send

        If you use EmailServer you don't have to call this because
        this is called by EmailServer already

        Argument(s):
            sender      : [String] e-mail of sender (from)
            receiver    : [String] e-mail of receiver (to)

        Return     :
            [String] string that ready to send by smtp server
        """

        self.__email_message = MIMEMultipart()
        self.__email_message['From'] = sender
        self.__email_message['To'] = receiver
        self.__email_message['Subject'] = self.subject

        for method, value in self.__object:
            method(self.__email_message, value)

        result = self.__email_message.as_string()

        del self.__email_message
        self.__email_message = None

        return result

# --------------------------------------------------------------------------- #


class EMailServer:

    """
    An object that stores e-mail's provider, user and password
    It has connect, disconnect, send_mail and quick_mail methods

    Supported E-mail provider:
        | Provider  | Code      |
        | ---       | ---       |
        | Gmail     | gmail     |
        | Outlook   | hotmail   |
        | Office365 | office365 |

    Parameter(s):
        provider    : E-mail provider
        user        : E-mail
        password    : E-mail's password

    Example     :
        # Create Server object
        server = EMailServer('E-mail provider code', 'e-mail', 'password')

        # 1st style: Send quick e-mail
        server.quick_mail("Receiver's e-mail", 'EmailMessage object')

        # 2nd style: connect, send, close (good with multiple email send)
        # Connect to smtp server
        server.connect()

        # Send e-mail
        server.send_mail("Receiver's e-mail", 'EmailMessage object')

        # Disconnect smtp server
        server.disconnect()
    """

    # Initial Method, save provider, e-mail and password
    def __init__(self, provider: str, user: str, password: str) -> None:
        self.provider = provider
        self.user = user
        self.password = password
        self.__server = None

    # ----------------------------------------------------------------------- #
    def connect(self) -> str:

        """
        Method use to connect to prior specified smtp server and login with
        prior specified e-mail address and password
        """

        self.__server = smtplib.SMTP(settings['server_smtp'][self.provider],
                                     587)

        if self.__server.starttls()[0] == 220:

            login_result = self.__server.login(self.user, self.password)

            if login_result[0] == 235:
                return 'Success'
            else:
                return login_result[1]

        else:
            return 'Connection failed'

    # ----------------------------------------------------------------------- #
    def disconnect(self):

        """
        Method use to disconnect the connected smtp server
        """

        status = self.__server.quit()

        self.__server = None

        if status[0] == 221:
            return 'Success'

        else:
            return status[1]

    # ----------------------------------------------------------------------- #
    def send_mail(self, to: str, message: EmailMessage) -> str:

        """
        Method use to send e-mail to "connected" smtp server

        Argument(s) :
            to          : [String] e-mail of the receiver (to)
            message     : [EmailMessage] message to send
        """

        result = self.__server.sendmail(self.user, to,
                                        message.compile(self.user, to))

        if result == {}:
            return 'Success'
        else:
            return 'Send email failed'

    # ----------------------------------------------------------------------- #
    def quick_mail(self, to: str, message: EmailMessage):

        """
        Method use to send quick e-mail
        This wrap-up connect, send_mail and disconnect into 1 method
        This is better when you want to send only 1 at a time

        Argument(s) :
            to          : [String] e-mail of the receiver (to)
            message     : [EmailMessage] message to send
        """

        if self.connect() == 'Success':

            result = self.send_mail(to, message)

            self.disconnect()

            return result

        else:
            return 'Connection failed'

# --------------------------------------------------------------------------- #
#                             Unit Test Functions                             #
# --------------------------------------------------------------------------- #


def test_e_mail(provider: str, user: str, password: str):

    """Function that performs test on all command of
    EmailMessage and EmailServer class"""

    # Create some text file use as test file to send with e-mail
    with open('test_file.txt', 'w') as file:
        file.writelines(['This file is generated by ap_e_mail.',
                         'Use to test send file via email only.'])

    # Test create EmailMessage object
    message = EmailMessage('Test send email using python')
    # Test add message
    message.add_message('Test message')
    # Test add file
    message.add_file('test_file.txt')

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

    # Remove test file we've created before
    os.remove('test_file.txt')

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
