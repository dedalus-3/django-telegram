from django.urls import path
from TgAdmin import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('chats/', views.ChatView.as_view(), name='chats'),
    path('chat/<int:pk>/delete/', views.ChatDeleteView.as_view(), name='chat_delete'),
    path('chat/<int:pk>/', views.ChatUpdateView.as_view(), name='chat_edit'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout', views.LogoutThenLoginView.as_view(), name='logout'),
    path('users/inaction', views.InactionView.as_view(), name='inaction_users'),
    path('users/agree/', views.ClickYesView.as_view(), name='click_yes_users'),
    path('users/disagree/', views.ClickNoView.as_view(), name='click_no_users'),
    path('users/all_agree/', views.ClickYesTpView.as_view(), name='click_yes_tp_users'),
    path('users/anonymous', views.IsVneView.as_view(), name='anonymous_users'),
    path('update_text/', views.UpdateText.as_view(), name='text_create'),
    path('update_btn_yes/', views.UpdateBtnYes.as_view(), name='btn1_create'),
    path('update_btn_no/', views.UpdateBtnNo.as_view(), name='btn2_create'),
    path('update_mailing/', views.UpdateMailingView.as_view(), name='mailing'),
    path('update_faq/', views.UpdateFaq.as_view(), name='edit_faq'),
    path('search/', views.SearchResultView.as_view(), name='search_result'),
]
