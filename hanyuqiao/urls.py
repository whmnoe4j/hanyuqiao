from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from hanyuqiao import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

import xadmin
xadmin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^if_introduction_exist/(?P<version>\S+)$', 'hanyuqiao.api.if_introduction_exist'),
    url(r'^newest_version$', 'hanyuqiao.api.newest_version'),
    url(r'^get_user_by_uid_or_create/(?P<uid>\S+)$', 'hanyuqiao.api.get_user_by_uid_or_create'),
    url(r'^get_language_list$', 'hanyuqiao.api.get_language_list'),
    url(r'^set_language$', 'hanyuqiao.api.set_language'),
    url(r'^translate/(?P<messageid>\d+)/(?P<languageid>\d+)$', 'hanyuqiao.api.translate'),
    #url(r'^get_messages/(?P<languageid>\d+)$', 'hanyuqiao.api.get_messages'),
    url(r'^get_messages$', 'hanyuqiao.api.get_messages'),
    url(r'^get_subjects$', 'hanyuqiao.api.get_subjects'),
    url(r'^get_message/(?P<messageid>\d+)$', 'hanyuqiao.api.get_message'),
    url(r'^set_favorite$', 'hanyuqiao.api.set_favorite'),
    url(r'^get_favorites$', 'hanyuqiao.api.get_favorites'),
    url(r'^get_competitions$', 'hanyuqiao.api.get_competitions'),
    url(r'^get_players/(?P<competitionid>\d+)$', 'hanyuqiao.api.get_players'),
    url(r'^search_players$', 'hanyuqiao.api.search_players'),
    url(r'^vote$', 'hanyuqiao.api.vote'),
    url(r'^get_user/(?P<userid>\d+)$', 'hanyuqiao.api.get_user'),
    url(r'^register$', 'hanyuqiao.api.register'),
    url(r'^if_cellphone_exist/(?P<cellphone>\S+)$', 'hanyuqiao.api.if_cellphone_exist'),
    url(r'^login$', 'hanyuqiao.api.login'),
    url(r'^modify_password$', 'hanyuqiao.api.modify_password'),
    url(r'^update_user_info$', 'hanyuqiao.api.update_user_info'),
    url(r'^get_friends_list$', 'hanyuqiao.api.get_friends_list'),
    url(r'^get_notifications$', 'hanyuqiao.api.get_notifications'),
    url(r'^get_notification$', 'hanyuqiao.api.get_notification'),
    url(r'^invite$', 'hanyuqiao.api.invite'),
    url(r'^pass_invite$', 'hanyuqiao.api.pass_invite'),
    url(r'^deny_invite$', 'hanyuqiao.api.deny_invite'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', include(xadmin.site.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
