DATABASES = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'Equip_Rent_Project',
    'USER': 'root',
    'PASSWORD': '1234',
    'HOST': 'localhost',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
    }
}

EMAIL = {
    'EMAIL_BACKEND' : 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_USE_TLS' : True,
    'EMAIL_PORT' : 587,
    'EMAIL_HOST' : 'smtp.gmail.com',   
    'EMAIL_HOST_USER' : 'vnavna16@sookmyung.ac.kr',                    
    'EMAIL_HOST_PASSWORD' : 'pirogramming14',
    'REDIRECT_PAGE' : 'http://10.58.5.40:3000/signin'
}

