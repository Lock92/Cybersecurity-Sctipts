# Analyzing the contents of outlooks, stored data file
# containing emails on our local machine.
# This is PST file format on a computer
# We will use library libratom.lib.pff for parsing pst file
# This PffArchive defines the structire of a PST file,
# Allowing us to very easily access the data inside of it,
# iterate through it, and take a look at the contents of the message
# is stored in an outlook data file.

from libratom.lib.pff import PffArchive

filename = "C:\\Users\\hepos\\Documents\\Outlook Files\\howard@howardposton.com.pst"
archive = PffArchive(filename)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            print("Sender: %s" % message.get_sender_name())
            print("Subject: %s" % message.get_subject())
            print("Message: %s" % message.get_plain_nect_body())

# We can also access the HTML body of the message
