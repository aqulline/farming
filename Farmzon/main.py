import os
import re
import threading
import phonenumbers
import plyer
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from datetime import datetime

from kivy.utils import platform
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.image import AsyncImage
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
import kivy.uix.screenmanager as SM
from kivymd.toast import toast
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldRound

from Address_location import Location_Address as LA

from Database_class import Upload_image as UI

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"


class NumberOnly(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnly, self).insert_text(s, from_undo=from_undo)


class NumberOnlyRound(MDTextFieldRound):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat

        if "." in self.text:
            s = re.sub(pat, "", substring)

        else:
            s = ".".join([re.sub(pat, "", s) for s in substring.split(".", 1)])

        return super(NumberOnlyRound, self).insert_text(s, from_undo=from_undo)


class category(MDCard, AsyncImage):
    pass


class round_image(MDBoxLayout):
    pass


class cat_image(AsyncImage):
    pass


class Labels(MDLabel):
    pass


class products_cards(MDCard):
    pass


class number_of_app:
    times = 0


class main(MDApp):
    spin_active = BooleanProperty(False)
    storage_url = "https://farmzon-abdcb.appspot.com"
    database_url = "https://farmzon-abdcb.firebaseio.com/.json"
    data = {"uu": {"Joe Tilsed": "me"}}
    auth_key = "sBlt6fzvguYnrGl2FlXRK3k4vRxSfZJBV2P7yIRv"
    # Clock.max_iteration = 20
    size_x = NumericProperty(0)
    size_y = NumericProperty(0)
    count = 11
    count_screen = NumericProperty(0)
    dialog = None

    # XXX-------USER LOGIN VAR-------XXX
    user_name = StringProperty("")
    user_phone = StringProperty("")
    user_password = StringProperty("")
    user_city = StringProperty("")
    user_email = StringProperty("")
    user_address = StringProperty("")
    user_location = StringProperty("")
    user_image = StringProperty("")
    user_products = StringProperty("")
    user_followers = StringProperty("")
    user_purchased = StringProperty("")
    user_latitude = StringProperty("")
    user_longitude = StringProperty("")
    user_true = BooleanProperty(False)

    # XXX-------ADMIN LOGIN VAR-------XXX
    admin_name = StringProperty("")
    admin_phone = StringProperty("")
    admin_password = StringProperty("")
    admin_city = StringProperty("")
    admin_email = StringProperty("")
    admin_address = StringProperty("")
    admin_image = StringProperty("")
    admin_products = StringProperty("")
    admin_followers = StringProperty("")
    admin_purchased = StringProperty("")
    admin_true = BooleanProperty(False)

    # XXX-------USER REGISTER VAR-------XXX
    admin_r_name = StringProperty("")
    admin_r_phone = StringProperty("")
    admin_r_password = StringProperty("")
    admin_r_city = StringProperty("")
    admin_r_email = StringProperty("")
    admin_r_address = StringProperty("")
    type_business = StringProperty("company")

    # XXX-------USER REGISTER VAR-------XXX
    user_r_name = StringProperty("")
    user_r_phone = StringProperty("")
    user_r_password = StringProperty("")
    user_r_city = StringProperty("")
    user_r_email = StringProperty("")
    user_r_address = StringProperty("")

    # XXX-------CATEGORIES VAR----------XXX
    real_source = StringProperty("")
    label_name = StringProperty("")
    food_count = NumericProperty(0)
    fruit_count = NumericProperty(0)
    herbs_count = NumericProperty(0)

    # XXX------PRODUCT VAR-------XXX
    products_id = StringProperty("")
    product_image = StringProperty("")
    product_name = StringProperty("")
    product_max_price = StringProperty("")
    product_min_price = StringProperty("")
    product_full_sack = NumericProperty(0)
    product_half_sack = NumericProperty(0)
    product_date = StringProperty("")
    product_month = StringProperty("")
    product_year = StringProperty("")
    product_time = StringProperty("")
    product_state = StringProperty("")
    screen_name = []

    # XXX------FRIENDLY FUNCTIONS------XXX

    def __init__(self, **kwargs):
        super().__init__()
        self.file_manager = MDFileManager()
        self.file_manager.exit_manager = self.exit_manager
        self.file_manager.select_path = self.select_path
        self.file_manager.preview = True
        self.file_manager.previous = True
        # self.file_manager.search = "files"

    def remember_me(self, user, password, name, image):
        with open("login.txt", "w") as fl:
            fl.write(user + "\n")
            fl.write(password)
        with open("user_info.txt", "w") as ui:
            ui.write(image + "\n")
            ui.write(name)
        fl.close()
        ui.close()

    def remember_me_admin(self, user, password, name, image):
        with open("admin.txt", "w") as fl:
            fl.write(user + "\n")
            fl.write(password)
        with open("admin_info.txt", "w") as ui:
            ui.write(image + "\n")
            ui.write(name)
        fl.close()
        ui.close()

    def Permission(self, android=None):
        if platform == 'android':
            from android.permissions import request_permissions, Permission  # todo
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])  # todo
            self.file_manager_open()  # todo

    def check(self):
        te = self.root.ids.user_phone
        tex = te.text
        te.helper_text_mode = "on_focus"
        te.helper_text = "remain" + " " + str(self.count)
        self.count = tex.__len__()
        self.count = 10 - self.count
        if tex.__len__() < 10 or tex.__len__() > 10:
            te.icon_right = "alpha-x"
            te.icon_right_color = 1, 0, 0, 1
        elif tex.__len__() == 10:
            te.icon_right = "check"
            te.icon_right_color = 0, 1, 0, 1
            te.helper_text = "correct"

    def phone_number(self, phone):
        new_number = ""
        for i in range(phone.__len__()):
            if i == 0:
                pass
            else:
                new_number = new_number + phone[i]
        number = "+255" + new_number
        if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
            toast("wrong number")
            te = self.root.ids.user_phone
            te.text = "start with 07 or 06"
            return False
        else:
            return True

    def dark(self):
        self.theme_cls.theme_style = "Dark"

    def light(self):
        self.theme_cls.theme_style = "Light"

    def actively(self):
        if self.spin_active:
            self.spin_active = False

    def actively_reg(self):
        sm = self.root
        if self.spin_active:
            self.spin_active = False
            sm.current = "login screen"
            toast("Succefull Registerd!")

    def on_start(self):
        # screen manager
        sm = self.root
        sm.transition = SM.FadeTransition(duration=.2)
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        self.user_memory()
        self.fps_monitor_start()

    def user_memory(self):
        file_size = os.path.getsize("login.txt")
        if file_size == 0:
            pass
        else:
            sm = self.root
            self.user_true = True
            file1 = open('login.txt', 'r')
            file2 = open("user_info.txt")
            Lines = file1.readlines()
            Lines2 = file2.readlines()
            count = 0
            # Strips the newline character
            self.user_phone = Lines[0].strip()
            self.user_password = Lines[1].strip()
            self.user_name = Lines2[1]
            self.user_image = "alpha-" + self.user_name[0].lower()
            self.Signing_in(self.user_phone, self.user_password)
            sm.current = "main"

    def admin_memory(self):
        file_size = os.path.getsize("admin.txt")
        if file_size == 0:
            sm = self.root
            sm.current = "login_screen_admin"
            self.count_screen += 1
        else:
            sm = self.root
            self.admin_true = True
            file1 = open('admin.txt', 'r')
            file2 = open("admin_info.txt")
            Lines = file1.readlines()
            Lines2 = file2.readlines()
            count = 0
            # Strips the newline character
            self.admin_phone = Lines[0].strip()
            self.admin_password = Lines[1].strip()
            self.admin_name = Lines2[1]
            self.admin_image = Lines2[0]
            self.Signing_in_admin(self.admin_phone, self.admin_password)
            sm.current = "admin_main"
            self.count_screen += 1

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Do you real want to quit?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.kill
                    ),
                    MDRaisedButton(
                        text="QUIT!", text_color=self.theme_cls.primary_color, on_release=quit
                    ),
                ],
            )
        self.dialog.open()

    def kill(self, *kwargs):
        self.dialog.dismiss()

    def hook_keyboard(self, window, key, *largs):
        count = self.screen_name.__len__() - 1
        sm = self.root
        if key == 27 and self.count_screen == 0:
            self.show_alert_dialog()
            return True
        elif key == 27 and self.count_screen > 0:
            sm.current = "main"
            self.count_screen -= 1
            return True

    def resize_bottom_tabs(self):
        # bottom_nav
        bv = self.root.ids.bottom_nav
        bv.on_resize()

    def screen_collector(self, name):
        self.screen_name.append(name)

        return self.screen_name.__len__()

    def Screen_changer(self, screen_name):
        sm = self.root
        sm.current = screen_name

    # XXX-------PROFILE VALIDATIONS FUNCTIONS------XXX
    def validate_user(self, phone, password):
        if phone == "":
            toast("please enter your phone number correctly")
        elif password == "":
            toast("please enter your password")
        else:
            self.spin_active = True
            self.Signing_in(phone, password)

    def Signing_in(self, phone, password):
        thread = threading.Thread(target=self.Signing_in_function, args=(phone, password,))
        thread.start()

    def Signing_in_function(self, phone, password):
        if phone != "" and password != "":
            if UI.Signing_in(UI(), phone, password):
                sm = self.root
                # image = self.root.ids.user_image
                # taken from database
                self.user_name = UI.name
                self.user_image = "alpha-" + self.user_name[0].lower()
                self.remember_me(phone, password, self.user_name, UI.image)
                # image.source = UI.image
                # Clock.schedule_interval(lambda x: self.image_loader_user(UI.image), 1)
                self.user_purchased = UI.purchased
                self.user_products = UI.product
                self.user_followers = UI.follower
                if not self.user_true:
                    sm.current = "main"
                    self.screen_collector("main")
                    self.spin_active = False

            else:
                toast("oop! phone number or password in correct or "
                      "check your internet connection", 5)
                self.spin_active = False

    def image_loader_user(self, y):
        image = self.root.ids.drawer_logo
        Cache.remove(image.texture)
        image.source = y
        image.reload()

    def validate_registration1(self, name, phone, password, city, email, address):
        self.spin_active = True
        Clock.schedule_once(lambda x: self.validate_registration(name, phone, password, city, email, address), 2)

    def validate_registration(self, name, phone, password, city, email, address):
        if city != " " and address != " " and city.isalpha() and address.isalpha():
            if self.phone_number(phone):
                self.user_location = address + "/" + city
                sm = self.root
                if LA.Generate_address(LA(), self.user_location):
                    self.user_location = str(LA.location2)
                    self.user_latitude = str(LA.latitude)
                    self.user_longitude = str(LA.longitude)
                    if name != "" and phone != "" and phone.__len__() == 10 and password != "" and city != "" and address != "" and email != "" and email.count(
                            "@") == 1 and email.count(".") > 0:
                        self.spin_active = True
                        self.register(name, phone, password, city, address, email, self.user_location,
                                      self.user_latitude,
                                      self.user_longitude)

                    else:
                        toast("something is wrong")
                        self.spin_active = False
                else:
                    toast("your address is not available")
                    self.spin_active = False
                    city = self.root.ids.user_city
                    district = self.root.ids.user_address
                    city.text = " "
                    district.text = " "
            else:
                toast("check your phone number")
                self.spin_active = False
        else:
            toast("your city, address and phone number invalid", 3)
            self.spin_active = False
            city = self.root.ids.user_city
            district = self.root.ids.user_address
            city.text = " "
            district.text = " "

    def register(self, name, phone, password, city, address, email, location, latitude, longitude):
        thread = threading.Thread(target=UI.upload_data_user,
                                  args=(
                                      UI(), name, phone, password, city, address, email, location, latitude, longitude))
        thread.start()
        thread.join()

        self.actively_reg()

    def register_user(self):
        sm = self.root
        sm.current = "register screen"
        self.screen_collector("register screen")

    # XXX-------ADMIN FUNCTIONS------XXX

    def validate_admin(self, phone, password):
        if phone == "" and phone.Isdigit():
            toast("please enter your phone number correctly")
        elif password == "":
            toast("please enter your password")
        else:
            self.spin_active = True
            thread = threading.Thread(target=self.Signing_in_admin_function, args=(phone, password))
            thread.start()

    def Signing_in_admin(self, phone, password):
        thread = threading.Thread(target=self.Signing_in_admin_function, args=(phone, password,))
        thread.start()

    def Signing_in_admin_function(self, phone, password):
        if UI.Signing_in_admin(UI(), phone, password):
            sm = self.root
            image = self.root.ids.admin_image
            self.admin_name = UI.name_admin
            self.admin_image = UI.image_admin
            image.source = UI.image_admin
            Clock.schedule_interval(lambda x: self.image_loder_admin(UI.image_admin), 0.1)
            self.admin_purchased = UI.purchased_admin
            self.admin_products = UI.product_admin
            self.admin_followers = UI.follower_admin
            self.remember_me_admin(phone, password, self.admin_name, self.admin_image)
            if not self.admin_true:
                sm.current = "admin_main"
        else:
            self.spin_active = False
            toast("oops! phone number or password in correct")

    def image_loder_admin(self, x):
        image = self.root.ids.admin_image

        image.source = x

    def validate_registration_admin(self, name, phone, password, city, email, address):
        if name != "" and phone != "" and password != "" and city != "" and address != "" and email != "" and email.count(
                "@") == 1 and email.count(".") > 0:
            self.spin_active = True
            thread = threading.Thread(target=self.admin_register,
                                      args=(name, phone, password, city, address, email, self.type_business))
            thread.start()
        else:
            toast("something is wrong!")

    def admin_register(self, name, phone, password, city, address, email, business):
        thread = threading.Thread(target=UI.upload_data_admin,
                                  args=(UI(), name, phone, password, city, address, email, self.type_business))

        thread.start()
        thread.join()
        toast("registered")
        self.spin_active = False
        self.Screen_changer("login_screen_admin")

    def catergory_food_spinner1(self):
        self.spin_active = True
        Clock.schedule_once(lambda x: self.add_image_food("food", "categories_food"), 2)

    def add_image_food(self, cat, screen):
        from connection_status import connect
        if self.food_count == 0:
            self.food_count = self.food_count + 1
            if connect():
                food = self.root.ids.food_cat
                from firebase_admin import credentials, initialize_app, db
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="food")
                store = db.reference("Categories_url", default_app).child(cat)
                stores = store.get()
                for y, x in stores.items():
                    self.real_source = x["url"]
                    food_categories = category()
                    food_categories.add_widget(Labels(text=y))
                    food_categories.add_widget(MDSeparator(height="1dp"))
                    food_categories.add_widget(cat_image(source=self.real_source))
                    food.add_widget(food_categories)
                    sm = self.root
                    sm.current = screen
        else:
            sm = self.root
            sm.current = screen

    def catergory_fruit_spinner2(self):
        self.spin_active = True
        Clock.schedule_once(lambda x: self.add_image_fruit("fruit", "categories_fruit"), 2)

    def add_image_fruit(self, cat, screen):
        from connection_status import connect
        if self.fruit_count == 0:
            self.fruit_count = self.fruit_count + 1
            if connect():
                food = self.root.ids.fruit_cat
                from firebase_admin import credentials, initialize_app, db
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="fruit")
                store = db.reference("Categories_url", default_app).child(cat)
                stores = store.get()
                for y, x in stores.items():
                    self.real_source = x["url"]
                    food_categories = category()
                    food_categories.add_widget(Labels(text=y))
                    food_categories.add_widget(MDSeparator(height="1dp"))
                    food_categories.add_widget(cat_image(source=self.real_source))
                    food.add_widget(food_categories)
                    sm = self.root
                    sm.current = screen
        elif self.fruit_count != 0:
            sm = self.root
            sm.current = screen

    def catergory_herbs_spinner3(self):
        self.spin_active = True
        Clock.schedule_once(lambda x: self.add_image_herbs("herbs", "categories_herbs"), 2)

    def add_image_herbs(self, cat, screen):
        from connection_status import connect
        if self.herbs_count == 0:
            self.herbs_count = self.herbs_count + 1
            if connect():
                food = self.root.ids.herb_cat
                from firebase_admin import credentials, initialize_app, db
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="herbs")
                store = db.reference("Categories_url", default_app).child(cat)
                stores = store.get()
                for y, x in stores.items():
                    self.real_source = x["url"]
                    food_categories = category()
                    food_categories.add_widget(Labels(text=y))
                    food_categories.add_widget(MDSeparator(height="1dp"))
                    food_categories.add_widget(cat_image(source=self.real_source))
                    food.add_widget(food_categories)
                    sm = self.root
                    sm.current = screen
        else:
            sm = self.root
            sm.current = screen

    def type_active(self, checkbox, value):
        if value:
            self.type_business = "company"
            toast(self.type_business)
        else:
            self.type_business = "individual"
            toast(self.type_business)

    # XXX------- PRODUCTS_FUNCTION---------XXX

    def Product_validation(self, name, max, min, date, month, year, description):
        if name != "" and max != "" and min != "" and date != "" and month != "" and year != "" and description != "":
            self.product_name = name
            self.product_date = date
            self.product_year = year
            self.product_month = month
            self.product_max_price = max
            self.product_min_price = min
            self.products_id = datetime.now()

    # XXX-------FILE_MANAGER------XXX

    def file_manager_open(self):
        from android.storage import primary_external_storage_path  # todo
        primary_ext_storage = primary_external_storage_path()  # todo
        self.file_manager.show("/")  # todo
        self.file_manager.show(primary_ext_storage)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """

        self.exit_manager()
        toast(path)
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            toast("correct format")
            image = self.root.ids.product_image

            image.source = path
            self.product_image = path
        else:
            toast("Wrong format")

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.accent = "Brown"
        # Window.size = (360, 640)
        print(plyer.uniqueid.id)
        self.size_x, self.size_y = Window.size
        self.title = "farmzon"


# requests.patch(url=self.database_url, json=self.data)
# requests.delete(url="https://farmzon-abdcb.firebaseio.com/uu/.json")
# require = requests.get(url="https://farmzon-abdcb.firebaseio.com/name/.json" + "?auth=" + self.auth_key)
# print(require.json())


if __name__ == "__main__":
    main().run()
