from django.conf.urls import url 
from . import views 

app_name = 'dashboard'

urlpatterns = [
    url(r'^signup/$', views.signup_view, name="signup"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^create/$', views.post_question, name="create_ques"),
    url(r'^$', views.question_list, name="question_list"),
    url(r'^(?P<id>[\w]+)/$', views.question_detail, name="detail"),
    url(r'^(?P<id>[\w]+)/answer$', views.post_answer, name="post_answer"),
    url('get_questions', views.get_questions),
    url('post_question', views.post_question_api),
]
