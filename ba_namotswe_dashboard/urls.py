
"""ba_namotswe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url

from ba_namotswe_dashboard.views import SubjectDashboardView

urlpatterns = [
    url(r'(?P<subject_identifier>[0-9\-]{14})/(?P<appointment_pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/(?P<selected_crf>[\.\w]+)/(?P<toggle_status>flagged|reviewed|)/',
        SubjectDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'(?P<subject_identifier>[0-9\-]{14})/(?P<appointment_pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/',
        SubjectDashboardView.as_view(), name='subject_dashboard_url'),
    url(r'(?P<subject_identifier>[0-9\-]{14})/',
        SubjectDashboardView.as_view(), name='subject_dashboard_url'),
]
