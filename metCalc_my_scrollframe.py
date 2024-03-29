"""calculator"""
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import os
import sys
import sqlite3
import pandas
from PIL import Image
from CTkListbox import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Metal sections calculator")

        # place app in the center of the screen
        width = 355
        height = 300
        x = int(self.winfo_screenwidth() / 2 - width / 2)
        y = int(self.winfo_screenheight() / 2 - height / 2)
        self.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))
        # restrict resize
        self.resizable(False, False)

        # icon path
        self.iconbitmap(self.resource_path("assets\\icons8.ico"))

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

        # database
        conn = sqlite3.connect(self.resource_path("database\\metalDB.db"))
        self.cursor = conn.cursor()
        # self.createdataTable(conn)

        # menu
        self.upper_menu = UpperMenu(self)
        self.upper_menu.grid(row=0, column=0, pady=(10, 0), padx=(30, 0), sticky="w")

        # interface
        self.window = BuildInterface(self, 0)
        self.window1 = BuildInterface(self, 1)
        self.window2 = BuildInterface(self, 2)

        self.interface = self.window
        self.interface.grid(row=1, column=0, pady=(0, 0), padx=(0, 0))

        # create list for entries validations indication
        self.indL = [False, False, False]
        self.indL1 = [False, True, False]
        self.indList = self.indL

        # list for errLabels indexes
        self.ErLabLi = [self.window.wLabel.label, self.window.hLabel.label, self.window.tLabel.label,
                        self.window.dLabel.label, self.window.sumLabel.label]
        self.ErLabLi1 = [self.window1.wLabel.label, "", self.window1.tLabel.label, self.window1.dLabel.label,
                         self.window1.sumLabel.label]
        self.ErLabLi2 = ["", "", "", self.window2.dLabel.label, self.window2.sumLabel.label]
        self.ErLabList = self.ErLabLi
        self.ErLabListNew = self.ErLabLi

        # list of entries
        self.entrLst = [self.window.width_entry.entry, self.window.height_entry.entry,
                        self.window.thickness_entry.entry, self.window.dens_entry.entry, self.window.sumEntry.entry]
        self.entrLst1 = [self.window1.width_entry.entry, "", self.window1.thickness_entry.entry,
                         self.window1.dens_entry.entry, self.window1.sumEntry.entry]
        self.entrLst2 = ["", "", "", self.window2.dens_entry.entry, self.window2.sumEntry.entry]
        self.entriesList = self.entrLst
        self.entriesListNew = self.entrLst

    ########################
    def change_interface(self, frame_ind):
        """change frames"""
        # remove focus from entry
        self.interface.focus()
        self.interface.grid_remove()

        if frame_ind == 0:
            self.interface = self.window
            self.indList = self.indL
            self.ErLabListNew = self.ErLabLi
            self.entriesListNew = self.entrLst

        elif frame_ind == 1:
            self.interface = self.window1
            self.indList = self.indL1
            self.ErLabListNew = self.ErLabLi1
            self.entriesListNew = self.entrLst1

        else:
            self.interface = self.window2
            self.ErLabListNew = self.ErLabLi2
            self.entriesListNew = self.entrLst2

        self.interface.grid(row=1, column=0, pady=(0, 0), padx=(0, 0))

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
    def popup_info(self):
        """info"""
        CTkMessagebox(self, title="Info", justify="center", icon_size=(30, 30), font=('Helvetica', 14),
                      message="Formulas and data sources:\nhollow sections:\n\
    EN10210-2 p.14-15\n\
    EN10219-2 p.20-22\nI sections:\n\
    EN10365 p.8-10\n\nby Mozkovyi O.I")

    ########################
    def sliding(self, value, frame_ind):
        """show slide value"""
        self.list_trick()
        self.interface.sliderLabel.label.configure(text=str(int(value)) + "m")
        self.goto_count(frame_ind)

    ########################
    def optionmenu_callback(self, frame_ind):
        """combobox, redirect to goto_count"""
        self.list_trick()
        self.goto_count(frame_ind)

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
                    self.entriesList[int(er_label_num)].configure(border_color=self.theme_color, validate="all")
                    return False
                else:
                    if int(inp) <= 10000:
                        self.entriesList[int(er_label_num)].configure(border_color=self.densChangedC)
                        return True
                    else:
                        self.fill_label(er_label_num, 88)
                        return False
            elif inp == "":
                self.entriesList[int(er_label_num)].configure(border_color=self.theme_color)
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
                    self.entriesList[int(er_label_num)].configure(border_color=self.origEntBorderColor, validate="all")
                    return False
                else:
                    # check max absolute value
                    if self.check_abs_max(er_label_num, inp):
                        # change indList value
                        self.change_indicator(er_label_num, True)
                        # give main color(green, blue)
                        self.entriesList[int(er_label_num)].configure(border_color=self.theme_color)
                        return True
                    else:
                        if er_label_num == "2":
                            self.fill_label(er_label_num, 45)
                        else:
                            self.fill_label(er_label_num, 44)
                        return False
            elif inp == "":
                self.change_indicator(er_label_num, False)
                self.entriesList[int(er_label_num)].configure(border_color=self.origEntBorderColor)
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
                        self.entriesList[int(er_label_num)].configure(border_color=self.origEntBorderColor,
                                                                      validate="all")
                        return False
                    if self.check_abs_max(er_label_num, inp):
                        if len(inp.split(".")[1]) > 2:
                            self.fill_label(er_label_num, 33)
                            return False
                        else:
                            self.change_indicator(er_label_num, True)
                            self.entriesList[int(er_label_num)].configure(border_color=self.theme_color)
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
    def goto_count(self, frame_ind):  # , event=None,
        """keyrelease event, main function"""
        match frame_ind:
            case 0 | 1:
                # check all indicators
                for i, each in enumerate(self.indList):
                    if not each:
                        self.entriesList[4].configure(state="normal")
                        self.entriesList[4].delete("0", "end")
                        # readonly state kills placeholder if it defines in same configure
                        self.entriesList[4].configure(placeholder_text="result")
                        self.entriesList[4].configure(state="readonly", border_color=self.origEntBorderColor)
                        # if remove not thickness value, change border to green 
                        if i != 2:
                            if self.is_float(self.entriesList[2].get()):
                                self.entriesList[2].configure(border_color=self.theme_color)
                                if self.ErLabList[2].cget("text") == "too large thickness":
                                    self.clear_label("2")
                        return
                # get parameters
                width = float(self.entriesList[0].get().replace(",", "."))
                height = 10000
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
                    # print(self.interface.combobox.cget("bg_color"))
                    ro = 0
                    ri = 0
                    spreadsheet = ""
                    if standard == "EN10210":
                        match frame_ind:
                            case 0:
                                ro = 1.5 * thickness
                                ri = thickness
                                # for database
                                spreadsheet = "rectEN10210"
                            case 1:
                                spreadsheet = "circleEN10210"
                    else:
                        match frame_ind:
                            case 0:
                                if thickness <= 6:
                                    ro = 2 * thickness
                                    ri = thickness
                                elif 6 < thickness <= 10:
                                    ro = 2.5 * thickness
                                    ri = 1.5 * thickness
                                elif thickness > 10:
                                    ro = 3 * thickness
                                    ri = 2 * thickness
                                spreadsheet = "rectEN10219"
                            case 1:
                                spreadsheet = "circleEN10219"
                    # counting
                    if frame_ind == 0:
                        area = (2 * thickness * (width + height - 2 * thickness) - (4 - 3.141592) * (
                                ro * ro - ri * ri)) / 100
                    else:
                        area = 3.141592 * (width ** 2 - (width - 2 * thickness) ** 2) / 400

                    self.put_sumtext(area, standard)

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
                                        height) + ") OR (W =" + str(width) + " ANd H =" + str(
                                        height) + ")) and T =" + str(thickness))
                        case 1:
                            self.cursor.execute(
                                "SELECT * FROM " + spreadsheet + " WHERE W =" + str(width) + " and T =" + str(
                                    thickness))
                    data01 = self.cursor.fetchall()

                    if len(data01) == 0:
                        self.ErLabList[4].configure(text="this size is not in the standard")
                        self.entriesList[4].configure(state="readonly", border_color=self.densChangedC)
                    else:
                        self.entriesList[4].configure(state="readonly", border_color=self.theme_color)
                        self.ErLabList[4].configure(text="")

                else:
                    self.entriesList[4].configure(state="normal")
                    self.entriesList[4].delete("0", "end")
                    # readonly state kills placeholder if it defines in the same configure
                    self.entriesList[4].configure(placeholder_text="result")
                    self.entriesList[4].configure(state="readonly", border_color=self.origEntBorderColor)
                    self.ErLabList[4].configure(text="")
            case 2:
                self.list_trick()
                profile_name = self.interface.scrollable_button_frame.button_chosen
                standard = self.interface.combobox.combobox.get()
                spreadsheet = ""
                if standard == "EN10365":
                    spreadsheet = "IPE_EN10365"
                if profile_name is not None:
                    self.cursor.execute("SELECT * FROM " + spreadsheet + " WHERE N = '" + str(profile_name) + "' ")
                    data = self.cursor.fetchall()
                    area = data[0][7]

                    hei = data[0][3]
                    if hei.is_integer():
                        hei = int(hei)
                    sizes_text = (str(data[0][1]) + " (" + str(hei).replace(".", ",") + "x" +
                                  str(data[0][4]) + "x" + str(data[0][6]).replace(".", ",") + ")")
                    standard = sizes_text  # ! caution

                    self.put_sumtext(area, standard)
                    self.entriesList[4].configure(state="readonly", border_color=self.theme_color)

    #############################
    def give_color_th(self, th, smaller):
        """give or not color for thickness entry"""
        if th > smaller / 4:
            self.fill_label("2", 66)
            self.entriesList[2].configure(border_color="red")
            return False
        else:
            self.entriesList[2].configure(border_color=self.theme_color)
            if self.ErLabList[2].cget("text") == "too large thickness":
                self.clear_label("2")
            return True

    ##############################
    def get_mass(self, area):
        """return mass and length"""
        length = int(self.interface.slider.slider.get())
        # get density
        try:
            density = float(self.entriesList[3].get()) / 10000
        except (Exception,):
            density = 0.785
        mass = round(density * area * length, 2)
        # remove ",oo" if necessary
        if mass.is_integer():
            mass = int(mass)
        return mass, length

    ##############################
    def put_sumtext(self, area, standard):
        """put sum text in result entry"""
        mass, length = self.get_mass(area)

        sumtext = standard + " - " + str(length) + "m - " + str(mass).replace(".", ",") + "kg"

        self.entriesList[4].configure(state="normal")
        self.entriesList[4].delete("0", "end")
        self.entriesList[4].insert(0, sumtext)

    #############################
    def create_table(self, conn):
        """create new table for database"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS rectEN10210 ([W] REAL, [H] REAL, [T] REAL, [M] REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS rectEN10219 ([W] REAL, [H] REAL, [T] REAL, [M] REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS circleEN10210 ([W] REAL, [T] REAL, [M] REAL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS circleEN10219 ([W] REAL, [T] REAL, [M] REAL)")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS IPE_EN10365 ([N] REAL, [M] REAL, "
            "[h] REAL, [b] REAL, [s] REAL, [t] REAL, [A] REAL)")

        conn.commit()
        # read and rewrite tables
        spreadsheet = pandas.read_excel("metalDB.xlsx", "10210")
        spreadsheet.to_sql(name='rectEN10210', con=conn, if_exists="replace")

        spreadsheet = pandas.read_excel("metalDB.xlsx", "10219")
        spreadsheet.to_sql(name='rectEN10219', con=conn, if_exists="replace")

        spreadsheet = pandas.read_excel("metalDB.xlsx", "C10210")
        spreadsheet.to_sql(name='circleEN10210', con=conn, if_exists="replace")

        spreadsheet = pandas.read_excel("metalDB.xlsx", "C10219")
        spreadsheet.to_sql(name='circleEN10219', con=conn, if_exists="replace")

        spreadsheet = pandas.read_excel("metalDB.xlsx", "IPE")
        spreadsheet.to_sql(name='IPE_EN10365', con=conn, if_exists="replace")

        # self.cursor.execute("SELECT * FROM IPE_EN10365 WHERE N = 'IPE 100' ")
        # data = self.cursor.fetchall()

        conn.close()

    #############################
    def list_trick(self):
        """lists trick for avoiding add artifacts"""
        self.ErLabList = self.ErLabListNew
        self.entriesList = self.entriesListNew


###################################################################
class UpperMenu(ctk.CTkFrame):
    """upper menu"""
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")

        self.holSecBt = MenuButton(self, 0, "rectang.png", master.hoverBtColor)
        self.circleBt = MenuButton(self, 1, "green-circle.png", "transparent")
        self.beamBt = MenuButton(self, 2, "i-beam.png", "transparent")

        self.buttonList = (self.holSecBt.button, self.circleBt.button, self.beamBt.button)

        # info button
        MenuButton(self, 3, "information.png", "transparent")  # InfoBt =

    def change_fg(self, column):
        """change foreground of side menu button"""
        for each in self.buttonList:
            if each.cget("fg_color") != "transparent":
                each.configure(fg_color="transparent")
                break
        self.buttonList[column].configure(fg_color=self.master.hoverBtColor)
        self.master.change_interface(column)


#########
class MenuButton:
    """buttons for upper menu"""
    def __init__(self, master, column, image_name, hover_color):
        super().__init__()
        if image_name == "information.png":
            comm = master.master.popup_info
        else:
            comm = lambda: master.change_fg(column)
        image = ctk.CTkImage(Image.open(App.resource_path("assets\\" + image_name)), size=(28, 28))
        self.button = ctk.CTkButton(master, text="", image=image, width=28, fg_color=hover_color,
                                    border_width=0, command=comm)
        self.button.grid(row=0, column=column, pady=(0, 0), padx=(0, 5))


###################################################################
class BuildInterface(ctk.CTkFrame):
    """build frame"""
    def __init__(self, master, frame_ind):
        super().__init__(master)
        self.configure(fg_color="transparent")
        ###############

        # some paddings
        lpadx = 30  # left padx
        lpadx2 = 25  # left padx 2-nd column
        hpady = 7  # upper pady
        lwpady = 5  # lower pady
        justify = "left"

        # elements' width
        elem_width = 135
        # for slider
        sl_lab_width = 30
        # fonts
        self.custom_font = ('Helvetica', 15)

        if frame_ind == 0:
            minus_row = 0
        else:
            minus_row = 2
        if frame_ind == 2:
            combo_list = ["EN10365"]
        else:
            combo_list = ["EN10210", "EN10219"]
        #######################
        # register validation
        vcmd_wht = (master.register(master.valid_wht))
        vcmd_d = (master.register(master.valid_dens))

        match frame_ind:
            case 0 | 1:
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

            case 2:
                # get list of profiles
                master.cursor.execute("SELECT N FROM IPE_EN10365 ")
                data = list(master.cursor.fetchall())
                self.listOfProfiles = list()
                for each in data:
                    self.listOfProfiles.append(list(each)[0])

                self.scrollable_button_frame = ScrollableButtonFrame(self, width=108, height=100, border_width = 2,
                                                                    border_color=master.origEntBorderColor,)
                self.scrollable_button_frame.grid(row=0, column=0, padx=(lpadx, 0), pady=(hpady + 15, lwpady), rowspan=4, 
                                                  columnspan = 1, sticky = "nesw")
                self.scrollable_button_frame._scrollbar.configure(height=0)
                self.scrollable_button_frame._scrollbar.grid(row=1, column=1, sticky="nsew", padx=(0, 3))
                self.scrollable_button_frame.add_items(self.listOfProfiles)

                # image = ctk.CTkImage(Image.open(App.resource_path("assets\\search-50.png")), size=(28, 28))
                self.Sentry = ctk.CTkEntry(self, width=elem_width, placeholder_text="search", font=self.custom_font,
                                           justify=justify) #image = image,
                self.Sentry.bind("<KeyRelease>", self.search)
                self.Sentry.grid(row=0, column=1, padx=(lpadx2, 0), pady=(hpady + 15, lwpady))

        # options menu for standards
        self.combobox = CreateCombobox(self, [1, 1], [lpadx2, 0], [0, lwpady], combo_list, elem_width, self.custom_font,
                                       justify, frame_ind)

        self.dLabel = CreateLabels(self, [2, 1], [lpadx2, 0], [0, 0], elem_width, "w", 1)
        self.dens_entry = CreateEntry(self, [3, 1], [lpadx2, 0], [0, lwpady], elem_width, "7850kg/cub.m", self.custom_font,
                                      vcmd_d, justify, 3, "w", 1, frame_ind)
        self.dens_entry.entry.configure(border_color=master.theme_color)

        # slider section + label
        self.slider = CreateSlider(self, [6 - minus_row, 0], [lpadx, 0], [lwpady, 0], lpadx2, elem_width, sl_lab_width,
                                   frame_ind)
        self.sliderLabel = CreateLabels(self, [6 - minus_row, 1], [lpadx2, 0], [lwpady, 0], sl_lab_width, "e", 1)
        self.sliderLabel.label.configure(height=28, text=str(1) + "m", anchor="e", font=self.custom_font,
                                         text_color=master.textColor)

        # result
        self.sumLabel = CreateLabels(self, [7 - minus_row, 0], [lpadx, 0], [0, 0], elem_width, "we", 2)
        self.sumEntry = CreateEntry(self, [8 - minus_row, 0], [lpadx, 0], [0, 0], elem_width, "result", self.custom_font,
                                    vcmd_wht, "center", 2, "we", 2, frame_ind)
        self.sumEntry.entry.unbind()
        self.sumEntry.entry.configure(state="readonly")

        if frame_ind == 2:
            self.combobox.combobox.grid(row=1, column=1, padx=(lpadx2, 0), pady=(15, lwpady))
            self.dens_entry.entry.configure(border_color=master.theme_color)

    ############
    def search(self, event):
        """search in listbox"""
        event.widget.configure(state="disabled")
        value = event.widget.get()
        if value == "":
            data = self.listOfProfiles
        else:
            data = []
            for item in self.listOfProfiles:
                if value.lower() in item.lower():
                    data.append(item)

        for widget in self.scrollable_button_frame.winfo_children():
            widget.destroy()
        
        self.scrollable_button_frame._parent_canvas.yview_moveto(0) # move to start of the list
        if len(data)>0:
            self.scrollable_button_frame.add_items(data)
            # self.scrollable_button_frame._scrollbar.configure(minimum_pixel_length=20) # change in ctk_scrollabel_frame.py! 
        else:
            # self.scrollable_button_frame._scrollbar.configure(minimum_pixel_length=110)
            pass
        # print(self.scrollable_button_frame._scrollbar.cget("minimum_pixel_length"))
        
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
                                        command=lambda value=None, ind=frame_ind:
                                        master.master.optionmenu_callback(ind),
                                        border_color=master.master.theme_color,
                                        button_color=master.master.theme_color,
                                        justify=justify)
        self.combobox.set(val_list[0])
        self.combobox.grid(row=row_col[0], column=row_col[1], padx=(padx_l[0], padx_l[1]), pady=(pady_l[0], pady_l[1]))


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
        
        self.button_chosen = ctk.StringVar(value="")
        self.initial_bt_list = []

    def add_items(self, list_of_values):
        self.initial_bt_list.clear()
        for j, each in enumerate(list_of_values):
            self.add_item(each, j)
        
        """why this is not working?"""
        # for j, each in enumerate(list_of_values):
        #     self.button = ctk.CTkButton(self, text=each, height=24, width=108, fg_color="transparent", font=self.master.master.master.custom_font, 
        #                        anchor= "w", command=lambda: self.change_bt_chosen(each))
        #     self.button.grid(row=j, column=0, pady=(0, 2), padx=0)

    def add_item(self, item, j):
        self.button = ctk.CTkButton(self, text=item, height=24, width=108, fg_color="transparent", font=self.master.master.master.custom_font, 
                               anchor= "w", command=lambda: self.change_bt_chosen(item, j))
        self.button.grid(row=j, column=0, pady=(0, 2), padx=0)
        self.initial_bt_list.append(self.button)
    
    def change_bt_chosen(self, value, bt_ind):       
        color = self.master.master.master.master.theme_color #how to get rid of this 'master' train?
        for widget in self.initial_bt_list:
            if widget.cget("fg_color") == color:
                widget.configure(fg_color= "transparent")
                break
        self.initial_bt_list[bt_ind].configure(fg_color= color)
        self.button_chosen = value
        self.master.master.master.master.goto_count(2)


###########################################################################################
class ImageSide(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="transparent")


###########################################################################################
if __name__ == "__main__":
    ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
    app = App()
    app.mainloop()
