from django.urls import path

from . import views

app_name = 'RSA'
urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('RSA/', views.inform, name = 'RSA'),
    path('RSA/instructions/', views.instruct, name = 'instructions'),
    path('RSA/encrypt_text/', views.encrypt, name = 'encrypt'),
    path('RSA/encrypt_text/encrypt_data', views.encrypt_data, name = 'encrypt_data'),
    path('RSA/encrypt_file/', views.encrypt_file, name = 'encrypt_file'),
    path('RSA/encrypt_file/encrypt_file_data', views.encrypt_file_data, name = 'encrypt_file_data'),
    path('RSA/your_key_encrypt_text/', views.your_key_encrypt, name = 'your_key_encrypt'),
    path('RSA/your_key_encrypt_data/', views.your_key_encrypt_data, name = 'your_key_encrypt_data'),
    path('RSA/your_key_encrypt_file/', views.your_key_encrypt_file, name = 'your_key_encrypt_file'),
    path('RSA/your_key_encrypt_file_data/', views.your_key_encrypt_file_data, name = 'your_key_encrypt_file_data'),
    path('RSA/download_enc_file', views.download_enc_file, name = 'download_enc_file'),
    path('RSA/decrypt_text/', views.decrypt, name = 'decrypt'),
    path('RSA/decrypt_text/decrypt_data', views.decrypt_data, name = 'decrypt_data'),
    path('RSA/decrypt_file/', views.decrypt_file, name = 'decrypt_file'),
    path('RSA/decrypt_file/decrypt_file_data', views.decrypt_file_data, name = 'decrypt_file_data'),
    path('RSA/download_dec_file', views.download_dec_file, name = 'download_dec_file'),
]