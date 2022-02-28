# psutil allow us to perform operations regarding the processes running on the windows system
import psutil

conn_counts = {}
totalConss = 0

# To detect which processes on the system could be expected to have network activity.
def buildBaseLine():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = int(len(proc.connections())) > 0 # will give us a list of the connections that a paticular process has.
        if name in conn_counts:
            (connected,total) = conn_counts[name]
            conn_counts[name] = (connected+hasConns,total+1)
        else:
            conn_counts[name] = (hasConns,1)
threshold = .5 
def checkConnections():
    for p in psutil.pids():
        proc = psutil.Process(p)
        name = proc.name()
        hasConns = int(len(proc.connections())) > 0 # will give us a list of the connections that a paticular process has.
        if hasConns:
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = connected/total
                if prob < threshold:
                    print("Process %s has network connection at %f probability" % (name,prob))
            else:
                print("New process %s has network connection" % name)
        else: # We also want to look at the case where something doesnt have a network connection and petentially should.
            # for example Firefox and chrome are very trusted processes on system.
            # this means that masquerading as Firefox or malware.
            if name in conn_counts:
                (connected,total) = conn_counts[name]
                prob = 1-(connected/total)
                if prob < threshold:print("Process %s doesn't have network connection at %f probability" % (name,prob))


buildBaseLine()
checkConnections()



