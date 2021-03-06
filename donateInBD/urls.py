from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
import settings




from donation import views as donationview

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'donateInBD.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', donationview.first_page),
                       url(r'^dashboard$', donationview.IndexView.as_view()),
                       url(r'^register$', donationview.register),
                       url(r'^login$', donationview.login_view),
                       url(r'^logout$', donationview.logout_view),

                       url(r'^post_donation',donationview.post_donation_view),
                       url(r'^submit_donation',donationview.submit_donation_view),
                       url(r'^my_donation',donationview.my_donation_view),
                       url(r'^donations$',donationview.donation_view),
                       url(r'^requests$',donationview.request_donation_view),
                       url(r'^users$',donationview.all_users_view),

                       url(r'^post/(?P<pk>\d+)', donationview.post_detail_view),
                       url(r'^message$', donationview.my_messages),


                       url(r'^update$', donationview.update),
                       url(r'^update_profile$', donationview.update),
                       url(r'^my_profile$', donationview.my_profile),
                       url(r'^profile/(?P<username>\w+)$', donationview.profile_detail_view),
                       url(r'^users/(?P<username>\w+)/$', donationview.profile_detail_view),
                       url(r'^add_profile_feedback', donationview.add_profile_feedback),
                       url(r'^profile/message/submit/(?P<receiver>\w+)', donationview.send_message.as_view()),


					   url(r'^report/submit',donationview.submit_report),
					   url(r'^report/show/(?P<report_id>\d+)$',donationview.show_report),

					   url(r'^report/show_report_list/(?P<post_id>\d+)$',donationview.show_report_list),

						
						
                       (r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
                       url(r'.*', donationview.index),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
