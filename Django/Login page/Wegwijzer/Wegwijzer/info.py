import smtplib

EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wegwijzer.dands@gmail.com'
EMAIL_HOST_PASSWORD = "hvgfhtlsfnipcenu"
EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
