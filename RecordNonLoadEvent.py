import sys
import argparse
from Quaternion import Quat
import Ska.Sun
import numpy as np

################################################################################
#
# Program RecordNonLoadEvent.py - This program is called by History-files.pl 
#                                 whenever it is run for a too, scs-107, stop
#                                 Then, given a set of arguments, this program
#                                 updates the  NonLoadTrackedEvents.txt file
#                                 with the supplied event parameters. Ir 
#                                 appends the information onto the end of the
#                                 file in the appropriate format. 
#
# From the history-files.pl input arguments, you will have the event types:
#   s107  - Science load only halted (SCS-107 for Rad reasons)
#   stop  - Both vehicle and science loads halted
#   go    - Resume vehicle and science ops based on new plan
#   too   - TOO
#   man   - Maneuver Load running only
#
# From the Non-LoadEvent Tracking Tool you will get:
#   PITCH Maneuver
#   LTCTI
#   OTHER CAP
#   ANOMALOUS
#
# For all of these events you will have: time of the event (2015:201:22:10:55)
#                                        type (e.g. "too", "s107", "go" etc)
#     inputs: 
#                event_time - Precise time of the event
#                event_type - s107, too, etc.
#               status_line - history-files.pl will supply a status array
#                             which will be written into the event header
#                      desc - User supplied description of the event obtained
#                             from the Non-Load Event Tracker tool.
#
#    outputs: The user-specified event file has a new event appended to it.
#
################################################################################

# Get the list of command line arguments
arg_list = sys.argv

# Using ARGPARSE
cl_parser = argparse.ArgumentParser(description='Non-Load Event Tracker argument handler')

# Add the CHOICE a.k.a. EVENT_TYPE argument as a *****POSITIONAL*****
cl_parser.add_argument('event_type', help='Specify the type of event: LTCTI, OTHERCTI, S107, etc')

# Add event TIME argument as NON-POSITIONAL
cl_parser.add_argument('--event_time', help='DOY format time of this event. Example: 2017:162:21:57:22.22', type=str)

# Add the STATUS LINE argument as NON-POSITIONAL.  default is a string
cl_parser.add_argument('--status_line', help='This is a help string  for STATUS LINE to tell you how to use this. Example: HRC-I,HETG-OUT,LETG-OUT,18913,OORMPEN,CSELFMT1,ENAB')

# Add the DESCRIPTION LINE argument as NON-POSITIONAL.  default is a string
cl_parser.add_argument('--desc', help='This is a string that is obtained when running the Non-Load Event Tracker tool.  The user of that tool is allowed to input a descriptive string which describes the event.')

# Add the TEST argument as NON-POSITIONAL.  
cl_parser.add_argument("-t", '--test', help='If specified it tells RecordNonLoadEvent.py to use the test output file and not the real output file.', action="store_true")

# Add the SOURCE argument as NON-POSITIONAL.  
cl_parser.add_argument("-s", '--source', help='If specified it tells RecordNonLoadEvent.py who called it')

# Add the path to the NON-Load Event Tracking File - default to TEST  
cl_parser.add_argument("--NLET_file", help='Full path to the Non Load Event Tracking file where this event will be recorded.The Default is: /data/acis/LoadReviews/TEST_NonLoadTrackedEvents.txt', default = '/data/acis/LoadReviews/TEST_NonLoadTrackedEvents.txt')

# ----------------------- QUATERNIONS ---------------------------------------------
# Add the QUATERNIONS argument as NON-POSITIONAL.  
cl_parser.add_argument("--q1", help='Final q1 quaternion after a  maneuver')

# Add the QUATERNIONS argument as NON-POSITIONAL.  
cl_parser.add_argument("--q2", help='Final q2 quaternion after a  maneuver')

# Add the QUATERNIONS argument as NON-POSITIONAL.  
cl_parser.add_argument("--q3", help='Final q3 quaternion after a  maneuver')

# Add the QUATERNIONS argument as NON-POSITIONAL.  
cl_parser.add_argument("--q4", help='Final q4 quaternion after a  maneuver')

#
# Items for LTCTI and other CLD files
# NOTE: Use the event_time argument for the CAP time execution
#
# Add the CTI CLD file argument as NON-POSITIONAL.  
cl_parser.add_argument('--cld_file', help='Path to the CLD file used in the CTI run')

# Add the CAP Number for the LTCTI run as NON-POSITIONAL.  
cl_parser.add_argument('--cap_num', help='Cap Number used in the CTI run')



# Parse out the args
args = cl_parser.parse_args()

# Upcase the event type so that use can use any lower/upper mix
args.event_type = args.event_type.upper()

# If -t or --test was specified, set the output file to the Test example
if args.test:
    # For Test Purposes:
    eventfilepath = "/data/acis/LoadReviews/TEST_NonLoadTrackedEvents.txt"
else: # Else set the path to the for-score tracking
    # For really keeping score
    eventfilepath = "/data/acis/LoadReviews/NonLoadTrackedEvents.txt"


# List of similar events
basic_event_list = ['S107', 'STOP', 'TOO', 'OTHERCLD']


# Open the official event file for appending information

# Substitute any Python None's with the appropriate spaces or 
# an appropriate string for thiose items that always appear.
# Therefore they need to have substitute values if none are 
# supplied (e.g. time  in the case of a GO)
if args.event_time == None:
    args.event_time = "".ljust(17)

if args.status_line == None:
    args.status_line = "".ljust(50)

if args.desc == None:
    args.desc = "None given."

# Open the output file to record the event
eventfile = open(eventfilepath, "a")
 
#---------------------------------------------------------------------------
#
#  Now handle each of the history file command types:
#   s107
#   stop
#   go
#   too
#   man
#
#---------------------------------------------------------------------------
if args.event_type in basic_event_list:
    # Append the header to the file
    eventfile.write("#*******************************************************************************")       
    eventfile.write("\n# Type: "+args.event_type)
    eventfile.write("\n# Time of Event: "+args.event_time)
    eventfile.write("\n# Status Array: "+args.status_line)
    eventfile.write("\n# Source: "+args.source)
    eventfile.write("\n# Description: "+args.desc)
    eventfile.write("\n#-------------------------------------------------------------------------------")
    eventfile.write("\n#       Time           Event                 Status Line")
    eventfile.write("\n#-------------------------------------------------------------------------------")
    
    # Now write the information
    eventfile.write("\n"+str(args.event_time)+"    "+args.event_type+"   "+args.status_line+"\n")
    
    # Write the closing comment symbol
    eventfile.write("#\n")

#
# Record the LTCTI event
#
if (args.event_type == "LTCTI") or (args.event_type == "OTHERCLD"):
    # Append the header to the file
    eventfile.write("#*******************************************************************************")       
    eventfile.write("\n# Type: "+args.event_type)
    eventfile.write("\n# Time of Event: "+args.event_time)
#    eventfile.write("\n# Status Array: "+args.status_line)
    eventfile.write("\n# Source: "+args.source)
    eventfile.write("\n# CAP Number: "+args.cap_num)
    eventfile.write("\n# CLD File Path: "+args.cld_file)
    eventfile.write("\n# Description: "+args.desc)
    eventfile.write("\n#-------------------------------------------------------------------------------")
    eventfile.write("\n#       Time            Event   CAP #            CLD File Path")
    eventfile.write("\n#-------------------------------------------------------------------------------")
    
    # Now write the information
    eventfile.write("\n"+str(args.event_time)+"    "+args.event_type+"   "+args.cap_num+"  "+args.cld_file+"\n")
    
    # Write the closing comment symbol
    eventfile.write("#\n")
  
#
# Record the GO event
#
if args.event_type == "GO":
    # Append the header to the file
    eventfile.write("#*******************************************************************************")       
    eventfile.write("\n# Type: "+args.event_type)
#    eventfile.write("\n# Time of Event: "+args.event_time)
#    eventfile.write("\n# Status Array: "+args.status_line)
    eventfile.write("\n# Source: "+args.source)
    eventfile.write("\n# Description: "+args.desc)
    eventfile.write("\n#-------------------------------------------------------------------------------")
    eventfile.write("\n#       Time       Event  ")
    eventfile.write("\n#-------------------------------------------------------------------------------")
    
    # Now write the information
    eventfile.write("\n"+str(args.event_time)+"    "+args.event_type+"\n")
 
#
# ======================  Non-Basic ==========================
#
# Now handle any maneuvers that are dissimilar to the basic format of type and status line   
#
# Record the MANEUVER event
#

# If this IS a maneuver event...
if args.event_type == "MAN":
    # Calculate the pitch and roll values from the specified Quaternions
    # First create an aray of the 4 quaternions
    man_quat_array = np.array([float(args.q1), float(args.q2), float(args.q3), float(args.q4)])
    # Create the Quat instance
    man_quat = Quat(man_quat_array)
    # Now calculate the pitch and roll
    pitch = Ska.Sun.pitch(man_quat.ra, man_quat.dec, str(args.event_time))
    nom_roll = Ska.Sun.nominal_roll(man_quat.ra, man_quat.dec, str(args.event_time))

    # Append the header to the file
    eventfile.write("#*******************************************************************************")       
    eventfile.write("\n# Type: "+args.event_type)
    eventfile.write("\n# Time of Event: "+args.event_time)
    eventfile.write("\n# Source: "+args.source)
    eventfile.write("\n# Description: "+args.desc)
    eventfile.write("\n#-------------------------------------------------------------------------------")
    eventfile.write("\n#       Time        Event   Pitch  Nom-Roll      Q1       Q2       Q3      Q4")
    eventfile.write("\n#-------------------------------------------------------------------------------")
    
    # Now write the information; build the output string
    event_file_string = "\n"+str(args.event_time)+"   "+args.event_type+"   "+str(('%.2f') % pitch)+"  "+str(('%.2f') % nom_roll)
    event_file_string = event_file_string+ '  '+ args.q1+' '+ args.q2+' '+ args.q3+' '+ args.q4+"\n"

    # Now write the string out
    eventfile.write(event_file_string)
    

    # Write the closing comment symbol
    eventfile.write("#\n")
  
# Close the official event file
eventfile.close()

  
