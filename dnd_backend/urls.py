"""dnd_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import UserCharacterView
from api.views import UserRegisterView, UserLoginView, UserLogoutView, UserRecoverPasswordView
from api.views import ReferenceBookView, ReferenceBookClassView, DetailClassView, ReferenceBookRaceView, DetailRaceView, \
CharacterBackgroundView, DetailBackgroundView, CalculateStatsView, InstrumentsView, ReferenceBookAbilitesView,ReferenceBookMasteryView, \
ReferenceBookLanguagesView, ReferenceBookSpellsView, DetailSpellView, RandomCharacterNameView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', UserRegisterView.as_view()),
    path('api/user/login/', UserLoginView.as_view()),
    path('api/user/logout/', UserLogoutView.as_view()),
    path('api/user/recover/', UserRecoverPasswordView.as_view()),
    path('api/reference_book/', ReferenceBookView.as_view()),
    path('api/reference_book/class/', ReferenceBookClassView.as_view()),
    path('api/reference_book/class/<int:class_id>/', DetailClassView.as_view()),
    path('api/reference_book/race/', ReferenceBookRaceView.as_view()),
    path('api/reference_book/race/<int:race_id>/', DetailRaceView.as_view()),
    path('api/reference_book/background/', CharacterBackgroundView.as_view()),
    path('api/reference_book/abilites/', ReferenceBookAbilitesView.as_view()),
    path('api/reference_book/spells/', ReferenceBookSpellsView.as_view()),
    path('api/reference_book/spells/<int:spell_id>/', DetailSpellView.as_view()),
    path('api/reference_book/mastery/', ReferenceBookMasteryView.as_view()),
    path('api/reference_book/languages/', ReferenceBookLanguagesView.as_view()),
    path('api/reference_book/background/<int:background_id>/', DetailBackgroundView.as_view()),
    path('api/instruments/', InstrumentsView.as_view()),
    path('api/calculator/stats/', CalculateStatsView.as_view()),
    path('api/services/namegen/<str:gender>/', RandomCharacterNameView.as_view()),
    path('api/users/<int:user_id>/characters/', UserCharacterView.as_view()),
]
