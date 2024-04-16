"""calculator"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import sys
import sqlite3
import pandas
from PIL import Image


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Metal profiles calculator")
        # place app in the center of the screen
        width = 680
        height = 300
        x = int(self.winfo_screenwidth() / 2 - width / 2)
        y = int(self.winfo_screenheight() / 2 - height / 2)
        self.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
        # restrict resize
        self.resizable(False, False)

        # icon path
        self.iconbitmap(self.resource_path("assets\\rectangular.ico"))

        # theme main color
        self.theme_color = ctk.ThemeManager.theme["CTkButton"]['fg_color']
        # original border color
        self.origEntBorderColor = ctk.ThemeManager.theme["CTkEntry"]['border_color']
        # text color
        self.textColor = ctk.ThemeManager.theme["CTkEntry"]['text_color']
        # hover button color
        self.hoverBtColor = ctk.ThemeManager.theme["CTkButton"]['hover_color']
        # density special border color
        self.densChangedC = "#f95c00"  # orange

        # spreadsheets lists
        self.rect_spr_list = ["rectEN10210", "rectEN10219", "rectEN10305"]
        self.circle_spr_list = ["circleEN10210", "circleEN10219"]
        self.beam_spr_list = ["IPE_EN10365", "IPN_EN10365"]
        self.channel_spr_list = ["PFC_EN10365", "CH_EN10365", "UPE_EN10365", "UPN_EN10365", "U_EN10365"]

        # database
        conn = sqlite3.connect(self.resource_path("database\\metalDB.db"))
        self.cursor = conn.cursor()
        # self.create_table(conn)

        # menu
        self.upper_menu = UpperMenu(self)
        self.upper_menu.grid(row=0, column=0, pady=(10, 10), padx=(30, 0), sticky="", columnspan=2)

        # side image with parameters
        self.image_side_list = [ImageSide(self, 0), ImageSide(self, 1), ImageSide(self, 2), ImageSide(self, 3)]
        self.image_side = self.image_side_list[0]
        self.image_side.grid(row=1, column=0, pady=(0, 0), padx=(30, 0), sticky="nw")

        # interface
        self.windows_list = [BuildInterface(self, 0), BuildInterface(self, 1),
                             BuildInterface(self, 2), BuildInterface(self, 3)]
        self.interface = self.windows_list[0]
        self.interface.grid(row=1, column=1, pady=(0, 0), padx=(0, 0), sticky="nw")

        # create list for entries validations indication
        self.list_of_indLists = [[False, False, False], [False, True, False], "", ""]
        self.indList = self.list_of_indLists[0]

        # list for errLabels indexes
        ErLabLi = [self.windows_list[0].wLabel.label, self.windows_list[0].hLabel.label, self.windows_list[0].tLabel.label,
                   self.windows_list[0].dLabel.label, self.windows_list[0].sumLabel.label]
        ErLabLi1 = [self.windows_list[1].wLabel.label, "", self.windows_list[1].tLabel.label, self.windows_list[1].dLabel.label,
                    self.windows_list[1].sumLabel.label]
        ErLabLi2 = ["", "", "", self.windows_list[2].dLabel.label, self.windows_list[2].sumLabel.label]
        ErLabLi3 = ["", "", "", self.windows_list[3].dLabel.label, self.windows_list[3].sumLabel.label]
        self.list_of_labels_lists = [ErLabLi, ErLabLi1, ErLabLi2, ErLabLi3]
        self.ErLabList = self.list_of_labels_lists[0]
        self.ErLabListNew = self.list_of_labels_lists[0]

        # list of entries
        entrLst = [self.windows_list[0].width_entry.entry, self.windows_list[0].height_entry.entry,
                   self.windows_list[0].thickness_entry.entry, self.windows_list[0].dens_entry.entry, self.windows_list[0].sumEntry.entry]
        entrLst1 = [self.windows_list[1].width_entry.entry, "", self.windows_list[1].thickness_entry.entry,
                    self.windows_list[1].dens_entry.entry, self.windows_list[1].sumEntry.entry]
        entrLst2 = ["", "", "", self.windows_list[2].dens_entry.entry, self.windows_list[2].sumEntry.entry]
        entrLst3 = ["", "", "", self.windows_list[3].dens_entry.entry, self.windows_list[3].sumEntry.entry]
        self.list_of_entries_lists = [entrLst, entrLst1, entrLst2, entrLst3]
        self.entriesList = self.list_of_entries_lists[0]
        self.entriesListNew = self.list_of_entries_lists[0]

    ########################
    def change_interface(self, frame_ind):
        """change frames"""
        # remove focus from entry
        self.interface.focus()
        self.image_side.grid_remove()
        self.interface.grid_remove()

        self.image_side = self.image_side_list[frame_ind]
        self.interface = self.windows_list[frame_ind]
        self.indList = self.list_of_indLists[frame_ind]
        self.ErLabListNew = self.list_of_labels_lists[frame_ind]
        self.entriesListNew = self.list_of_entries_lists[frame_ind]

        self.image_side.grid(row=1, column=0, pady=(0, 0), padx=(30, 0), sticky="nw")
        self.interface.grid(row=1, column=1, pady=(0, 0), padx=(0, 0), sticky="nw")

    ########################
    @staticmethod
    def resource_path(relative_path):
        """# for pyinstaller from stackoverflow"""
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            """PyInstaller creates a temp folder and stores path in _MEIPASS"""
            base_path = sys._MEIPASS
        except (Exception,):
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    ########################
    def sliding(self, value, frame_ind):
        """show slide value"""
        self.list_trick()
        self.interface.focus()
        self.interface.sliderLabel.label.configure(text=str(int(value)) + "m")
        self.goto_count(frame_ind)

    ########################
    def optionmenu_callback(self, frame_ind):
        """combobox, redirect to goto_count"""
        self.list_trick()
        if frame_ind in (2, 3):
            app.image_side.clear_imageside(frame_ind)
            app.interface.Sentry.delete(0, "end")
            app.interface.Sentry.configure(placeholder_text="search")
            app.interface.scrollable_button_frame.button_chosen = "blank"
            app.clear_result_entry()
            standard = app.interface.combobox.combobox.get()
            for widget in app.interface.scrollable_button_frame.winfo_children():
                widget.destroy()
            app.interface.scrollable_button_frame._parent_canvas.yview_moveto(0)
            i = app.find_standard_index(standard)

            ind = app.interface.combo_dict[standard]
            app.interface.scrollable_button_frame.add_items(app.interface.frame_list_of_sec_lists[i], frame_ind)
            app.image_side.label_im.configure(image=app.image_side.db_images[ind])
        else:
            self.goto_count(frame_ind)

    ########################
    @staticmethod
    def find_standard_index(standard):
        """find standard's index"""
        for i, each in enumerate(app.interface.combo_list):
            if standard == each:
                return i

    ########################
    def add_validation(self, event):
        """functions for focusin focusout events and clear error labels"""
        self.list_trick()
        event.widget.configure(validate="all")

    def delete_validation(self, event, placeholder, er_label_num):
        """clear focusout error label if not "too large thickness"""""
        if er_label_num != 2 or self.ErLabList[2].cget("text") != "too large thickness":
            self.clear_label(er_label_num)
        value_str = event.widget.get()
        if len(value_str) == 0:
            event.widget.configure(validate="none")
            event.widget.insert("0", placeholder)

    ########################
    def valid_dens(self, inp, action_code, er_label_num):
        """validation for density"""
        self.clear_label(er_label_num)
        if action_code == "-1":  # focusout action code
            pass
        else:
            if inp.isnumeric():
                # give indicator
                if inp[0] == "0":
                    self.fill_label(er_label_num, 77)
                    self.entriesList[int(er_label_num)].delete(0, "end")
                    self.entriesList[int(er_label_num)].insert(0, "")
                    self.entriesList[int(er_label_num)].configure(border_color=app.theme_color, validate="all")
                    return False
                else:
                    if int(inp) <= 10000:
                        self.entriesList[int(er_label_num)].configure(border_color=app.densChangedC)
                        return True
                    else:
                        self.fill_label(er_label_num, 88)
                        return False
            elif inp == "":
                self.entriesList[int(er_label_num)].configure(border_color=app.theme_color)
                return True
            else:
                self.fill_label(er_label_num, 13)
                return False

    ########################
    def valid_wht(self, inp, action_code, er_label_num):
        """validation for width, height, thickness"""
        if action_code == "-1":  # focusout action code
            pass
        elif inp not in \
                ("width, mm", "height, mm", "thickness, mm", "outs. diam., mm"): \
                # fucking validation take placeholder as input
            self.clear_label(er_label_num)
            if inp.isdigit():
                # error if zero
                if inp[0] == "0":
                    # fill errorLabel
                    self.fill_label(er_label_num, 77)
                    self.change_indicator(er_label_num, False)
                    self.entriesList[int(er_label_num)].delete(0, "end")
                    self.entriesList[int(er_label_num)].insert(0, "")
                    self.entriesList[int(er_label_num)].configure(border_color=app.origEntBorderColor, validate="all")
                    return False
                else:
                    # check max absolute value
                    if self.check_abs_max(er_label_num, inp):
                        # change indList value
                        self.change_indicator(er_label_num, True)
                        # give main color(green, blue)
                        self.entriesList[int(er_label_num)].configure(border_color=app.theme_color)
                        return True
                    else:
                        if er_label_num == "2":
                            self.fill_label(er_label_num, 45)
                        else:
                            self.fill_label(er_label_num, 44)
                        return False
            elif inp == "":
                self.change_indicator(er_label_num, False)
                self.entriesList[int(er_label_num)].configure(border_color=app.origEntBorderColor)
                self.ErLabList[4].configure(text="")
                return True
            else:
                inp = inp.replace(",", ".")
                count = 0
                for char in inp:
                    if char == ".":
                        count += 1
                if self.is_float(inp):
                    if inp[0] == "0" or inp[0] == ".":
                        self.fill_label(er_label_num, 77)
                        self.change_indicator(er_label_num, False)
                        self.entriesList[int(er_label_num)].delete(0, "end")
                        self.entriesList[int(er_label_num)].insert(0, "")
                        self.entriesList[int(er_label_num)].configure(border_color=app.origEntBorderColor,
                                                                      validate="all")
                        return False
                    if self.check_abs_max(er_label_num, inp):
                        if len(inp.split(".")[1]) > 2:
                            self.fill_label(er_label_num, 33)
                            return False
                        else:
                            self.change_indicator(er_label_num, True)
                            self.entriesList[int(er_label_num)].configure(border_color=app.theme_color)
                            return True
                    else:
                        if er_label_num == "2":
                            self.fill_label(er_label_num, 45)
                        else:
                            self.fill_label(er_label_num, 44)
                        return False
                elif count > 1:
                    # fillLabel(erLabelNum, 22)
                    return False
                else:
                    self.fill_label(er_label_num, 11)
                    return False

    ########################
    @staticmethod
    def is_float(value):
        """check if float"""
        try:
            float(value)
            return True
        except (Exception,):
            return False

    ########################
    def change_indicator(self, er_label_num, ind_validation):
        """change indication list"""
        self.indList[int(er_label_num)] = ind_validation

    ########################
    def fill_label(self, er_label_num, er_code):
        """fill error label"""
        error = ""
        match er_code:
            case 11:
                error = str("should be a number")
            case 13:
                error = str("should be an integer")
            # case 22:
            #     error = str("must be only one decimal point")
            case 33:
                error = str("hundredths are enough")
            case 44:
                error = str("1000mm max")
            case 45:
                error = str("200mm max")
            case 66:
                error = str("too large thickness")
            case 77:
                error = str("can't start with zero")
            case 88:
                error = str("10k max")
        self.ErLabList[int(er_label_num)].configure(text=error)

    ########################
    def clear_label(self, er_label_num):
        """clear errorLabel"""
        self.ErLabList[int(er_label_num)].configure(text="")

    ########################
    @staticmethod
    def check_abs_max(er_label_num, inp):
        """check absolute max"""
        if er_label_num == "2":
            return float(inp) <= 200
        else:
            return float(inp) <= 1000

    ########################
    def goto_count(self, frame_ind):
        """keyrelease event, main function"""
        match frame_ind:
            case 0 | 1:
                # check all indicators
                for i, each in enumerate(self.indList):
                    if not each:
                        self.clear_result_entry()
                        app.image_side.clear_imageside(frame_ind)
                        # if remove not thickness value, change border to green 
                        if i != 2:
                            if self.is_float(self.entriesList[2].get()):
                                self.entriesList[2].configure(border_color=app.theme_color)
                                if self.ErLabList[2].cget("text") == "too large thickness":
                                    self.clear_label("2")
                        return
                # get parameters
                width = float(self.entriesList[0].get().replace(",", "."))
                height = 0
                if frame_ind == 0:
                    height = float(self.entriesList[1].get().replace(",", "."))
                thickness = float(self.entriesList[2].get().replace(",", "."))

                # check thickness
                if frame_ind == 0:
                    smaller = min(width, height)
                else:
                    smaller = width

                indicator = self.give_color_th(thickness, smaller)
                if indicator:
                    standard = self.interface.combobox.combobox.get()
                    ro = 0.0
                    ri = 0.0
                    if standard == "EN10210":
                        if frame_ind == 0:
                            ro = 1.5 * thickness
                            ri = thickness
                        
                        # for database
                        spreadsheet = app.interface.spreadsheets_list[0]
                    elif standard == "EN10219":
                        if frame_ind == 0:
                            if thickness <= 6:
                                ro = 2 * thickness
                                ri = thickness
                            elif 6 < thickness <= 10:
                                ro = 2.5 * thickness
                                ri = 1.5 * thickness
                            elif thickness > 10:
                                ro = 3 * thickness
                                ri = 2 * thickness
                        spreadsheet = app.interface.spreadsheets_list[1]
                    else:
                        if thickness <= 2.5:
                            ro = 0.5 * thickness
                        else:
                            ro = 1.75 * thickness
                            ri = 0.75 * thickness
                        spreadsheet = app.interface.spreadsheets_list[2]
                    # counting
                    if frame_ind == 0:
                        area = round((2 * thickness * (width + height - 2 * thickness) - (4 - 3.141592) *
                                      (ro ** 2 - ri ** 2)) / 100, 5)
                        app.image_side.pollute_imageside(frame_ind, [height, width, thickness, ro, ri])
                    else:
                        area = round(3.141592 * (width ** 2 - (width - 2 * thickness) ** 2) / 400, 5)
                        app.image_side.pollute_imageside(frame_ind, [width, thickness])

                    # search in database
                    match frame_ind:
                        case 0:
                            if width == height:
                                self.cursor.execute(
                                    "SELECT * FROM " + spreadsheet + " WHERE W =" + str(width) + " ANd H =" + str(
                                        height) + " and T =" + str(thickness))
                            else:
                                self.cursor.execute(
                                    "SELECT * FROM " + spreadsheet + " WHERE ((W =" + str(width) + " ANd H =" + str(
                                        height) + ") OR (W =" + str(height) + " ANd H =" + str(
                                        width) + ")) and T =" + str(thickness))
                        case 1:
                            self.cursor.execute(
                                "SELECT * FROM " + spreadsheet + " WHERE W =" + str(width) + " and T =" + str(
                                    thickness))
                    data = self.cursor.fetchall()
                    self.put_sumtext(frame_ind, data, standard, area)

                    if len(data) == 0:
                        self.ErLabList[4].configure(text="this size is not in the standard")
                        self.entriesList[4].configure(state="readonly", border_color=app.densChangedC)
                    else:
                        self.entriesList[4].configure(state="readonly", border_color=app.theme_color)
                        self.ErLabList[4].configure(text="")

                else:
                    self.clear_result_entry()
                    app.image_side.clear_imageside(frame_ind)

            case 2 | 3:
                self.list_trick()
                profile_name = self.interface.scrollable_button_frame.button_chosen
                standard = self.interface.combobox.combobox.get()
                
                i = app.find_standard_index(standard)
                spreadsheet = app.interface.spreadsheets_list[i]

                if profile_name != "blank":
                    self.cursor.execute("SELECT * FROM " + spreadsheet + " WHERE N like '%" + str(profile_name) + "%' ")
                    data = self.cursor.fetchall()
                    app.image_side.pollute_imageside(frame_ind, [data[0][3], data[0][4], data[0][6], data[0][5]])
                    standard = standard.split(" ")[0] + " - " + str(data[0][1])
                    self.put_sumtext(frame_ind, data, standard)
                    self.entriesList[4].configure(state="readonly", border_color=app.theme_color)

    #############################
    def give_color_th(self, th, smaller):
        """give or not color for thickness entry"""
        if th > smaller / 4:
            self.fill_label("2", 66)
            self.entriesList[2].configure(border_color="red")
            return False
        else:
            self.entriesList[2].configure(border_color=app.theme_color)
            if self.ErLabList[2].cget("text") == "too large thickness":
                self.clear_label("2")
            return True

##############################
    def put_sumtext(self, frame_ind, data, standard, *args):
        """put sum text in result entry"""
        length = int(self.interface.slider.slider.get())
        if frame_ind == 0:
            i = 4
        elif frame_ind == 1:
            i = 3
        else:
            i = 2
        try:
            density = float(self.entriesList[3].get()) / 10000
        except (Exception,):
            density = 0.785
        if len(data) > 0:
            mass = float(data[0][i])
            if density != 0.785:
                mass = round(mass*density/0.785, 2)
        else:
            mass = round(density * args[0], 2)
        mass = round(mass * length, 2)
        # remove ",oo" if necessary
        if mass.is_integer():
            mass = int(mass)
        sumtext = standard + " - " + str(length) + "m - " + str(mass).replace(".", ",") + "kg"

        self.entriesList[4].configure(state="normal")
        self.entriesList[4].delete("0", "end")
        self.entriesList[4].insert(0, sumtext)

    ##############################
    def clear_result_entry(self):
        """clear result entry"""
        self.entriesList[4].configure(state="normal")
        self.entriesList[4].delete("0", "end")
        # readonly state kills placeholder if it defines in the same configure
        self.entriesList[4].configure(placeholder_text="result")
        self.entriesList[4].configure(state="readonly", border_color=self.origEntBorderColor)
        self.ErLabList[4].configure(text="")

    #############################
    def create_table(self, conn):
        """create new table for database"""
        excel_tables = ["R10210", "R10219", "R10305-5",
                        "C10210", "C10219",
                        "IPE", "IPN",
                        "PFC", "CH", "UPE", "UPN", "U"]
        for j, each in enumerate(self.rect_spr_list + self.circle_spr_list +
                                 self.beam_spr_list + self.channel_spr_list):
            if j < 3:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS " + each + " ([W] REAL, [H] REAL, [T] REAL, [M] REAL)")
            elif j < 5:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS " + each + " ([W] REAL, [T] REAL, [M] REAL)")
            else:
                self.cursor.execute(
                    "CREATE TABLE IF NOT EXISTS " + each + " ([N] REAL, [M] REAL, "
                    "[h] REAL, [b] REAL, [s] REAL, [t] REAL, [A] REAL)")
            
            conn.commit()
            # read and rewrite tables
            spreadsheet = pandas.read_excel("metalDB.xlsx", excel_tables[j])
            spreadsheet.to_sql(name=each, con=conn, if_exists="replace")
        
        # self.cursor.execute("SELECT * FROM CH_EN10365 WHERE N = 'CH76x38x7' ")
        # data = self.cursor.fetchall()
        # print(data)

        # conn.close()

    #############################
    def list_trick(self):
        """lists trick for avoiding adding artifacts"""
        self.ErLabList = self.ErLabListNew
        self.entriesList = self.entriesListNew


###################################################################
class UpperMenu(ctk.CTkFrame):
    """upper menu"""

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.holSecBt = MenuButton(self, 0, "rectang.png", master.hoverBtColor)
        self.circleBt = MenuButton(self, 1, "round_circle.png", "transparent")
        self.beamBt = MenuButton(self, 2, "i-beam.png", "transparent")
        self.channel_Bt = MenuButton(self, 3, "u_sect.png", "transparent")

        self.buttonList = (self.holSecBt.button, self.circleBt.button, self.beamBt.button, self.channel_Bt.button)

        # info button
        MenuButton(self, 4, "information.png", "transparent")  # InfoBt =

    def change_fg(self, column):
        """change foreground of side menu button"""
        for each in self.buttonList:
            if each.cget("fg_color") != "transparent":
                each.configure(fg_color="transparent")
                break
        self.buttonList[column].configure(fg_color=app.hoverBtColor)
        app.change_interface(column)

    #############
    def popup_info(self):
        """info"""
        CTkMessagebox(self.master, title="Info", justify="center", icon_size=(30, 30), button_height=28,
                      font=('Helvetica', 14),
                      message="Formulas and data sources:\nhollow sections:\n\
    EN10210-2:2006 p.14-15\n\
    EN10219-2:2006 p.20-22\n    EN10305-5:2016 p.13-15\nI sections:\n\
    EN10365:2017 p.8-10, p.27\nchannels:\n    EN10365:2017 p.28-31\n\
    \n\ntested by Flawless\ncreated by Kviten4")


##################
class MenuButton:
    """buttons for upper menu"""

    def __init__(self, master, column, image_name, hover_color):
        super().__init__()
        if image_name == "information.png":
            comm = master.popup_info
        else:
            comm = lambda: master.change_fg(column)
        image = ctk.CTkImage(Image.open(App.resource_path("assets\\" + image_name)), size=(28, 28))
        self.button = ctk.CTkButton(master, text="", image=image, width=28, fg_color=hover_color,
                                    border_width=0, command=comm)
        self.button.grid(row=0, column=column, pady=(0, 0), padx=(0, 5))


###################################################################
class BuildInterface(ctk.CTkFrame):
    """build window"""

    def __init__(self, master, frame_ind):
        super().__init__(master)
        self.configure(fg_color="transparent")
        ###############

        # some paddings
        lpadx = 20  # left padx
        lpadx2 = 20  # left padx 2-nd column
        hpady = 0  # upper pady
        lwpady = 5  # lower pady
        justify = "left"

        # elements' width
        elem_width = 140
        # for slider
        sl_lab_width = 30
        # fonts
        self.custom_font = ('Helvetica', 15)

        minus_row = 2
        if frame_ind == 0:
            self.combo_list = ["EN10210", "EN10219", "EN10305-5"]
            self.spreadsheets_list = master.rect_spr_list
            minus_row = 0
        elif frame_ind == 1:
            self.combo_list = ["EN10210", "EN10219"]
            self.spreadsheets_list = master.circle_spr_list
        elif frame_ind == 2:
            self.combo_dict = {"EN10365 - IPE": 0, "EN10365 - IPN": 1}
            self.combo_list = list(self.combo_dict.keys())
            self.spreadsheets_list = master.beam_spr_list
        else:
            self.combo_dict = {"EN10365 - PFC": 0, "EN10365 - CH": 1, "EN10365 - UPE": 0, "EN10365 - UPN": 1, "EN10365 - U": 1}
            self.combo_list = list(self.combo_dict.keys())
            self.spreadsheets_list = master.channel_spr_list
            
            #######################
        # register validation
        vcmd_wht = (master.register(master.valid_wht))
        vcmd_d = (master.register(master.valid_dens))

        match frame_ind:
            case 0 | 1:
                dens_tail = 0
                self.wLabel = CreateLabels(self, [0, 0], [lpadx, 0], [hpady, 0], elem_width, "w", 1)

                if frame_ind == 0:
                    placeholder = "width, mm"
                else:
                    placeholder = "outs. diam., mm"

                self.width_entry = CreateEntry(self, [1, 0], [lpadx, 0], [0, lwpady], elem_width, placeholder,
                                               self.custom_font, vcmd_wht, justify, 0, "w", 1, frame_ind)

                if frame_ind == 0:
                    self.hLabel = CreateLabels(self, [2, 0], [lpadx, 0], [0, 0], elem_width, "w", 1)
                    self.height_entry = CreateEntry(self, [3, 0], [lpadx, 0], [0, lwpady], elem_width, "height, mm",
                                                    self.custom_font, vcmd_wht, justify, 1, "w", 1, frame_ind)

                self.tLabel = CreateLabels(self, [4 - minus_row, 0], [lpadx, 0], [0, 0], elem_width, "w", 1)
                self.thickness_entry = CreateEntry(self, [5 - minus_row, 0], [lpadx, 0], [0, lwpady],
                                                   elem_width, "thickness, mm", self.custom_font, vcmd_wht, justify,
                                                   2, "w", 1, frame_ind)

            case 2 | 3:
                # get list of profiles
                self.frame_list_of_sec_lists = []
                dens_tail = 10
                for i, every in enumerate(self.spreadsheets_list):
                    self.frame_list_of_sec_lists.append(list())
                    if i < 2 and frame_ind == 3:
                        remove_last = 3
                    else:
                        remove_last = 0
                    data = list(master.cursor.execute("SELECT N FROM " + every).fetchall())
                    for each in data:
                        self.frame_list_of_sec_lists[i].append(list(each)[0][:len(list(each)[0]) - remove_last])

                self.scrollable_button_frame = ScrollableButtonFrame(self, width=elem_width-26, height=100, border_width=2,
                                                                     border_color=master.origEntBorderColor, )
                self.scrollable_button_frame.grid(row=0, column=0, padx=(lpadx, 0), pady=(hpady + 5, lwpady),
                                                  rowspan=4, columnspan=1, sticky="nesw")
                self.scrollable_button_frame._scrollbar.configure(height=0)  # bug, it's needed
                self.scrollable_button_frame._scrollbar.grid(row=1, column=1, sticky="nsew", padx=(0, 3))
                self.scrollable_button_frame.add_items(self.frame_list_of_sec_lists[0], frame_ind)

                self.Sentry = ctk.CTkEntry(self, width=elem_width, placeholder_text="search", font=self.custom_font,
                                           justify=justify)
                self.Sentry.bind("<KeyRelease>", lambda event: self.search(event, frame_ind))
                self.Sentry.grid(row=0, column=1, padx=(lpadx2, lpadx), pady=(hpady + 5, lwpady))

        # options menu for standards
        self.combobox = CreateCombobox(self, [1, 1], [lpadx2, lpadx], [0, lwpady], self.combo_list, elem_width,
                                       self.custom_font, justify, frame_ind)

        self.dLabel = CreateLabels(self, [2, 1], [lpadx2, lpadx], [0, 0], elem_width, "w", 1)
        self.dens_entry = CreateEntry(self, [3, 1], [lpadx2, lpadx], [0, lwpady + dens_tail], elem_width, "7850kg/cub.m",
                                      self.custom_font, vcmd_d, justify, 3, "w", 1, frame_ind)
        self.dens_entry.entry.configure(border_color=master.theme_color)

        # slider section + label
        self.slider = CreateSlider(self, [6 - minus_row, 0], [lpadx, 0], [lwpady, 0], lpadx2, elem_width, sl_lab_width,
                                   frame_ind)
        self.sliderLabel = CreateLabels(self, [6 - minus_row, 1], [lpadx2, lpadx], [lwpady, 0], sl_lab_width, "e", 1)
        self.sliderLabel.label.configure(height=28, text=str(1) + "m", anchor="e", font=self.custom_font,
                                         text_color=master.textColor)

        # result
        self.sumLabel = CreateLabels(self, [7 - minus_row, 0], [lpadx, lpadx], [0, 0], elem_width, "we", 2)
        self.sumEntry = CreateEntry(self, [8 - minus_row, 0], [lpadx, lpadx], [0, 0], elem_width, "result",
                                    self.custom_font, vcmd_wht, "center", 2, "we", 2, frame_ind)
        self.sumEntry.entry.unbind()
        self.sumEntry.entry.configure(state="readonly")

        if frame_ind == 2 or frame_ind == 3:
            self.combobox.combobox.grid(row=1, column=1, padx=(lpadx2, lpadx), pady=(15, lwpady))
            self.dens_entry.entry.configure(border_color=master.theme_color)

    ############
    def search(self, event, frame_ind):
        """search in scrollable frame"""
        event.widget.configure(state="disabled")
        
        standard = app.interface.combobox.combobox.get()
        i = app.find_standard_index(standard)

        value = event.widget.get()
        if value == "":
            data = self.frame_list_of_sec_lists[i]
        else:
            data = []
            for item in self.frame_list_of_sec_lists[i]:
                if value.lower() in item.lower():
                    data.append(item)

        for widget in self.scrollable_button_frame.winfo_children():
            widget.destroy()

        self.scrollable_button_frame._parent_canvas.yview_moveto(0)  # move to start of the list
        if len(data) > 0:
            self.scrollable_button_frame.add_items(data, frame_ind)
            # change in ctk_scrollabel_frame.py!
            # self.scrollable_button_frame._scrollbar.configure(minimum_pixel_length=20)
        else:
            # self.scrollable_button_frame._scrollbar.configure(minimum_pixel_length=110)
            pass

        event.widget.configure(state="normal")


##################################
class CreateLabels:
    """create error labels"""

    def __init__(self, master, row_col, padx_l, pady_l, elem_width, sticky, columnspan):
        super().__init__()

        # error labels height
        label_h = 12
        custom_font_er_lb = ('Helvetica', 12)

        self.label = ctk.CTkLabel(master, text="", width=elem_width, height=label_h,
                                  font=custom_font_er_lb, text_color="red")
        self.label.grid(row=row_col[0], column=row_col[1], padx=(padx_l[0], padx_l[1]), pady=(pady_l[0], pady_l[1]),
                        sticky=sticky, columnspan=columnspan)


##################################
class CreateEntry:
    """entries creating"""

    def __init__(self, master, row_col, padx_l, pady_l, elem_width, placeholder, custom_font, vcmd_wht,
                 justify, er_label_num, sticky, columnspan, frame_ind):
        super().__init__()
        self.entry = ctk.CTkEntry(master, width=elem_width, placeholder_text=placeholder, font=custom_font,
                                  validate="none", validatecommand=(vcmd_wht, '%P', "%d", er_label_num),
                                  justify=justify)
        # have to add events because placeholder don't work properly with fucking validatecommand
        self.entry.bind("<FocusIn>", master.master.add_validation)
        # also add erLabelNum for clearing error labels when focusout
        self.entry.bind("<FocusOut>", lambda event, placeholder_text=placeholder,
                        lnum=er_label_num: master.master.delete_validation(event, placeholder_text, lnum))
        # event for get entries values after validation
        self.entry.bind("<KeyRelease>", lambda event=None, ind=frame_ind: master.master.goto_count(ind))
        self.entry.grid(row=row_col[0], column=row_col[1], padx=(padx_l[0], padx_l[1]), pady=(pady_l[0], pady_l[1]),
                        sticky=sticky, columnspan=columnspan)


##################################
class CreateCombobox:
    """combobox creating"""

    def __init__(self, master, row_col, padx_l, pady_l, val_list, elem_width, custom_font, justify, frame_ind):
        super().__init__()
        self.combobox = ctk.CTkComboBox(master,
                                        values=val_list,
                                        width=elem_width,
                                        font=custom_font,
                                        dropdown_font=custom_font,
                                        state="readonly",
                                        # command=lambda value=None, ind=frame_ind:
                                        # app.optionmenu_callback(ind),
                                        border_color=master.master.theme_color,
                                        button_color=master.master.theme_color,
                                        justify=justify)
        self.combobox.set(val_list[0])
        self.combobox.grid(row=row_col[0], column=row_col[1], padx=(padx_l[0], padx_l[1]), pady=(pady_l[0], pady_l[1]))

        self.dropdown_menu = None
        # rebind to new function
        self.combobox._canvas.tag_unbind("dropdown_arrow", "<Button-1>")
        self.combobox._canvas.tag_unbind("right_parts", "<Button-1>")
        self.combobox._canvas.tag_bind("dropdown_arrow", "<Button-1>",
                                       lambda event: self.arrow_clicked(event, elem_width, val_list, frame_ind))
        self.combobox._canvas.tag_bind("right_parts", "<Button-1>",
                                       lambda event: self.arrow_clicked(event, elem_width, val_list, frame_ind))

    ############
    def arrow_clicked(self, event, elem_width, val_list, frame_ind):
        """after clicking combobox button(arrow) create toplevel"""

        if self.dropdown_menu is None:
            # create toplevel dropdown menu
            self.dropdown_menu = ctk.CTkToplevel(self.combobox)
            self.dropdown_menu.width = elem_width
            self.dropdown_menu.height = (28 + 2 + 2) * len(val_list)
            self.dropdown_menu.overrideredirect(True)  # remove upper panel
        else:
            # unhide menu
            self.dropdown_menu.deiconify()

        x = event.widget.winfo_rootx()
        y = event.widget.winfo_rooty() + 28 + 1
        self.dropdown_menu.geometry(str(self.dropdown_menu.width) + 'x' + str(self.dropdown_menu.height) + '+'
                                    + str(x) + '+' + str(y))
        self.dropdown_menu.focus()
        self.frame_dropdown = ctk.CTkFrame(self.dropdown_menu, border_color=app.origEntBorderColor, border_width=2,
                                           width=self.dropdown_menu.width, height=self.dropdown_menu.height)
        self.frame_dropdown.grid(row=0, column=0)

        self.dropdown_menu.bind("<FocusOut>", self.hide_dropdown)

        for i, each in enumerate(val_list):
            self.add_btn(i, each, len(val_list), frame_ind)

    ############
    def add_btn(self, i, each, length, frame_ind):
        """add buttons to the dropdown menu"""
        button = ctk.CTkButton(self.frame_dropdown, text=each, fg_color="transparent", width=self.dropdown_menu.width - 5,
                               font=app.interface.custom_font,
                               command=lambda: self.close_toplevel(each, frame_ind), corner_radius=3, anchor="w",
                               text_color=app.textColor)
        pady_lower = 0
        if i == length - 1:
            pady_lower = 2

        button.grid(row=i, column=0, padx=(2, 2), pady=(2, pady_lower))

    ############
    def close_toplevel(self, item, frame_ind):
        """change combobox value and close dropdown"""
        self.combobox._entry.configure(state="normal")
        self.combobox._entry.delete(0, "end")
        self.combobox._entry.insert(0, item)
        self.combobox._entry.configure(state="readonly")
        self.hide_dropdown()
        app.optionmenu_callback(frame_ind)

    ############
    def hide_dropdown(self, event=None):
        """close dropdown menu"""
        self.dropdown_menu.withdraw()
        app.interface.focus()


##################################
class CreateSlider:
    """slider and label creating"""

    def __init__(self, master, row_col, padx_l, pady_l, lpadx2, elem_width, sl_lab_width, frame_ind):
        super().__init__()
        self.slider = ctk.CTkSlider(master, from_=1, to=12, number_of_steps=11, border_width=4,
                                    width=2 * elem_width + lpadx2 - sl_lab_width,
                                    command=lambda value, ind=frame_ind: master.master.sliding(value, ind))
        self.slider.set(1)
        self.slider.grid(row=row_col[0], column=row_col[1], padx=(padx_l[0], padx_l[1]), pady=(pady_l[0], pady_l[1]),
                         sticky="w", columnspan=2)


###########################################################################################
class ScrollableButtonFrame(ctk.CTkScrollableFrame):
    """scrollable frame with buttons creating"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")

        self.button_chosen = "blank"
        self.initial_bt_list = []

    def add_items(self, list_of_values, frame_ind):
        """add list of values"""
        self.initial_bt_list.clear()
        for j, each in enumerate(list_of_values):
            self.add_item(each, j, frame_ind)

    def add_item(self, item, j, frame_ind):
        """add button"""
        button = ctk.CTkButton(self, text=item, height=24, width=108, fg_color="transparent",
                               font=self.master.master.master.custom_font,
                               anchor="w", command=lambda: self.change_bt_chosen(item, j, frame_ind),
                               text_color=self.master.master.master.master.textColor)
        button.grid(row=j, column=0, pady=(0, 2), padx=0)
        self.initial_bt_list.append(button)

    def change_bt_chosen(self, value, bt_ind, frame_ind):
        """change chosen button"""
        for widget in self.initial_bt_list:
            if widget.cget("fg_color") == app.theme_color:
                widget.configure(fg_color="transparent")
                break
        self.initial_bt_list[bt_ind].configure(fg_color=app.theme_color)
        self.button_chosen = value
        app.goto_count(frame_ind)


###########################################################################################
class ImageSide(ctk.CTkFrame):
    """side for size illustration"""
    def __init__(self, master, frame_ind):
        super().__init__(master)
        self.configure(fg_color="transparent")
        self.labels_parameters = [
            [["H", 248, 114], ["W", 115, 188], ["t", 1, 117], ["R", 3, 11], ["r", 94, 56]],
            [["D", 223, 23], ["t", 223, 172]],
            [["H", 9, 104], ["W", 115, 187], ["t", 238, 34], ["s", 178, 120]],
            [["H", 0, 104], ["W", 115, 187], ["t", 238, 34], ["s", 135, 86]]
        ]
        self.image_label_list = [[], [], [], []]
        self.db_images = []
        db_images_beams = ["bigBeam.png", "bigBeam_taper.png"]
        db_images_channels = ["big_Usect.png", "big_Usect_taper.png"]

        images_list = []
        if frame_ind == 2:
            images_list = db_images_beams
        elif frame_ind == 3:
            images_list = db_images_channels
        for each in images_list:
            self.db_images.append(ctk.CTkImage(Image.open(App.resource_path("assets\\" + each)), size=(293, 225)))
        self.image_png_names = ["bigRec.png", "bigCircle.png", "bigBeam.png", "big_Usect.png", ]
        self.create_imageside(frame_ind)

    ##############################
    def create_imageside(self, frame_ind):
        """create image and labels"""

        image = ctk.CTkImage(Image.open(App.resource_path("assets\\" + self.image_png_names[frame_ind])), size=(293, 225))
        self.label_im = ctk.CTkLabel(self, text="", image=image)
        self.label_im.pack()
        for item in self.labels_parameters[frame_ind]:
            label = ctk.CTkLabel(self.label_im, fg_color="transparent", font=('Helvetica', 14), height=13, width=34,
                                 anchor="center", text=item[0])
            label.place(x=item[1], y=item[2])
            self.image_label_list[frame_ind].append(label)

    ##############################
    @staticmethod
    def clear_imageside(frame_ind):
        """clear parameters labels"""
        for k, _label in enumerate(app.image_side_list[frame_ind].image_label_list[frame_ind]):
            _label.configure(text=app.image_side_list[frame_ind].labels_parameters[frame_ind][k][0])

    ##############################
    @staticmethod
    def pollute_imageside(frame_ind, list_of_parameters):
        """pollute labels on image side"""
        for j, par in enumerate(list_of_parameters):
            match frame_ind:
                case 0 | 1:
                    if par.is_integer():
                        par = int(par)
                    if j < 3:
                        lb_txt = str(par).replace(".", ",")
                    elif par == 0:
                        lb_txt = "N/S"
                    elif round(float(par), 1).is_integer():
                        lb_txt = str(int(round(par, 1))).replace(".", ",")
                    else:
                        lb_txt = str(round(par, 1)).replace(".", ",")
                case 2 | 3:
                    if float(par).is_integer():
                        par = int(par)
                    lb_txt = str(par).replace(".", ",")
            app.image_side_list[frame_ind].image_label_list[frame_ind][j].configure(text=lb_txt)


#########################################################################################
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
    app = App()
    app.mainloop()
