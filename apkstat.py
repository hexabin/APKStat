import xml.sax
import sys
import os

class ManifestReader(xml.sax.ContentHandler):
   # Control Variables
   isActivityOpen=False;
   currentActivityName="";
   launcherActivity=""

   # Number of Classes Variables
   numberOfActivities=0
   numberOfReceivers=0
   numberOfServices=0
   numberOfProviders=0
   numberOfActivityAliases=0
   numberOfPermissionsRequested=0

   # File and Report Variables
   report = ""
   apkfilename=""
   truefilename = ""
   manifestlocation = ""

   # Arrays for storing names of important classes
   activityNames=['']
   serviceNames=['']
   providerNames=['']
   receiverNames=['']
   activityaliasnames=['']
   permissionNames=['']

   def __init__(self):
      # Track File and Folder Names
      self.apkfilename = ""
      self.truefilename = ""

      # Check The State Of The Activity Element
      self.isActivityOpen=False;

      # Track the Launcher Activity
      self.currentActivityName=""
      self.launcherActivity=""
      self.manifestlocation = ""

      # Track the number of important classes
      self.numberOfActivities=0
      self.numberOfReceivers=0
      self.numberOfServices=0
      self.numberOfProviders=0
      self.numberOfActivityAliases=0
      self.numberOfPermissionsRequested=0

      # Track The Names Of Important Classes in Arrays
      self.activityNames = ['']
      self.serviceNames=['']
      self.providerNames=['']
      self.receiverNames=['']
      self.activityAliasNames=['']
      self.permissionNames=['']

      # Create A Report File Object To Write Output To
      self.report = open("report.txt", "a")

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag

      # If In Android Manifest Increment Counter
      if (tag == "activity"):
          self.isActivityOpen=True
          self.numberOfActivities = self.numberOfActivities + 1

      if (tag == "receiver"):
          self.numberOfReceivers = self.numberOfReceivers + 1

      if (tag == "service"):
          self.numberOfServices = self.numberOfServices + 1

      if (tag == "provider"):
          self.numberOfProviders = self.numberOfProviders + 1

      if (tag == "activity-alias"):
          self.numberOfActivityAliases = self.numberOfActivityAliases + 1

      if (tag == "uses-permission"):
	  self.numberOfPermissionsRequested = self.numberOfPermissionsRequested + 1

      try:
          # If Name is Available Add To Array
          if(attributes["android:name"] != ""):
	      if (tag=="activity"): 
	          self.currentActivityName= attributes["android:name"]
                  self.activityNames.append(attributes["android:name"])
              elif (tag=="service"):
		  self.serviceNames.append(attributes["android:name"])
	      elif (tag=="receiver"):
                  self.receiverNames.append(attributes["android:name"])
              elif (tag=="provider"):
                  self.providerNames.append(attributes["android:name"])
              elif (tag=="activity-alias"):
		  self.activityAliasNames.append(attributes["android:name"])
              elif (tag=="uses-permission"):
                  self.permissionNames.append(attributes["android:name"])
      except:
	  print ""

      if (tag == "action"):
          # Check If An Activity Is Open
          if (self.isActivityOpen):
             try:
                 # If within an Activity and is the Main we have the Launcher
	         if (attributes["android:name"]=="android.intent.action.MAIN"):
		     self.launcherActivity = self.currentActivityName
             except:
                  print ""

   # Call when an elements ends
   def endElement(self, tag):
        # If an Activity then close it
	if (tag == "activity"):
	    self.isActivityOpen=False
	    currentActivityName=""

   def writeURLsAndIPs(self):
        #Listing all domains and IPs found
        print "\n[3] Listing All Domains Found:\n"
        print ""

        # Grep Domains and IPs from the APK file
        cmd = "grep -oE '[[:alnum:]]+[.][[:alnum:]_.-]+' " + self.apkfilename + " | sed 's/www.//' >> domains.txt"
        os.system(cmd)

        # Write the domains and IPs found to report (if any)
	self.report.write("\n\n Domains & IPs Extracted From Strings\n")
        domainText = open("domains.txt", 'r')
        for lines in domainText:
            if "Binary file" not in lines:
                self.report.write(lines + "\n")
                print "\n\n Domains: " + lines

        os.system("rm domains.txt")
        self.report.close()

   def printStats(self):
       # Print Stats On Screen At Completion
       print "\n[1] Overall Stats \n"
       print "Number Of Permissions Requested: " + str(self.numberOfPermissionsRequested)
       print "Number Of Activities: " + str(self.numberOfActivities)
       print "Number Of Receivers: " + str(self.numberOfReceivers)
       print "Number Of Providers: " + str(self.numberOfProviders)
       print "Number Of Services: " + str(self.numberOfServices)
       print "Number Of Activity Aliases: " + str(self.numberOfActivityAliases)
       print ""
       print "[2] Launcher Activity\n"
       print "Launcher Activity: " + self.launcherActivity

   def writeActivitiesToReport(self):
       # Write Activity Names To Report
       self.report.write("\n\n Names Of Activities:\n")

       for name in self.activityNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writeReceiversToReport(self):
       # Write Receiver Names To Report
       self.report.write("\n\n Names Of Receivers:\n")

       for name in self.receiverNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writeServicesToReport(self):
       # Write Service Names To Report
       self.report.write("\n\n Names Of Services:\n")

       for name in self.serviceNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writeProvidersToReport(self):
       # Write Provider Names To Report
       self.report.write("\n\n Names Of Providers:\n")

       for name in self.providerNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writeActivityAliasesToReport(self):
       # Write Activity Aliases To Report
       self.report.write("\n\n Names Of Activity Aliases:\n")

       for name in self.activityAliasNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writePermissionsToReport(self):
       # Write Permission Requests to Report
       self.report.write("\n\n Permissions Requested:\n")

       for name in self.permissionNames:
           if(name != ""):
               self.report.write(name + "\n")

   def writeReport(self):
       # Write Stats To Report
       self.report.write("Number Of Permissions Requested: " + str(self.numberOfPermissionsRequested) + "\n")
       self.report.write("Number Of Activities: " + str(self.numberOfActivities) + "\n")
       self.report.write("Number Of Receivers: " + str(self.numberOfReceivers) + "\n")
       self.report.write("Number Of Providers: " + str(self.numberOfProviders) + "\n")
       self.report.write("Number Of Services: " + str(self.numberOfServices) + "\n")
       self.report.write("Number Of Activity Aliases: " + str(self.numberOfActivityAliases) + "\n\n")
       self.report.write("Launcher Activity: " + self.launcherActivity + "\n\n")

   def createStringsFile(self):
       # Create a Strings File from APK
       os.system("strings " + self.apkfilename + " >> strings.txt")
       print "\n[*] Strings Files Created: strings.txt\n"

   def openAPK(self):
        #set the apkfilename and storage directory of decompressed apk globally
        print "[*] Decompressing APK Using APKTool\n"
        unzip_apk_str = "apktool d " + self.apkfilename
        os.system(unzip_apk_str)

        # Remove the .apk for the true filename
        self.truefilename = self.apkfilename[0:-4]
        self.manifestlocation = self.truefilename + "/AndroidManifest.xml"

   def getManifestLocation(self):
        # Return the location to the AndroidManifest.xml
        return self.manifestlocation

   def setAPKFilename(self, filename):
        # Set the APK Filename
        self.apkfilename=filename

   def displayUsage(self):
        # Display Usage Information
        print "Usage: python apk-stats.py yourfile.apk\n\n"
        exit()


if ( __name__ == "__main__"):

   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = ManifestReader()

   # Set XML Parser
   parser.setContentHandler( Handler )

   # Introduction Header
   print "                \n\nAPKSTAT v1.0 - by Hexabin  (T: @TheRealHexabin)\n\n"

   # Check if there is a filename in the argument
   if (len(sys.argv)==2):
       Handler.setAPKFilename(str(sys.argv[1]))
   else:
       Handler.displayUsage()

   # Open the APK using APKTool
   Handler.openAPK()

   # Parse the AndroidManifest.xml
   parser.parse(Handler.getManifestLocation())

   # Print Stats On Screen
   Handler.printStats()

   # Write Report
   Handler.writeReport()
   Handler.writePermissionsToReport()
   Handler.writeActivitiesToReport()
   Handler.writeServicesToReport()
   Handler.writeReceiversToReport()
   Handler.writeProvidersToReport()
   Handler.writeActivityAliasesToReport()

   # Write Domains and IPs to Report
   Handler.writeURLsAndIPs()

   # Create Strings File
   Handler.createStringsFile()

   print "\n\n[*] Report Created : report.txt\n"
