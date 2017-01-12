from django.conf.urls import url, include
from rest_framework import routers

from datasets.bommenkaart.urls import bommenkaart


class DocumentedRouter(routers.DefaultRouter):
    def get_api_root_view(self, **kwargs):
        view = super().get_api_root_view(**kwargs)
        cls = view.cls

        class Datapunt(cls):
            pass

        Datapunt.__doc__ = self.__doc__
        return Datapunt.as_view()


router = DocumentedRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^explosieven/', include(bommenkaart.urls)),
]
