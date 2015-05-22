import urllib, hashlib, os, time, string, re

#Setting up a dict that will be used
#throughout the script, and a variable 
#for the directory in which the text files 
#containing the information for each target 
#(i.e. url, hash, etc.) are kept
targetInfo = {}
targetdir = "targets/"

class Check(object):

    def __init__(self):
        #Print the time the script is started to the 
        #update log
        s = time.localtime()
        q = open("updatelog.txt", "a")
        q.write("*** Updater started at: " + str(s[0]) + '/' + str(s[1]) + '/' + str(s[2]) + '-' + str(s[3]) + ':' + str(s[4]) + " ***" + "\n")
        q.close()
        while True:
            #Check all the sites, then sleep
            self.updateCheck()
            time.sleep(60)

    #The function for reading in the information for each 
    #target to be checked, and putting that information into 
    #the dict targetInfo
    def readTargetInfo(self, targetfile):
        f = open(targetfile)
        temp = f.readline()
        while temp != "":
            #The lines read in from the target file are split
            #along the index ": "
            index = temp.find(": ")
            if index != -1:
                targetInfo[temp[:index]] = temp[index+2:len(temp)-1]
            temp = f.readline()
        f.close()
    
    #The function for writing the updated target information
    #(often just the updated hash) out to the target file
    def writeTargetInfo(self, targetfile):
        g = open(targetfile, "w")
        for name, value in targetInfo.iteritems():
            g.write(name+": "+value)
            g.write("\n")
        g.close()

    #The function for opening the page, searching for 
    #the desired element, then hashing it for comparison
    #to the stored hash
    def getHash(self, site, element, hash):
        n = urllib.urlopen(site)
        page = n.read()
        #If there is no specific element you care 
        #about, you can set the "Element" line in 
        #the target file to "Whole Page" and it will 
        #just hash the entire page
        if element == 'Whole Page':
            m = hashlib.md5()
            m.update(page)
            slack = m.hexdigest()
        else:
            #Search for the element (a regex pattern saved 
            #in the target file) in the page. The re.DOTALL 
            #option causes the search to treat "." as matching 
            #any character /including/ newlines, whereas it 
            #would normall not match newlines
            result = re.search(element, page, re.DOTALL)
            print result
            if result:
                nugget = result.group(1)
                print 'nugget: '+nugget
                m = hashlib.md5()
                m.update(nugget)
                slack = m.hexdigest()
            else:
                slack = hash
        #Slack was chosen as the variable name for the old 
        #hash with the following logic:
        #hack 'n slash -> slack 'n hash
        print slack
        return slack

    def updateCheck(self):
        #Get the list of files in the 
        #target directory set at the top 
        #of the script
        targetlist = os.listdir(targetdir)

        for target in targetlist:
            isUpdate = False
            print isUpdate
            #Get the contents of the target file and 
            #use that to fill the targetInfo dict
            self.readTargetInfo(targetdir+target)

            #Setting some variables for less typing in the 
            #following lines
            site = targetInfo['URL']
            element = targetInfo['Element']
            hash = targetInfo['Hash']
            
            print targetInfo
            print 'site: '+site
            print 'element: '+element
            print 'hash: '+hash
            
            #Get the page of the target site, search for the 
            #desired element, then hash it
            slack = self.getHash(site, element, hash)
            
            #Compare the new and old hashes to determine if the 
            #site has updated
            if slack != hash:
                isUpdate = True
                print isUpdate
                
                #Print out the url that has updated and the 
                #time that the update was discovered to the 
                #update log
                t = time.localtime()
                p = open("updatelog.txt", "a")
                p.write(str(t[0]) + '/' + str(t[1]) + '/' + str(t[2]) + '-' + str(t[3]) + ':' + str(t[4]) + " " + site + " has updated" + "\n")
                p.close()
                #Set the new hash as the hash value in the 
                #targetInfo dict
                targetInfo['Hash'] = slack

            if isUpdate == True:
                #Write out the updated target info
                #(probably all that has changed is the 
                #hash)
                self.writeTargetInfo(targetdir+target)
            


check = Check()
