from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, about, features
from feedback.views import contact, feedback
from members.views import member, psearch, add_member, subscription, profile, prenew, psubscription, exportpdf, expiredmembership
from gym_or_club.views import signup, settings1, success, signin, welcome, logout, renewal, payment, chpassword, chemail, chusername, chaddress, chphonenumber
import mfa
import mfa.TrustedDevice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('About/', about, name='about'),
    path('Features/', features, name='features'),
    path('Contact/', contact, name='contact'),
    path('Feedback/', feedback, name='feedback'),
    path('SignUp/', signup, name='signup'),
    path('LogIn/', signin, name='signin'),
    path('Welcome/', welcome, name='welcome'),
    path('Success/', success, name='success'),
    path('Settings/', settings1, name='settings'),
    path('Payment/', payment, name='payment'),
    path('|->/', logout, name='logout'),
    path('Renew_Membership/', renewal, name='renewal'),
    path('chphonenumber/', chphonenumber, name='chphonenumber'),
    path('chaddress/', chaddress, name='chaddress'),
    path('chusername/', chusername, name='chusername'),
    path('exportpdf/', exportpdf, name='exportpdf'),
    path('psearch/', psearch, name='psearch'),
    path('chpassword/', chpassword, name='chpassword'),
    path('chemail/', chemail, name='chemail'),
    path('Expired_Membership_List/', expiredmembership, name='expiredmembership'),
    path('Member/', member, name='member'),
    path('Add_Member/', add_member, name='add_member'),
    path('Subscription/', subscription, name='subscription'),
    path('Profile/', profile, name='profile'),
    path('Profile/Renew', prenew, name='prenew'),
    path('Profile/Subscription', psubscription, name='psubscription'),
    path('mfa/', include('mfa.urls')),
    path('devices/add/', mfa.TrustedDevice.add,name="mfa_add_new_trusted_device"),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
