from django.urls import path
from om.controllerOM import om

urlpatterns = [
    # path('', controllerCommon.login, name=''),
    # path('login/', controllerCommon.login, name='login'),
    # path('faq_ug/', controllerGuide.faq_ug, name='faq_ug')
    path('', om , name='om')
]