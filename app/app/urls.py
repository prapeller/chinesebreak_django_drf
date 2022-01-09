from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from users.views import UserModelViewSet
from structure.views import LangModelViewSet, CourseModelViewSet, TopicModelViewSet, LessonModelViewSet, TaskModelViewSet
from elements.views import WordModelViewSet, CharacterModelViewSet, GrammarModelViewSet

router = DefaultRouter()
router.register('users', UserModelViewSet)
router.register('structure/langs', LangModelViewSet)
router.register('structure/courses', CourseModelViewSet)
router.register('structure/topics', TopicModelViewSet)
router.register('structure/lessons', LessonModelViewSet)
router.register('structure/task', TaskModelViewSet)
router.register('elements/words', WordModelViewSet)
router.register('elements/characters', CharacterModelViewSet)
router.register('elements/grammars', GrammarModelViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/get-token/', obtain_auth_token),
    path('adminpanel/', include('adminpanel.urls')),
]
