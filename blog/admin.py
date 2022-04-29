from django.contrib import admin

from blog.models import Account, Transaction, UserPayer, Wallet, Auth_token

# Register your models here.
admin.site.register(UserPayer)  

admin.site.register(Auth_token)

admin.site.register(Wallet)

admin.site.register(Transaction)

admin.site.register(Account)

