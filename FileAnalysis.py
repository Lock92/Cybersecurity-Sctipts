import os, pathlib

def keywordCheck(filename):
    keywords = ["password"]
    return True in [k in filename.lower() for k in keywords]

def contentsCheck(filename):
    keywords = ["http",".com",".org",".net",".edu",".de",".gov",
                "facebook","twitter","gmail"]
    with open(filename,"r") as f:
        try:
            contents = f.read()
        except:
            return False
    return True in [k in filename.lower() for k in keywords]

threshold = 31269600
def usageCheck(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if (stats.st_atime - stats.st_mtime > threshold)\
        and (stats.st_mtime != stats.st_ctime):
        return True
    else:
        return False
    

def fileSearch(d):
    results = []
    for dirpath,_,files in os.walk(d):
        for filename in files:
            fname = os.path.join(dirpath,filename)
            if keywordCheck(fname) or usageCheck(fname):
                if contentsCheck(fname):
                    results.append(fname)
    return results

# directory = "C:\\Users\\hepos\\Documents"
directory = "/home/aaa/Documents"
results = fileSearch(directory)
for r in results:
    print(r)
