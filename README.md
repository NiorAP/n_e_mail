# E-Mail Library
by Nior.A.P

Python package use to send text, file via E-Mail

## Supported E-Mail provider
| Provider  | Code      |
| ---       | ---       |
| Gmail     | gmail     |
| Outlook   | hotmail   |
| Office365 | office365 |

## Install Library
```shell script
pip install git+https://github.com/NiorAP/n_e_mail.git
```

## Example
```python
from n_e_mail import EmailMessage
from n_e_mail import EMailServer

# Create E-mail object
message = EmailMessage("E-mail's subject")

# Add text to e-mail's body
message.add_message("E-mail's text body")

# Add file to e-mail
message.add_file('filename')


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
```