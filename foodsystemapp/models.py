from django.db import models


class ResturantLogin(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __repr__(self):
        return f'{self.sno},{self.fullname},{self.username},{self.password}'


class Customerlogin(models.Model):
    sno = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __repr__(self):
        return f'{self.sno},{self.fullname},{self.username},{self.password}'


class OrderFood(models.Model):

    sno = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    dish = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    restname = models.CharField(max_length=140)
    price = models.CharField(max_length=100)
    total = models.CharField(max_length=100)

    def __repr__(self):
        return f'{self.sno},{self.firstname},{self.lastname},{self.phonenumber},{self.dish}{self.quantity},{self.email},{self.address},{self.restname},{self.total}'


class ResturantDetails(models.Model):

    sno = models.AutoField(primary_key=True)
    hotelname = models.CharField(max_length=500)
    phoneno = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    address = models.CharField(max_length=500)

    def __repr__(self):

        return f'{self.sno},{self.hotelname},{self.phoneno},{self.rating},{self.address}'


class Addfooditems(models.Model):

    sno = models.AutoField(primary_key=True)
    hotelname = models.CharField(max_length=500)
    dishname = models.CharField(max_length=500)
    qty = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    def __repr__(self):

        return f'{self.sno},{self.hotelname},{self.dishname},{self.qty},{self.price}'
