from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djsani.dashboard.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='dashboard/success.html'
        ),
        name='admin_success'
    ),
    # ajax communication to paint the panels
    url(
        r'^panels/$',
        'panels', name="dashboard_panels"
    ),
    # home
    url(
        r'^$', 'home', name="dashboard_home"
    ),
    url(
        r'^student/(?P<cid>\d+)/$',
        'student_detail', name="student_detail"
    ),
    # home
    url(
        r'^$', 'home', name="dashboard_home"
    ),
)
