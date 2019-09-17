from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'sitereview'
urlpatterns = [
    path('', views.index, name='index'),
    path('au_revoir', views.au_revoir, name='au_revoir'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    path('website_alert/<int:website_alert_id>/',views.display_website_alert, name='display_website_alert'),
    path('list_website_alert/',views.list_website_alert, name='list_website_alert'),
    path('list_website_alert/<int:page>/',views.list_website_alert, name='list_website_alert'),
    path('create_website_alert/',views.create_website_alert, name='create_website_alert'),
    path('validate_list_website_alert/',views.validate_list_website_alert, name='validate_list_website_alert'),
    path('validate_list_website_alert/<int:page>/',views.validate_list_website_alert, name='validate_list_website_alert'),
    path('list_verified_website_alert/',views.list_verified_website_alert, name='list_verified_website_alert'),
    path('website_exists/<path:url_b64>',views.website_exists, name='website_exists'),
    path('already_voted/', TemplateView.as_view(template_name="sitereview/already_voted.html"),name='already_voted' ),
]

