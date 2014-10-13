from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from hanyuqiao import settings
from django.contrib import admin
admin.autodiscover()
from rest_framework.urlpatterns import format_suffix_patterns
from hanyuqiao import api


urlpatterns = patterns('',
    # Examples:
    url(r'^if_introduction_exist/(?P<version>\S+)$', 'hanyuqiao.api.if_introduction_exist'),
    url(r'^newest_version$', 'hanyuqiao.api.newest_version'),
    url(r'^reg$', api.Reg.as_view()),
    url(r'^login$', api.Login.as_view()),
    url(r'^get_language_list$', 'hanyuqiao.api.get_language_list'),
    url(r'^set_language$', 'hanyuqiao.api.set_language'),
    url(r'^translate/(?P<messageid>\d+)/(?P<languageid>\d+)$', 'hanyuqiao.api.translate'),
    #url(r'^get_messages/(?P<languageid>\d+)$', 'hanyuqiao.api.get_messages'),
    url(r'^get_messages$', api.GetMessages.as_view()),
    url(r'^get_subjects$', 'hanyuqiao.api.get_subjects'),
    url(r'^get_message/(?P<messageid>\d+)$', 'hanyuqiao.api.get_message'),
    url(r'^set_favorite$', 'hanyuqiao.api.set_favorite'),
    url(r'^get_favorites$', 'hanyuqiao.api.get_favorites'),
    url(r'^get_competitionSubjects$', 'hanyuqiao.api.get_competitionSubjects'),
    url(r'^get_competitions$', 'hanyuqiao.api.get_competitions'),
    url(r'^get_players/(?P<cpk>\d+)/(?P<apk>\d+)/(?P<page>\d+)$', api.GetPlayers.as_view()),
    url(r'^search_players$', 'hanyuqiao.api.search_players'),
    url(r'^vote$', api.Vote.as_view()),
    url(r'^get_user/(?P<userid>\d+)$', 'hanyuqiao.api.get_user'),
    
    url(r'^if_cellphones_exist$', 'hanyuqiao.api.if_cellphones_exist'),
    
    url(r'^modify_password$', 'hanyuqiao.api.modify_password'),
    url(r'^update_user_info$', 'hanyuqiao.api.update_user_info'),
    url(r'^get_friends_list$', 'hanyuqiao.api.get_friends_list'),
    url(r'^get_notifications$', 'hanyuqiao.api.get_notifications'),
    url(r'^get_notification$', 'hanyuqiao.api.get_notification'),
    url(r'^invite$', 'hanyuqiao.api.invite'),
    url(r'^pass_invite$', 'hanyuqiao.api.pass_invite'),
    url(r'^deny_invite$', 'hanyuqiao.api.deny_invite'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
