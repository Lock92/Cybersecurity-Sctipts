# The goal of these decoys is primarily to act as a tripwire.
# there's no legitimate reason for a user to try to access
# or modify these decoys, meaning that any access to the decoys is probably malicious.

# Pathlib gives us access to the files, including access to the timestamps
# associated with them.
import pathlib 


# ctime=creation time, mtime = modification time
# atime = access time
def getTimestamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists():  # File deleted
        return []
    return(stats.st_ctime,stats.st_mtime,stats.st_atime)


def checkTimestamps(filename,create,modify,access):
    stats = getTimestamps(filename)
    if len(stats) == 0:
        return False # file deleted
    (ctime,mtime,atime) = stats
    if float(create) != float(ctime):
        return False # file creation time is incorrect
    if float(modify) != float(mtime):
        return False # file modify time is incorrect
    if float(access) != float(atime):
        return False # file acess time is incorrect
    return True
    

def checkDecoyFiles():
    with open("decoys.txt","r") as f:
        for line in f:
            vals = line.rstrip().split(",")
            if not checkTimestamps(vals[0],vals[1],vals[2],vals[3]):
                print("%s has been tampered with." % vals[0])


checkDecoyFiles()