################################################################################
#
# Class LTCTI - CLass of attributes and functions that acquires associated 
#             parameters, makes necessary calculations and creates an entry
#             for the Non-Load Event Tracker
#
################################################################################
import os

class LTCTI:

    # The Constructor
    def __init__(self):
        self.start_date = ""
        self.stop_date = ""
        self.start_time = 0.0
        self.stop_time = 0.0
        self.default_current_folder = "/data/acis/CAPs/CTI-CLDs/"
        self.CLD_filespec = None
        self.cap_number = None
        self.pitch = 90.0
        self.quarts = []

    #-----------------------------------------------------------------------
    #
    #-----------------------------------------------------------------------
    def CLDFileSelectcallback(self, widget, data = None):

        #file filters used with the filechoosers
        CLDfile_filter=gtk.FileFilter()
        CLDfile_filter.set_name("CLD files")
        CLDfile_filter.add_pattern("*.cld")
        all_filter=gtk.FileFilter()
        all_filter.set_name("All files")
        all_filter.add_pattern("*")

        # Create the dialog but do not show it yet
        self.CLDFILESelectordialog = gtk.FileChooserDialog(title="Select the CLD File",
                                                         action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                                         buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                                                  gtk.STOCK_OPEN, gtk.RESPONSE_OK))
 
        # Capture the name of the file selected
        # Set the default folder
        self.CLDFILESelectordialog.set_current_folder(self.default_current_folder)
        self.CLDFILESelectordialog.add_filter(CLDfile_filter)
        self.CLDFILESelectordialog.add_filter(all_filter)
 
        # Run the dialog and get the response
        response = self.CLDFILESelectordialog.run()

        if response == gtk.RESPONSE_OK:
            # User specified a file; capture it's name
            self.CLDfile_filespec = self.CLDFILESelectordialog.get_filename()
            # Now put the name of the selected file in the text entry field
            self.CLD_File_Name_entry.set_text(self.CLDfile_filespec)

        elif response == gtk.RESPONSE_CANCEL:
            print 'Cancel Clicked'

        # Done with the file chooser - get rid of it
        self.CLDFILESelectordialog.destroy()

#-----------------------------------------------------------------------
#
# LTCTIcallback - call back function when TEST, CANCEL or SCORE buttons
#               are pressed
#
#-----------------------------------------------------------------------
    def LTCTIcallback(self, widget, string):

        # Set up the output file depending upon whether this is for score
        # or just a test run
        if (string == "SCORE"):
            NLET_cmd = "/proj/sot/ska/bin/python /data/acis/LoadReviews/script/NONLOADEVENTTRACKER/RecordNonLoadEvent.py LTCTI --source NLET "
        else:
            NLET_cmd = "/proj/sot/ska/bin/python /data/acis/LoadReviews/script/NONLOADEVENTTRACKER/RecordNonLoadEvent.py -t  LTCTI --source NLET "

        # Now extract the arguments from the GUI and form the rest of the
        # RecordNonLoadEvent.py command.
        if (string == "SCORE") or (string == "TEST"):

            # --------------- DATE ------------------------------------------
            # Get the entry in the date field
            self.start_date = self.DATE_entry.get_text()

            if self.start_date == "":
                print "NO START TIME SPECIFIED!!!"
            else:
                # Concatenate the 
                NLET_cmd += "--event_time "+self.start_date+" "

            # --------------- CAP NUMBER -----------------------------------
            # Next Obtain the CAP number. NOTe that it is a string at 
            # point and concatenate it to the command
            self.cap_number = self.CAP_Number_entry.get_text()
            NLET_cmd += "--cap_num "+self.cap_number+" "

            # --------------- CLD FILE PATH -------------------------------
            # Now we want the full file path to the selected CLD file
            # and concatenate it to the command
            self.CLD_filespec =  self.CLD_File_Name_entry.get_text()
            NLET_cmd += "--cld_file "+self.CLD_filespec+" "

            # -------------- COMMENT -----------------------------------------
            # Now get whatever the user put in the comment field if anything
            user_comments_buffer = self.UserComment_entry.get_buffer()
            tstart = user_comments_buffer.get_start_iter()
            tend = user_comments_buffer.get_end_iter()
      
            user_comments = user_comments_buffer.get_text(tstart, tend)

            if user_comments == "":
                print "USER SUPPLIED NO COMMENT"
                user_comments = "No Comment"

            NLET_cmd += '--desc "'+user_comments+'" '   

        # Now that you have the command line built - execute it
        os.system(NLET_cmd)

        # Done with the window so destroy it
        self.BuildLTCTIWindow.destroy()
        return False


    def Pop_UP_LTCTI_Window(self):
        # 1111 -  Create the Basic window
        self.BuildLTCTIWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # set the title and size of the window.
        self.BuildLTCTIWindow.set_title("Long Term CTI Run")
        self.BuildLTCTIWindow.set_size_request(1000,700)
        self.BuildLTCTIWindow.set_border_width(10)

        # 2222 VBOX Create Vertical box to hold the toolbar and the plot
        # The first row will hold the toolbar
        # The second row item will contain the plotting area
        self.LTCTI_VBox = gtk.VBox(False, 20)

        # 3333 - Create a TABLE for textual entries and buttons
        self.TextEntry_Table = gtk.Table(15,15, True)

        start_row = 0
        start_col = 0

        # ------------------------------- DATE --------------------------------------
        # 4444 - LABEL - DATE
        row_len = 1
        col_len = 4
        self.DATE_label = gtk.Label("CAP Execution Date (DOY): ")
        self.TextEntry_Table.attach(self.DATE_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len+1

        row_len = 1
        col_len = 5
        # 4444a -  TEXT ENTRY - DATE
        self.DATE_entry = gtk.Entry(max=0)
        self.DATE_entry.set_text("")
        self.TextEntry_Table.attach(self.DATE_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)


        # -------------------------- CAP Number  --------------------------------------
        # 5555b - LABEL - CAP number
        start_row += row_len
        start_col = 1
        row_len = 1
        col_len = 2
        self.CAPNumber_label = gtk.Label("CAP Number: ")
        self.TextEntry_Table.attach(self.CAPNumber_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len
        row_len = 1
        col_len = 1
        # 5555b -  TEXT ENTRY - CAP Number Text Entry Field
        self.CAP_Number_entry = gtk.Entry(max=0)
        self.CAP_Number_entry.set_text("")
        self.TextEntry_Table.attach(self.CAP_Number_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        # -------------------- CLD File Path Specification  -------------------------
        # 5555c - LABEL - CLD File Name Label
        start_row += row_len
        start_col = 0
        row_len = 1
        col_len = 3
        self.CLDFileName_label = gtk.Label("CLD FULL File Path: ")
        self.TextEntry_Table.attach(self.CLDFileName_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)
        start_col += col_len
        row_len = 1
        col_len = 9
        # 5555c -  TEXT ENTRY - CLD File Name Text Entry Field
        self.CLD_File_Name_entry = gtk.Entry(max=0)
        self.CLD_File_Name_entry.set_text("")
        self.TextEntry_Table.attach(self.CLD_File_Name_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len
        row_len = 1
        col_len = 4
 
        # 5555c - BUTTON  CLD file select button
        self.FSbutton = gtk.Button("Choose File")
        self.FSbutton.connect("clicked", self.CLDFileSelectcallback, "CHOOSE")
        self.TextEntry_Table.attach(self.FSbutton,
                                    start_col +1,start_col + col_len,
                                    start_row, start_row + row_len)



        # -------------------- USER COMMENT -------------------------
        # 4444d - LABEL - User Comment Label
        start_row += row_len+1
        start_col = 0
        row_len = 1
        col_len = 3

        self.CLDFileName_label = gtk.Label("User Comment: ")
        self.TextEntry_Table.attach(self.CLDFileName_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col =+ col_len
        row_len = 4
        col_len = 9
        # 4444d -  TEXT ENTRY - User Comment Text Entry field 
        self.UserComment_entry = gtk.TextView()
#        self.UserComment_entry.set_text("None")
        self.TextEntry_Table.attach(self.UserComment_entry,
                                    start_col, start_col+col_len,
                                    start_row, start_row+1)


        # -------------------- SCORE BUTTON -------------------------
        start_row = 14
        start_col = 0
        # 4444c - BUTTON  For Real SCORE button
        self.SCOREbutton = gtk.Button("SCORE")
        self.SCOREbutton.connect("clicked", self.LTCTIcallback, "SCORE")
        self.TextEntry_Table.attach(self.SCOREbutton,
                                    start_col, start_col + 2,
                                    start_row, start_row + 1)

        # -------------------- CANCEL BUTTON -------------------------
        start_row = 14
        start_col = 11
        # 4444c - BUTTON  CANCEL button
        self.CANCELbutton = gtk.Button("CANCEL")
        self.CANCELbutton.connect("clicked", self.LTCTIcallback, "CANCEL")
        self.TextEntry_Table.attach(self.CANCELbutton,
                                    start_col, start_col + 2,
                                    start_row, start_row + 1)

        # -------------------- TEST BUTTON -------------------------
        start_row = 14
        start_col = 13
        # 4444c - BUTTON  TEST button
        self.TESTbutton = gtk.Button("TEST")
        self.TESTbutton.connect("clicked", self.LTCTIcallback, "TEST")
        self.TextEntry_Table.attach(self.TESTbutton,
                                    start_col, start_col + 1,
                                    start_row, start_row + 1)

        # 2222 - Add the table to the VBOX
        self.LTCTI_VBox.pack_start(self.TextEntry_Table)

        # Add the VBox to the window box
        self.BuildLTCTIWindow.add(self.LTCTI_VBox)


        # 1111 - Done creating the BuildEVENTTRACKER Window. Show it.
        self.BuildLTCTIWindow.show_all()
