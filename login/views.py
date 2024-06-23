from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import joblib
import ast

import pandas as pd
import numpy as np
from pandas_datareader.data import DataReader
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

nifty_companies = {'Asian Paints':['ASIANPAINT.NS','Asian Paints Ltd is an Indian multinational paint company, headquartered in Mumbai. The company is engaged in the business of manufacturing, selling and distribution of paints, coatings, products related to home décor, bath fittings and providing related services.','1942',' 361.8 billion INR','7,348 Cr',0],
                   'Eicher Motors':['EICHERMOT.NS','Eicher Motors Limited is an Indian multinational automotive company that manufactures motorcycles and commercial vehicles, headquartered in New Delhi. Eicher is the parent company of Royal Enfield, a manufacturer of middleweight motorcycles','1948','165.4 billion INR ','1,070 Cr'],
                   'Hero MotorCrop':['HEROMOTOCO.NS','Hero MotoCorp Limited is an Indian multinational motorcycle and scooter manufacturer headquartered in Delhi. It is one of the worlds largest two-wheeler manufacturer and has a market share of about 46% in the Indian two-wheeler industry. As of 15 May 2024, the market capitalization of the company was ₹101,500 crore','1984','386.4 billion INR','943 Cr'],
                    'ITC':['ITC.NS','ITC Limited is an Indian conglomerate company, headquartered in Kolkata. It has a presence across six business segments, namely FMCG, hotels, agribusiness, information technology, paper products, and packaging. It generates a plurality of its revenue from tobacco products.','1910',' 481.5 billion INR','5,191 Cr'],
                   'Reliance Industries Limited':['RELIANCE.NS','Reliance Industries Limited is an Indian multinational conglomerate headquartered in Mumbai. Its businesses include energy, petrochemicals, natural gas, retail, entertainment, telecommunications, mass media, and textiles.','1957','9.145 trillion INR','21,243 Cr'],
                   'Tata Steel Limited':['TATASTEEL.NS','Tata Steel Limited is an Indian multinational steel-making company, based in Jamshedpur, Jharkhand and headquartered in Mumbai, Maharashtra. It is a part of the Tata Group','1907','2.444 trillion INR','522 Cr'],
                   "Dr Reddy's Laboratories Limited":['DRREDDY.NS','Dr. Reddys Laboratories is an Indian multinational pharmaceutical company based in Hyderabad. The company was founded by Kallam Anji Reddy, who previously worked in the mentor institute Indian Drugs and Pharmaceuticals Limited. Dr. Reddy manufactures and markets a wide range of pharmaceuticals in India and overseas','1984','257.2 billion INR','1,310 Cr'],
                   'Shriram Finance Limited' :['SHRIRAMFIN.NS','Shriram Finance is a leading financial services company in India, offering a wide range of products for individuals and businesses. They are part of the larger Shriram Group, which includes companies in insurance, real estate, and wealth management.','1979','42.91B','2,021 Cr'],
                   'Infosys Limited':['INFY.NS','Infosys Limited is an Indian multinational information technology company that provides business consulting, information technology and outsourcing services. The company was founded in Pune and is headquartered in Bangalore','1981','1.005 trillion INR','7,975 Cr'],
                   'Sun Pharmaceutical Industries Limited':['SUNPHARMA.BO','Sun Pharmaceutical Industries Limited is an Indian multinational pharmaceutical company headquartered in Mumbai, that manufactures and sells pharmaceutical formulations and active pharmaceutical ingredients in more than 100 countries across the globe','1983',' 445.2 billion INR','2,659 Cr'],
                   'Tata Consultancy Services Limited':['TCS.NS','Tata Consultancy Services Limited is an Indian multinational information technology services and consulting company headquartered in Mumbai. It is a part of the Tata Group and operates in 150 locations across 46 countries. In March 2024, it was reported that TCS had more than 601,546 employees worldwide','1968','25.71 billion USD','12,502 Cr'],
                   'Maruti Suzuki India Limited':['MARUTI.NS','Maruti Suzuki India Limited is the Indian subsidiary of Japanese automaker Suzuki Motor Corporation. As of September 2022, the company had a leading market share of 42 percent in the Indian passenger car market','1981',' 1.46 trillion INR','3,952 Cr'],
                   'HCL TECHNOLOGIES':['HCLTECH-BL.NS','HCL Technologies Limited, doing business as HCLTech, is an Indian multinational information technology consulting company headquartered in Noida. Founded by Shiv Nadar, it was spun out in 1991 when HCL entered into the software services business. The company has offices in 52 countries and over 225,944 employees','1991','11.18 billion USD','3,995 Cr'],
                   'Coal India Limited':['COALINDIA.NS','Coal India Limited is an Indian central public sector undertaking under the ownership of the Ministry of Coal, Government of India. It is headquartered at Kolkata. It is the largest government-owned-coal-producer in the world. It is also the ninth largest employer in India with nearly 272,000 employees.','1975','1.503 trillion INR','8,640 Cr'],
                   'LTIMindtree Limited':['LTIM.NS','LTIMindtree Limited is an Indian multinational information technology services and consulting company based in Mumbai. A subsidiary of Larsen & Toubro, the company was incorporated in 1996 and employs more than 81,000 people','1996',' 355.2 billion INR','1,101 Cr'],
                   'HDFC Life Insurance Company Limited':['HDFCLIFE.NS','HDFC Life Insurance Company Limited is a long-term life insurance provider headquartered in Mumbai, offering individual and group insurance services. The company was incorporated on 14 August 2000.','2000',' 711.9 billion INR','412 Cr'],
                   'Bajaj Auto Limited':['BAJAJ-AUTO.NS','Bajaj Auto Limited is an Indian multinational automotive manufacturing company based in Pune. It manufactures motorcycles, scooters and auto rickshaws. Bajaj Auto is a part of the Bajaj Group. It was founded by Jamnalal Bajaj in Rajasthan in the 1940s','1945','463.1 billion INR','2,011 Cr'],
                   'Britannia Industries Limited':['BRITANNIA.NS','Britannia Industries Limited is an Indian multinational food products company, which sells biscuits, breads and dairy products. Founded in 1892, it is one of India oldest existing companies and currently part of the Wadia Group headed by Nusli Wadia. As of 2023, about 80% of its revenues came from biscuit products','1892','163 billion INR','537 Cr'],
                   'Nestlé India Limited':['NESTLEIND.NS','Nestlé India Limited is the Indian subsidiary of Nestlé which is a Swiss multinational company. The company is headquartered in Gurgaon, Haryana. The company products include food, beverages, chocolate, and confectioneries','1959','192.5 billion INR','934 Cr'],
                   'Hindalco Industries Limited':['HINDALCO.NS','Hindalco Industries Limited an Indian aluminium and copper manufacturing company, is a subsidiary of the Aditya Birla Group. Its headquarters are at Mumbai, Maharashtra, India. The company is listed in the Forbes Global 2000 at 661st rank. Its market capitalisation by the end of November 2023 was US$15.6 billion','1958','2.245 trillion INR','2,331 Cr'],
                   'Larsen & Toubro Limited':['LT.NS','Larsen & Toubro Limited, abbreviated as L&T, is an Indian multinational conglomerate, with interests in industrial technology, heavy industry, engineering, construction, manufacturing, power, information technology, military and financial services. It is headquartered in Mumbai, Maharashtra','1946','2.253 trillion INR','5,013 Cr'],
                   'Tata Consumer Products Limited':['TATACONSUM.NS','Tata Consumer Products is an Indian fast-moving consumer goods company and a part of the Tata Group. Its registered office is located in Kolkata while its corporate headquarters is in Mumbai. It is the worlds second-largest manufacturer and distributor of tea and a major producer of coffee','1962','154.5 billion INR','212 Cr'],
                   'Wipro Limited':['WIPRO.NS','Wipro Limited is an Indian multinational corporation that provides information technology, consultant and business process services. It is one of the leading Big Tech companies','1945','897.6 billion INR','2,858 Cr'],
                   'Titan Company Limited':['TITAN.NS','Titan Company Limited is an Indian company that mainly manufactures fashion accessories such as jewellery, watches and eyewear. Part of the Tata Group and started as a joint venture with TIDCO, the company has its corporate headquarters in Electronic City, Bangalore, and registered office in Hosur, Tamil Nadu','1984','516.2 billion INR','771 Cr'],
                   'Bharat Petroleum Corporation Limited':['BPCL.NS','Bharat Petroleum Corporation Limited is an Indian public sector undertaking under the ownership of the Ministry of Petroleum and Natural Gas, Government of India. It operates three refineries in Bina, Kochi and Mumbai','1952','5.092 trillion INR','4,790 Cr'],
                   'Bajaj Finance Limited':['BAJFINANCE.NS','Bajaj Finance Limited is an Indian non-banking financial company headquartered in Pune. It is one of the leading non-banking financial companies of India with a customer base of 83.64 million and holds assets under management worth ₹330,615 crore, as of March 2024','1987','549.8 billion INR','3,825 Cr'],
                   'JSW Steel Limited':['JSWSTEEL.NS','JSW Steel Limited is an Indian multinational steel producer based in Mumbai and is a flagship company of the JSW Group. After the merger of Bhushan Power & Steel, Ispat Steel and Jindal Vijayanagar Steel Limited, JSW Steel became Indias second largest private sector steel company','1982',' 1.67 trillion INR','1,322 Cr'],
                   'ICICI Bank Limited':['ICICIBANK.NS','ICICI Bank Limited is an Indian multinational bank and financial services company headquartered in Mumbai with a registered office in Vadodara','1994','13 billion USD','12,200 Cr'],
                   'Oil and Natural Gas Corporation Limited': ['ONGC.NS','The Oil and Natural Gas Corporation Limited is an Indian central public sector undertaking under the ownership of Ministry of Petroleum and Natural Gas, Government of India. The company is headquartered in Delhi. ONGC was founded on 14 August 1956 by the Government of India.','1956','6.929 trillion INR','11,527 Cr'],
                   'Bharti Airtel Limited':['BHARTIARTL.NS','Bharti Airtel Limited, commonly known as Airtel, is an Indian multinational telecommunications services company based in New Delhi. It operates in 18 countries across South Asia and Africa, as well as the Channel Islands. Currently, Airtel provides 5G, 4G and LTE Advanced services throughout India','1995',' 1.514 trillion INR','2,068 Cr'],
                   "Divi's Laboratories Limited":['DIVISLAB.NS','Divis Laboratories Limited is an Indian multinational pharmaceutical company and producer of active pharmaceutical ingredients and intermediates, headquartered in Hyderabad. The company manufactures and custom synthesizes generic APIs, intermediates','1990','90.73 billion INR','358 Cr'],
                   'SBI Life Insurance Company Limited':['BILIFE.NS','SBI Life Insurance Company Limited is an Indian life insurance company which was started as a joint venture between State Bank of India and French financial institution BNP Paribas Cardif. SBI has a 55.50% stake in the company and BNP Paribas Cardif owns a 0.22% stake','2001',' 806.9 billion INR','811 Cr'],
                   'Bajaj Finance Limited':['BAJFINANCE.NS','Bajaj Finance Limited is an Indian non-banking financial company headquartered in Pune. It is one of the leading non-banking financial companies of India with a customer base of 83.64 million and holds assets under management worth ₹330,615 crore, as of March 2024.','1987',' 549.8 billion INR','3,825 Cr'],
                   'Cipla Limited':['CIPLA.NS','Cipla Limited is an Indian multinational pharmaceutical company headquartered in Mumbai. Cipla primarily focuses on developing medication to treat respiratory disease, cardiovascular disease, arthritis, diabetes, depression, and various other medical conditions','1935','227.5 billion INR','932 Cr'],
                   'Grasim Industries Limited':['GRASIM.NS','Grasim Industries Limited is an Indian manufacturing company based in Mumbai. Since its inception in 1947 as a textile manufacturer, Grasim has diversified into textile raw materials like viscose stapl','1947','1.212 trillion INR','2,722 Cr'],
                   'Hindustan Unilever Limited':['HINDUNILVR.NS','Hindustan Unilever Limited is a British-owned Indian final good company headquartered in Mumbai. It is a subsidiary of the British company Unilever. Its products include foods, beverages, cleaning agents, personal care products, water purifiers and other fast-moving consumer goods.','1933','627.1 billion INR','2,561 Cr'],
                   'MAHINDRA &MAHINDRA':['M&M-BL.NS','Mahindra & Mahindra is an automobile manufacturing company headquartered in Mumbai, Maharashtra. It was established in 1945 as Mahindra & Mohammed and later renamed Mahindra & Mahindra. Part of the Mahindra Group, M&M is one of the largest vehicle manufacturers by production in India.','1945','1.225 trillion INR','3,125 Cr'],
                   'Tata Motors Limited':['TATAMOTORS.NS','Tata Motors Limited is an Indian multinational automotive company, headquartered in Mumbai and part of the Tata Group. The company produces cars, trucks, vans, and busses. Subsidiaries include British Jaguar Land Rover and South Korean Tata Daewoo','1945','4.439 trillion INR','17,529 Cr'],
                   'Apollo Hospitals Enterprise Limited':['APOLLOHOSP.NS','Apollo Hospitals Enterprise Limited is an Indian multinational healthcare group headquartered in Chennai. It is the largest for-profit private hospital network in India, with a network of 71 owned and managed hospitals','1982',' 166.1 billion INR','254 Cr'],
                   'State Bank of India':['SBIN.NS','State Bank of India is an Indian multinational public sector bank and financial services statutory body headquartered in Mumbai, Maharashtra','1955','918.79B','69,543 Cr'],
                   'Kotak Mahindra Bank Limited':['KOTAKBANK.NS','Kotak Mahindra Bank Limited is an Indian banking and financial services company headquartered in Mumbai. It offers banking products and financial services for corporate and retail customers in the areas of personal finance, investment banking, life insurance, and wealth management','1985','942.7 billion INR','5,337 Cr'],
                   'Adani_Enterprise':['ADANIENT.NS','Adani Enterprises Limited is an Indian multinational publicly-listed holding company and a part of Adani Group. It is headquartered in Ahmedabad and primarily involved in mining and trading of coal and iron ore','1993','291.8B','352 Cr'],
                   'HDFC Bank Limited':['HDFCBANK.NS','HDFC Bank Limited is an Indian banking and financial services company headquartered in Mumbai. It is Indias largest private sector bank by assets and the worlds tenth-largest bank by market capitalization as of May 2024.','1994','668.89B','18,013 Cr'],
                   'Power Grid Corporation of India Limited':['POWERGRID.NS','Power Grid Corporation of India Limited is an Indian central public sector undertaking under the ownership of the Ministry of Power, Government of India. It is engaged mainly in transmission of bulk power across different states of India. It is headquartered in Gurugram.','1989',' 466 billion INR ','4,166 Cr'],
                   'Axis Bank Limited':['AXISBANK.NS','Axis Bank Limited, formerly known as UTI Bank, is an Indian multinational banking and financial services company headquartered in Mumbai, Maharashtra. It is Indias third largest private sector bank by assets and fourth largest by market capitalisation','1993','1.38 trillion INR','7,630 Cr'],
                   'NTPC Limited':['NTPC.NS','NTPC Limited is a titan in the Indian energy sector. Established in 1975, its not just Indias largest power company, but a dominant player across the entire electricity value chain.','1975','428.2B','5,209 Cr'],
                   'Tech Mahindra Limited':['TECHM.NS','Tech Mahindra is an Indian multinational information technology services and consulting company. Part of the Mahindra Group, the company is headquartered in Pune and has its registered office in Mumbai. Tech Mahindra has over 146,000 employees across 90 countries','1986',' 529.1 billion INR','664 Cr'],
                   'Adani Ports and Special Economic Zone Limited':['ADANIPORTS.NS','Adani Ports and Special Economic Zone Limited is an Indian multinational port operator and logistics company, based in Ahmedabad, India.','1998','	68.96B','2,015 Cr'],
                   'UltraTech Cement Limited':['ULTRACEMCO.NS','UltraTech Cement Limited is an Indian multinational cement company based in Mumbai. It is the largest manufacturer of grey cement, ready-mix concrete and white cement in India and 5th largest around','1983','715.2 billion INR','2,259 Cr']
                   }

def risk(volume, mean, std, pred_price, yes_price):
    average_volume = 6778689.438232469
    average_std = 31463.130901638862
    #average_mean = 60963.85847204988
    reason = []
    score = 0
    if pred_price > yes_price:
        score += 2
    else:
        score -=2
    if volume < average_volume:
        reason.append('Low Volatility of Stocks Traded')
        score -=1
    else :
        reason.append('High Volatility of Stocks Traded')
    if mean>yes_price :
        reason.append('Price greater than the mean price')
        score -=1
    else:
        reason.append('Price lower than the mean price')
        score += 1
    if std > average_std :
       reason.append('High Variable stock price')
       score -= 1
    else :
        reason.append('Low variable stock price')
        score += 1
    if score > 0 :
        reason = ['Buy'] + reason
    elif score < 0:
        reason = ['Sell'] + reason
    else:
        reason = ['Hold'] + reason
    return reason

def stock_price_predictor(tckr_symbol):
    df = pdr.get_data_yahoo(tckr_symbol,start = '2012-01-01' ,end=datetime.now())
    data = df.filter(['Close'])
    dataset = data.values
    training_data_len = int(np.ceil( len(dataset) * .95 ))
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    train_data = scaled_data[0:int(training_data_len), :]

    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    test_data = scaled_data[training_data_len - 60: , :]
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])

    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    avg_error = np.mean(predictions-y_test)
    new_pred_data = np.array([scaled_data[-60:]])

    new_pred_data = np.reshape(new_pred_data,(new_pred_data.shape[0],new_pred_data.shape[1],1))
    x = model.predict(new_pred_data)
    final_price = scaler.inverse_transform(x)-avg_error
    volume_mean = df['Volume'].mean()
    price_mean = df['Close'].mean()
    price_std = df['Close'].std()
    buy_or_sell = risk(volume_mean,price_mean,price_std,final_price,df['Close'][-1])
    current_price = df['Close'][-1]
    
    return final_price,buy_or_sell,current_price




# Create your views here.
# def home(request):
#     return render(request,"login/log_m.html")

def log(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            #return redirect('dashboard')
            return render(request, "login/dashboard.html",{}) 
        else:
            # Add a message to inform the user about invalid credentials
            #return redirect('log_m.html')
            return render(request, "login/log_error.html",{})
    return render(request, "login/log_m.html")

def sign_m(request):
    if request.method=="POST":
        #username=request.POST.get('username')
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']

        myuser=User.objects.create_user(username, email , pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()

        messages.success(request, "Your account has been successfully created")
        return redirect('log_m')



    return render(request,"login/sign_m.html")

def signout(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    if request.user.is_authenticated:
        request.session['test'] = 'Session is working'
        test_value = request.session.get('test')
        return render(request, "login/dashboard.html", {'test_value': test_value})
    else:
        return redirect('log_m')
    #return render(request,"login/dashboard.html")

def about(request):
    if request.user.is_authenticated:
        request.session['test'] = 'Session is working'
        test_value = request.session.get('test')
        return render(request, "login/about.html", {'test_value': test_value})
    else:
        return redirect('log_m')
    #return render(request,"login/about.html")

def contact(request):
    if request.user.is_authenticated:
        request.session['test'] = 'Session is working'
        test_value = request.session.get('test')
        return render(request, "login/contact.html", {'test_value': test_value})
    else:
        return redirect('log_m')
    #return render(request,"login/contact.html")

def User_Profile(request):
    if request.user.is_authenticated:
        request.session['test'] = 'Session is working'
        test_value = request.session.get('test')
        current_user=request.user
        username=current_user.username
        fname=current_user.first_name
        lname=current_user.last_name
        email=current_user.email
        return render(request,"login/User_Profile.html",{'username':username,'fname':fname,'lname':lname,'email':email})
    else:
        return redirect('log_m')
    # current_user=request.user
    # username=current_user.username
    # fname=current_user.first_name
    # lname=current_user.last_name
    # email=current_user.email
    # return render(request,"login/User_Profile.html",{'username':username,'fname':fname,'lname':lname,'email':email})


def search(request):
    if request.user.is_authenticated:
        request.session['test'] = 'Session is working'
        test_value = request.session.get('test')
        if request.method=="POST":
            global c_name
            c_name=request.POST['c_name']
            #return render(request,"login/model.html",{'c_name':c_name})
            return redirect('model')
        return render(request,"login/search.html")
    else:
        return redirect('log_m')
    # if request.method=="POST":
    #     global c_name
    #     c_name=request.POST['c_name']
    #     #return render(request,"login/model.html",{'c_name':c_name})
    #     return redirect('model')
    # return render(request,"login/search.html")

from cronjob import nifty_companies

def model(request):
    #cls=joblib.load('model_final.sav')
    #cls.predict()
    with open('C:/Users/Kevin Jacob/Desktop/Project/data.txt','r',encoding='utf-8') as f: 
        data = f.read() 
    js = ast.literal_eval(data) 
    ls=js[c_name]
    return render(request,"login/model.html",{'ans':ls[5],'bs1':ls[7],'bs2':ls[8],'bs3':ls[9],'c_name':c_name,'cp':ls[6],'desc':ls[1],'datefounded':ls[2],'rev':ls[3],'profit':ls[4]})

