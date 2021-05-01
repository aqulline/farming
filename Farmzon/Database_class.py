import datetime


# from main import number_of_app

def get_date():
    return str(datetime.datetime.now()).split(" ")[0]


class Upload_image:
    # Init firebase with your credentials
    url = ""
    name = ""
    admin_name = ""
    times = 0
    amount = 0
    pic_url = ""
    pic_name = ""
    image = ""
    follower = ""
    product = ""
    purchased = ""
    name_admin = ""
    image_admin = ""
    follower_admin = ""
    product_admin = ""
    purchased_admin = ""

    product_image = ""

    def rchop(sself, s, suffix):
        if suffix and s.endswith(suffix):
            return s[:-len(suffix)]
        return s

    def uploadima(self):
        from connection_status import connect
        if connect():
            from firebase_admin import credentials, initialize_app, storage
            import firebase_admin
            import pathlib
            if not firebase_admin._apps:
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'storageBucket': 'farmzon-abdcb.appspot.com'})
                # print(uploadima_app.name)
                list_food = [
                    "avocado.png", "pea.png", "carrot.png", "cucumber.png",
                    "capsicum.png", "onion.png", "clove.png"
                ]
                for i in range(list_food.__len__()):
                    fileName = "farmzon database/herbs/herbs/" + list_food[i]
                    bucket = storage.bucket()
                    suf = pathlib.Path(list_food[i]).suffix
                    name = self.rchop(list_food[i], ".png")
                    blob = bucket.blob("Categories_url/herbs/" + name.lower())
                    blob.upload_from_filename(fileName)
                    blob.make_public()
                    self.url = blob.public_url
                    print("your file url", self.url)
                    self.product_image = self.url
                    self.put_in_database(self.url, name.lower())

    def upload_product_image(self, home, cate, path, name):
        from connection_status import connect
        if connect():
            from firebase_admin import credentials, initialize_app, storage
            import firebase_admin
            import pathlib
            if not firebase_admin._apps:
                fileName = path
                cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'storageBucket': 'farmzon-abdcb.appspot.com'})
                bucket = storage.bucket()
                blob = bucket.blob(home + "/" + cate + "/" + name)
                blob.upload_from_filename(path)
                blob.make_public()
                self.url = blob.public_url
                print("your file url", self.url)

    def put_in_database(self, url, name):
        from connection_status import connect
        if connect():
            from firebase_admin import credentials, initialize_app, db
            import firebase_admin
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                         name="new" + name)
            # print(default_app.name)
            users = db.reference("Categories_url", default_app, 'https://farmzon-abdcb.firebaseio.com/').child(
                "herbs").child(name)
            users.set({
                "url": url
            })

    def upload_data_user(self, name, phone, password, city, address, email, location, latitude, longitude):
        from connection_status import connect
        if connect():
            from main import number_of_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_of_app.times == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print(default_app.name)
                number_of_app.times += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_of_app.times))
                print(default_app.name)
                number_of_app.times += 1
            ref = db.reference('Users').child(phone)
            ref.set({
                "name": name,
                "phone": phone,
                "password": password,
                "city": str(city),
                "address": address,
                "location": location,
                "latitude": latitude,
                "longitude": longitude,
                "email": email,
                "date": get_date(),
                "Purchased": "0",
                "Followed": "0",
                "Orders": "0",
            })
            print("ok")

    def upload_data_admin(self, name, phone, password, city, address, email, business):
        from connection_status import connect
        if connect():
            from main import number_of_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_of_app.times == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print(default_app.name)
                number_of_app.times += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_of_app.times))
                print(default_app.name)
                number_of_app.times += 1
            ref = db.reference('Admins').child(phone)
            ref.set({
                "name": name,
                "phone": phone,
                "password": password,
                "city": str(city),
                "address": address,
                "email": email,
                "date": get_date(),
                "b_type": business,
                "Purchased": "0",
                "Followers": "0",
                "Products": "0",
            })

    def Signing_in(self, phone, password):
        from connection_status import connect
        if connect():
            from main import number_of_app

            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_of_app.times == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print(default_app.name)
                number_of_app.times += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_of_app.times))
                print(default_app.name)
                number_of_app.times += 1
            users = db.reference("Users")
            sers = db.reference("Users")
            user = users.get()
            ser = sers.order_by_child("city").equal_to("arusha").get()
            print(ser)
            if phone in user.keys():
                password_collector = db.reference("Users").child(phone).child("password")
                if password == password_collector.get():
                    # take name
                    name_collector = db.reference("Users").child(phone).child("name")
                    Upload_image.name = name_collector.get()

                    # take image
                    first_char = Upload_image.name[0]
                    image = db.reference("Categories_url").child("letter_name").child(first_char).child("url")
                    Upload_image.image = image.get()
                    print(Upload_image.image)

                    # take purchase
                    purchase_collector = db.reference("Users").child(phone).child("Purchased")
                    Upload_image.purchased_admin = purchase_collector.get()

                    return True
                else:
                    return False
            else:
                return False

    def Signing_in_admin(self, phone, password):
        from connection_status import connect
        if connect():
            from main import number_of_app
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_of_app.times == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print(default_app.name)
                number_of_app.times += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_of_app.times))
                print(default_app.name)
                number_of_app.times += 1
            admins = db.reference("Admins")
            admin = admins.get()
            if phone in admin.keys():
                print("ok")
                password_collector = db.reference("Admins").child(phone).child("password")
                if password == password_collector.get():

                    # take name
                    name_collector = db.reference("Admins").child(phone).child("name")
                    Upload_image.name_admin = name_collector.get()

                    # take image
                    first_char = Upload_image.name_admin[0]
                    image = db.reference("Categories_url").child("letter_name").child(first_char).child("url")
                    Upload_image.image_admin = image.get()
                    print(Upload_image.image_admin)

                    # take followers
                    follower_collector = db.reference("Admins").child(phone).child("Followers")
                    Upload_image.follower_admin = follower_collector.get()

                    # take purchase
                    purchase_collector = db.reference("Admins").child(phone).child("Purchased")
                    Upload_image.purchased_admin = purchase_collector.get()

                    # take products
                    product_collector = db.reference("Admins").child(phone).child("Products")
                    Upload_image.product_admin = product_collector.get()
                    return True
                else:
                    return False
            else:
                print("not ok")
                return False

    def Product_Commiter(self, identity, name, image_path, max, min, date, month, year, state, time):
        from connection_status import connect
        if connect():
            from main import number_of_app

            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            if number_of_app.times == 0:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                print(default_app.name)
                number_of_app.times += 1
            else:
                default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                             name="default" + str(number_of_app.times))
                print(default_app.name)
                number_of_app.times += 1
            ref = db.reference('Products').child(identity)
            ref.set({
                "name": name,
                "time": time,
                "state": state,
                "year": year,
                "date": date,
                "month": month,
                "image": self.product_image,
                "maximum": max,
                "minimum": min
            })

    def get_img_url(self, cat):
        from connection_status import connect
        if connect():
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                         name=cat + self.pic_name)
            store = db.reference("Categories_url", default_app).child(cat)
            stores = store.get()
            print("ok")
            self.amount = stores.values().__len__()
            for x in stores.values():
                for y in stores.keys():
                    Upload_image.pic_url = x["url"]
                    Upload_image.pic_name = y

    def size_me(cat):
        from connection_status import connect
        if connect():
            content = + 1
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("farmzon-abdcb-c4c57249e43b.json")
            default_app = initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'},
                                         name=cat + str(content))
            store = db.reference("Categories_url", default_app).child(cat)
            stores = store.get()
            big = stores.values().__len__()
            return big

# Upload_image.uploadima(Upload_image())
# Upload_image.put_in_database(Upload_image(), "wewe")
# Upload_image.Signing_in(Upload_image(), "0788204327", "9060")
