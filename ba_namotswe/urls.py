"""edc_pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from edc_base.views import LoginView, LogoutView

from .admin_site import ba_namotswe_admin, ba_namotswe_historical_admin
from edc_metadata.admin import edc_metadata_admin
from edc_registration.admin import edc_registration_admin
from edc_consent.views import HomeView as EdcConsentHomeView
from edc_consent.admin_site import edc_consent_admin
from edc_identifier.admin_site import edc_identifier_admin

from .views import HomeView

urlpatterns = [
    url(r'^dashboard/', include('ba_namotswe_dashboard.urls')),
    url(r'login', LoginView.as_view(), name='login_url'),
    url(r'logout', LogoutView.as_view(pattern_name='login_url'), name='logout_url'),
    url(r'^admin/', ba_namotswe_admin.urls),
    url(r'^admin/', ba_namotswe_historical_admin.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^edc_metadata/', edc_metadata_admin.urls),
    url(r'^edc_registration/', edc_registration_admin.urls),
    url(r'^edc_consent/admin/', edc_consent_admin.urls),
    url(r'^edc_visit_schedule/', include('edc_visit_schedule.urls', namespace='edc-visit-schedule')),
    url(r'^edc_consent/', EdcConsentHomeView.as_view(), name='edc-consent-url'),
    url(r'^edc_identifier/', edc_identifier_admin.urls),
    url(r'^edc/', include('edc_base.urls', namespace='edc-base')),
    url(r'^(?P<subject_identifier>[0-9\-]{14})/$', HomeView.as_view(), name='home_url'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^', HomeView.as_view(), name='home_url'),
]
