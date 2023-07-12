from django.urls import path
from deploy.controllerDeploy import deploy
from sbom import controllerSBOM

urlpatterns = [
    # path('', controllerCommon.login, name=''),
    # path('login/', controllerCommon.login, name='login'),
    # path('faq_ug/', controllerGuide.faq_ug, name='faq_ug')

    path('', deploy , name='deploy')
]