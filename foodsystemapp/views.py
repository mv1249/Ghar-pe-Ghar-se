from django.shortcuts import render
import re
from foodsystemapp.models import ResturantLogin, Customerlogin, OrderFood, ResturantDetails, Addfooditems
from bs4 import BeautifulSoup
import urllib
import urllib.request
import requests
import csv
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# helper function

def fetchdetails(mapper_dict):
    all_tpo = {}
    count = 1
    for user in mapper_dict.objects.all():
        all_tpo[count] = user.__dict__
        count += 1

    all_tpo_user = []
    all_tpo_password = []
    for key, value in all_tpo.items():
        for key1, value1 in value.items():
            if key1 == 'username':
                all_tpo_user.append(value1)

            if key1 == 'password':
                all_tpo_password.append(value1)

    return all_tpo_user, all_tpo_password


# helper for hoteldetails

def hoteldetails(mapper_dict):

    all_tpo = {}
    count = 1
    for user in mapper_dict.objects.all():
        all_tpo[count] = user.__dict__
        count += 1

    all_tpo_user = []
    all_tpo_password = []
    for key, value in all_tpo.items():
        for key1, value1 in value.items():
            if key1 == 'hotelname':
                all_tpo_user.append(value1)

    return all_tpo_user


# <-----------------------------Functions Working on Resturant Data ----------------------->


def innerHTML(element):
    return element.decode_contents(formatter="html")


def get_name(body):
    return body.find('span', {'class': 'jcn'}).a.string


def which_digit(html):
    mappingDict = {'icon-ji': 9,
                   'icon-dc': '+',
                   'icon-fe': '(',
                   'icon-hg': ')',
                   'icon-ba': '-',
                   'icon-lk': 8,
                   'icon-nm': 7,
                   'icon-po': 6,
                   'icon-rq': 5,
                   'icon-ts': 4,
                   'icon-vu': 3,
                   'icon-wx': 2,
                   'icon-yz': 1,
                   'icon-acb': 0,
                   }
    return mappingDict.get(html, '')


def get_phone_number(body):
    i = 0
    phoneNo = "No Number!"
    try:

        for item in body.find('p', {'class': 'contact-info'}):
            i += 1
            if(i == 2):
                phoneNo = ''
                try:
                    for element in item.find_all(class_=True):
                        classes = []
                        classes.extend(element["class"])
                        phoneNo += str((which_digit(classes[1])))
                except:
                    pass
    except:
        pass
    body = body['data-href']
    soup = BeautifulSoup(body, 'html.parser')
    for a in soup.find_all('a', {"id": "whatsapptriggeer"}):
        # print (a)
        phoneNo = str(a['href'][-10:])

    return phoneNo


def get_rating(body):
    rating = 0.0
    text = body.find('span', {'class': 'star_m'})
    if text is not None:
        for item in text:
            rating += float(item['class'][0][1:])/10

    return rating


def get_rating_count(body):
    text = body.find('span', {'class': 'rt_count'}).string

    # Get only digits
    rating_count = ''.join(i for i in text if i.isdigit())
    return rating_count


def get_address(body):
    return body.find('span', {'class': 'mrehover'}).text.strip()


def get_location(body):
    text = body.find('a', {'class': 'rsmap'})
    if text == None:
        return
    text_list = text['onclick'].split(",")

    latitutde = text_list[3].strip().replace("'", "")
    longitude = text_list[4].strip().replace("'", "")

    return latitutde + ", " + longitude


def get_image(body):
    text = body.find('img', {'class': 'altImgcls'})
    return text


def gethotellink(body):
    text = body.find('a')
    return text


def getdetails(city):

    page_number = 1
    service_count = 1

    fields = ['Name', 'Phone', 'Rating', 'Rating Count',
              'Address', 'Location', 'Image', 'Hotel Link']

    totalrecords = []

    try:
        while True:
            # Check if reached end of result
            if page_number > 10:
                break

            url = " https://www.justdial.com/" + \
                str(city)+"/Restaurants/page-%s" % (page_number)

            req = urllib.request.Request(
                url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"})
            page = urllib.request.urlopen(req)

            soup = BeautifulSoup(page.read(), "html.parser")
            services = soup.find_all('li', {'class': 'cntanr'})

            # Iterate through the 10 results in the page
            for service_html in services:

                # Parse HTML to fetch data
                dict_service = {}
                temp = []
                name = get_name(service_html)
                phone = get_phone_number(service_html)
                rating = get_rating(service_html)
                count = get_rating_count(service_html)
                address = get_address(service_html)
                location = get_location(service_html)
                image = get_image(service_html)
                hotellink = gethotellink(service_html)
                if name != None:
                    dict_service['Name'] = name
                    temp.append(name)
                if phone != None:
                    dict_service['Phone'] = phone
                    temp.append(phone)
                if rating != None:
                    dict_service['Rating'] = rating
                    temp.append(rating)
                if count != None:
                    dict_service['Rating Count'] = count
                    temp.append(count)
                if address != None:
                    dict_service['Address'] = address
                    temp.append(address)
                if location != None:
                    dict_service['Address'] = location
                    temp.append(location)
                if image != None:
                    dict_service['Image'] = image
                    temp.append(image)

                if hotellink != None:
                    dict_service['Hotel Link'] = hotellink
                    temp.append(hotellink)

                service_count += 1

            totalrecords.append(temp)

            page_number += 1

        return totalrecords

    except:
        return 0


def getupdatedlist(totalrecords):

    tempdf = pd.DataFrame()
    names = [totalrecords[x][0] for x in range(len(totalrecords))]
    fields = [totalrecords[x][1] for x in range(len(totalrecords))]
    count = [totalrecords[x][2] for x in range(len(totalrecords))]
    address = [totalrecords[x][4] for x in range(len(totalrecords))]
    imagelinks = [totalrecords[x][5] for x in range(len(totalrecords))]
    hotellinks = [totalrecords[x][-1] for x in range(len(totalrecords))]
    tempdf['Hotel Name'] = np.array(names)
    tempdf['Phone No.'] = np.array(fields)
    tempdf['Rating'] = np.array(count)
    tempdf['Address'] = np.array(address)

    # cleaning the image and hotel link url's

    imagelink = []
    hotellink = []
    for link1 in range(len(imagelinks)):
        try:
            imagelink.append(str(imagelinks[link1]).split(
                'data-src=')[1].split('>')[0][:-1])
            hotellink.append(str(hotellinks[link1]).split(
                '\r')[0].split('data-href=')[1].split('>')[0][:-1])
        except:
            pass

    imagelink = [imagelink[i][:imagelink[i].find(
        'src')-1] for i in range(len(imagelink))]
    hotellink = [hotellink[i][:hotellink[i].find(
        'href')-1] for i in range(len(hotellink))]

    tempdf['Image Link'] = np.array(imagelink)
    tempdf['Hotel Link'] = np.array(hotellink)

    dummy = tempdf.drop_duplicates()

    hotelnames = list(dummy['Hotel Name'])
    phoneno = list(dummy['Phone No.'])
    rating = list(dummy['Rating'])
    address = list(dummy['Address'])
    newimagelink = list(dummy['Image Link'])
    newhotellink = list(dummy['Hotel Link'])

    totalrecordsnew = []
    for hotel, phone, rate, add, image, hotlink in zip(hotelnames, phoneno, rating, address, newimagelink, newhotellink):
        totalrecordsnew.append([hotel, phone, rate, add, image, hotlink])

    return totalrecordsnew


# <-------------------------------------End of Resturant Details--------------------------->


def homepage(request, methods=['GET', 'POST']):
    return render(request, 'home.html')

# Resturant Signup


def resturantsignup(request, methods=['GET', 'POST']):

    all_tpo_user, all_tpo_password = fetchdetails(ResturantLogin)

    if request.method == 'POST':
        restname = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        result = re.findall(pattern, password)

        # grabbing the last three characters
        user_last_three = username[-4:]

        if user_last_three == '_RES' and result:

            if username not in all_tpo_user and password not in all_tpo_password:

                instance = ResturantLogin(fullname=restname,
                                          username=username, password=password)

                instance.save()

                return render(request, 'login.html', context={'signed_in': True})

            else:
                return render(request, 'resturantsignup.html', context={'userexists': True})

        else:
            return render(request, 'resturantsignup.html', context={'error': True})

    return render(request, 'resturantsignup.html')


# Customer Signup

def customersignup(request, methods=['GET', 'POST']):

    all_tpo_user, all_tpo_password = fetchdetails(Customerlogin)

    if request.method == 'POST':
        fullname = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$"
        result = re.findall(pattern, password)

        # grabbing the last three characters
        user_last_three = username[-4:]

        if user_last_three == '_CUS' and result:

            if username not in all_tpo_user and password not in all_tpo_password:

                instance = Customerlogin(fullname=fullname,
                                         username=username, password=password)

                instance.save()

                return render(request, 'login.html', context={'signed_in': True})

            else:
                return render(request, 'customersignup.html', context={'userexists': True})

        else:
            return render(request, 'customersignup.html', context={'error': True})

    return render(request, 'customersignup.html')

# Login


def login(request, methods=['GET', 'POST']):

    rest_user, rest_password = fetchdetails(ResturantLogin)

    cust_user, cust_pass = fetchdetails(Customerlogin)

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        print(cust_user, cust_pass)

        if username in rest_user and password in rest_password:
            return render(request, 'resturanthome.html')

        elif username in cust_user and password in cust_pass:
            return render(request, 'customerhome.html')

        else:
            return render(request, 'login.html', context={'exists': True})

    return render(request, 'login.html')


# Customer Homepage

def customerhome(request, methods=['GET', 'POST']):

    allhotelnames = hoteldetails(ResturantDetails)

    try:
        if request.method == 'POST':
            location = request.POST.get('location')

            totalrecords = getdetails(str(location))

            if totalrecords == 0:
                return render(request, 'customerhome.html', context={'displayerror': True})

            else:

                tempdf = getupdatedlist(totalrecords)

                for i in range(len(tempdf)):
                    hotelname = tempdf[i][0]
                    phoneno = tempdf[i][1]
                    ratings = tempdf[i][2]
                    address = tempdf[i][3]

                    if hotelname not in allhotelnames:
                        instance = ResturantDetails(
                            hotelname=hotelname, phoneno=phoneno, rating=ratings, address=address)

                        instance.save()

                return render(request, 'customerhome.html', context={'displayhotels': True, 'detailslist': tempdf})

        #['Hotel Name', 'Phone No.', 'Rating', 'Address', 'Image Link','Hotel Link'],
    except:

        return render(request, 'customerhome.html', context={'displayerror': True})

    return render(request, 'customerhome.html')


# Resturant Homepage

def resturanthome(request, methods=['GET', 'POST']):

    return render(request, 'resturanthome.html')


# Order Food


def orderfood(request, methods=['GET', 'POST']):

    allhotelnames = hoteldetails(ResturantDetails)

    # ['firstname','lastname','phone','dish','qty','email','address']

    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        resturant = request.POST.get('resturant')
        phone = request.POST.get('phone')
        dish = request.POST.get('dish')
        qty = request.POST.get('qty')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if resturant in allhotelnames:

            instance = OrderFood(firstname=firstname, lastname=lastname,
                                 phonenumber=phone, dish=dish, quantity=qty, email=email,
                                 address=address, restname=resturant, price=100, total=100*int(qty))

            instance.save()

            return render(request, 'checkoutdetails.html', context={'minprice': 100, 'dish': dish, 'quantity': qty, 'total': 100*int(qty)})

        else:

            return render(request, 'orderfood.html', context={'nohotel': True})

        return render(request, 'orderfood.html')

    return render(request, 'orderfood.html')


def displayalert(request, methods=['GET', 'POST']):

    if request.method == 'POST':

        payment = request.POST.get('paymentMethod')

        return render(request, 'customerhome.html', context={'paymentdone': True})

    else:
        return render(request, 'checkoutdetails.html', context={'error': True})


# checkoutdetails

def checkoutdetails(request, methods=['GET', 'POST']):

    return render(request, 'checkoutdetails.html')

# customer order details


def custorderdetails(request, methods=['GET', 'POST']):

    completedata = OrderFood.objects.all()

    return render(request, 'customerorderdetails.html', context={'allTodo': completedata})


def fooditemsadded(request, methods=['GET', 'POST']):

    if request.method == 'POST':

        hotelname = request.POST.get('resturant')
        dishname = request.POST.get('dish')
        qty = request.POST.get('qty')
        price = request.POST.get('price')

        instance = Addfooditems(hotelname=hotelname,
                                dishname=dishname, qty=qty, price=price)

        instance.save()

        return render(request, 'resturanthome.html')

    return render(request, 'resturanthome.html')


def viewitems(request, methods=['GET', 'POST']):

    completedata = Addfooditems.objects.all()

    return render(request, 'viewitems.html', context={'allTodo': completedata})


def hotelspecific(request, methods=['GET', 'POST']):

    if request.method == 'POST':

        hotelname = request.POST.get('hotelname')

        completedata = OrderFood.objects.filter(restname=hotelname)

        return render(request, 'hotelspecific.html', context={'allTodo': completedata, 'validhotel': True})

    return render(request, 'hotelspecific.html')
