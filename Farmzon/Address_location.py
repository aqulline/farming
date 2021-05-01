import datetime
import threading


class Location_Address:
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    latitude = ""

    longitude = ""

    location = ""

    location2 = ""

    # District = input("Enter Wilaya/District")

    # region = input("Enter Region/Mkoa")

    # address = District + "/" + region

    def Generate_address(self, address):
        from connection_status import connect
        if connect:
            self.location = self.geolocator.geocode(address)
            print("yes")
            if self.location != "None":
                Location_Address.latitude = self.location.latitude

                Location_Address.longitude = self.location.longitude

                Location_Address.location2 = self.location

                print(self.longitude, self.latitude, self.location)
            else:
                return self.location
        else:
            print("No internet")
        return self.location


# Location_Address.Generate_address(Location_Address(), "ubungo/dar")
