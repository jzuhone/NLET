################################################################################
#
# Class MAN - CLass of attributes and functions that acquires associated 
#             parameters, makes necessary calculations and creates an entry
#             for the Non-Load Event Tracker
#
#
# Update: October 11, 2017
#         Gregg Germain
#         - Removed Pitch and Roll GUI entries
#         - Replaced them with a calculation for pitch and roll (TB_DONE)
#
################################################################################
class PITCHMAN:

    # The Constructor
    def __init__(self):
        self.start_date = "1900:000:00:01:00.00"
        self.stop_date = "1900:001:00:01:00.00"
        self.start_time = '0.0'
        self.stop_time = '0.0'
        self.pitch = '1000'
        self.roll = '2000'
        self.q1 = '-1000'
        self.q2 = '-2000'
        self.q3 = '-3000'
        self.q4 = '-4000'
#-----------------------------------------------------------------------
#
# MANcallback - call back function when TEST, CANCEL or SCORE buttons
#               are pressed
#
#-----------------------------------------------------------------------
    def MANcallback(self, widget, string):

        # Set up the output file depending upon whether this is for score
        # or just a test run
        #
        # NOTE: It is RecordNonLoadEvent.py that sets the file spec for the NLET file
        if (string == "SCORE"):
            NLET_cmd = "/proj/sot/ska/bin/python /data/acis/LoadReviews/script/NONLOADEVENTTRACKER/RecordNonLoadEvent.py   MAN --source NLET "
        else:
            NLET_cmd = "/proj/sot/ska/bin/python /data/acis/LoadReviews/script/NONLOADEVENTTRACKER/RecordNonLoadEvent.py -t MAN --source NLET "

        # Now extract the arguments from the GUI and form the rest of the
        # RecordNonLoadEvent.py command.
        if (string == "SCORE") or (string == "TEST"):

            # --------------- DATE ------------------------------------------
            # Get the entry in the date field
            self.start_date = self.DATE_entry.get_text()

            if self.start_date == "":
                print "NO START DATE SPECIFIED!!!"
            else:
                # Concatenate the 
                NLET_cmd += "--event_time "+self.start_date+" "


            # ---------------- QUATERNIONs Q1 through Q4 --------------------
            # Next Obtain the CAP number. NOTE that it is a string at 
            # point and concatenate it to the command
            self.q1 = self.Q1_entry.get_text()
            NLET_cmd += '--q1 '+str(self.q1)+" "

            # ---------------- QUATERNIONs Q2 --------------------
            # Next Obtain the CAP number. NOTE that it is a string at 
            # point and concatenate it to the command
            self.q2 = self.Q2_entry.get_text()
            NLET_cmd += '--q2 '+str(self.q2)+" "

            # ---------------- QUATERNIONs Q3 --------------------
            # Next Obtain the CAP number. NOTE that it is a string at 
            # point and concatenate it to the command
            self.q3 = self.Q3_entry.get_text()
            NLET_cmd += '--q3 '+str(self.q3)+" "

            # ---------------- QUATERNIONs Q4 --------------------
            # Next Obtain the CAP number. NOTE that it is a string at 
            # point and concatenate it to the command
            self.q4 = self.Q4_entry.get_text()
            NLET_cmd += '--q4 '+str(self.q4)+" "

             # -------------- COMMENT -----------------------------------------
            # Now get wheatever the user put in the comment field if anything
            user_comments_buffer = self.UserComment_entry.get_buffer()
    
            tstart = user_comments_buffer.get_start_iter()
            tend = user_comments_buffer.get_end_iter()
      
            user_comments = user_comments_buffer.get_text(tstart, tend)

            if user_comments == "":
                print "USER SUPPLIED NO COMMENT"
                user_comments = "No Comment"

            NLET_cmd += '--desc "'+user_comments+'" '
         
            # Execute the command
            os.system(NLET_cmd)

        # Done with the window so destroy it
        self.BuildMANWindow.destroy()
        return False


    def Pop_UP_MAN_Window(self):
        # 1111 -  Create the Basic window
        self.BuildMANWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # set the title and size of the window.
        self.BuildMANWindow.set_title("MAN")
        self.BuildMANWindow.set_size_request(700,700)
        self.BuildMANWindow.set_border_width(10)

        # 2222 VBOX Create Vertical box to hold the toolbar and the plot
        # The first row will hold the toolbar
        # The second row item will contain the plotting area
        self.MAN_VBox = gtk.VBox(False, 20)

        # 3333 - Create a TABLE for textual entries and buttons
        self.TextEntry_Table = gtk.Table(15,15, True)

        start_row = 0
        start_col = 0

        # ------------------------------- DATE ------------------------
        # 4444 - LABEL - DATE
        row_len = 1
        col_len = 3
        self.DATE_label = gtk.Label("MAN Date (DOY): ")
        self.TextEntry_Table.attach(self.DATE_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len

#        row_len = 1
        col_len = 5
        # 4444a -  TEXT ENTRY - DATE
        self.DATE_entry = gtk.Entry(max=0)
        self.DATE_entry.set_text("")
        self.TextEntry_Table.attach(self.DATE_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)



        # ------------------------------- QUATERNIONS ------------------------
        #
        # ------------------------------------------ Q1
        start_row += row_len
        # Shift this over the text box
        start_col = 0
        # 4444 - LABEL - QUATERNION
#        row_len = 1
#        col_len = 8
#        self.TextEntry_Table.attach(self.QUATERNION_label, 
#                                    start_col, start_col + col_len,
#                                    start_row, start_row + row_len)

        # 4444 - LABEL - Q1 QUATERNION
        row_len = 1
        col_len = 3
        self.QUATERNION_label = gtk.Label("Q1: ")
        self.TextEntry_Table.attach(self.QUATERNION_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len

        col_len = 5
        # 4444a -  TEXT ENTRY - QUATERNION
        self.Q1_entry = gtk.Entry(max=0)
        self.Q1_entry.set_text("")
        self.TextEntry_Table.attach(self.Q1_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        # ---------------------------------------  Q2
        start_row += row_len
        # Shift this over the text box
        start_col = 0
        # 4444 - LABEL - QUATERNION
#        row_len = 1
#        col_len = 8
#        self.TextEntry_Table.attach(self.QUATERNION_label, 
#                                    start_col, start_col + col_len,
#                                    start_row, start_row + row_len)

        # 4444 - LABEL - Q2 Q2
        row_len = 1
        col_len = 3
        self.Q2_label = gtk.Label("Q2: ")
        self.TextEntry_Table.attach(self.Q2_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len

        col_len = 5
        # 4444a -  TEXT ENTRY - Q2
        self.Q2_entry = gtk.Entry(max=0)
        self.Q2_entry.set_text("")
        self.TextEntry_Table.attach(self.Q2_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)


        # ---------------------------------------  Q3
        start_row += row_len
        # Shift this over the text box
        start_col = 0
        # 4444 - LABEL - QUATERNION
#        row_len = 1
#        col_len = 8
#        self.TextEntry_Table.attach(self.QUATERNION_label, 
#                                    start_col, start_col + col_len,
#                                    start_row, start_row + row_len)

        # 4444 - LABEL - Q3 Q3
        row_len = 1
        col_len = 3
        self.Q3_label = gtk.Label("Q3: ")
        self.TextEntry_Table.attach(self.Q3_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len

        col_len = 5
        # 4444a -  TEXT ENTRY - Q3
        self.Q3_entry = gtk.Entry(max=0)
        self.Q3_entry.set_text("")
        self.TextEntry_Table.attach(self.Q3_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)



        # ---------------------------------------  Q4
        start_row += row_len
        # Shift this over the text box
        start_col = 0

        # 4444 - LABEL - Q4 Q4
        row_len = 1
        col_len = 3
        self.Q4_label = gtk.Label("Q4: ")
        self.TextEntry_Table.attach(self.Q4_label, 
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)

        start_col += col_len

        col_len = 5
        # 4444a -  TEXT ENTRY - Q4
        self.Q4_entry = gtk.Entry(max=0)
        self.Q4_entry.set_text("")
        self.TextEntry_Table.attach(self.Q4_entry,
                                    start_col, start_col + col_len,
                                    start_row, start_row + row_len)



        # -------------------- USER COMMENT -------------------------
        # 4444d - LABEL - User Comment Label
        start_row += row_len
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
#        self.UserComment_entry.set_text("")
        self.TextEntry_Table.attach(self.UserComment_entry,
                                    start_col, start_col+col_len,
                                    start_row, start_row+1)


        # -------------------- SCORE BUTTON -------------------------
        start_row = 14
        start_col = 0
        # 4444c - BUTTON  For Real SCORE button
        self.SCOREbutton = gtk.Button("SCORE")
        self.SCOREbutton.connect("clicked", self.MANcallback, "SCORE")
        self.TextEntry_Table.attach(self.SCOREbutton,
                                    start_col, start_col + 2,
                                    start_row, start_row + 1)

        # -------------------- CANCEL BUTTON -------------------------
        start_row = 14
        start_col = 11
        # 4444c - BUTTON  CANCEL button
        self.CANCELbutton = gtk.Button("CANCEL")
        self.CANCELbutton.connect("clicked", self.MANcallback, "CANCEL")
        self.TextEntry_Table.attach(self.CANCELbutton,
                                    start_col, start_col + 2,
                                    start_row, start_row + 1)

        # -------------------- TEST BUTTON -------------------------
        start_row = 14
        start_col = 13
        # 4444c - BUTTON  TEST button
        self.TESTbutton = gtk.Button("TEST")
        self.TESTbutton.connect("clicked", self.MANcallback, "TEST")
        self.TextEntry_Table.attach(self.TESTbutton,
                                    start_col, start_col + 1,
                                    start_row, start_row + 1)

        # 2222 - Add the table to the VBOX
        self.MAN_VBox.pack_start(self.TextEntry_Table)

        # Add the VBox to the window box
        self.BuildMANWindow.add(self.MAN_VBox)


        # 1111 - Done creating the BuildEVENTTRACKER Window. Show it.
        self.BuildMANWindow.show_all()
