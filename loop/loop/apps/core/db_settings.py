import dbsettings

from django.conf import settings


class GoogleGraphCorporate(dbsettings.Group):
    organization_name = dbsettings.StringValue('Organization Name.',
                                               default=settings.GOOGLE_ORG_NAME)
    sales_phone_number = dbsettings.StringValue('Sales Phone Number.',
                                                default=settings.GOOGLE_ORG_PHONE,
                                                required=False)
    logo = dbsettings.StringValue('Logo URL.',
                                  default=settings.GOOGLE_ORG_LOGO,
                                  required=False)

class GoogleGraphSocial(dbsettings.Group):
    twitter_url = dbsettings.StringValue('Twitter profile URL.',
                                         default=settings.GOOGLE_ORG_TWITTER,
                                         required=False)
    googlep_url = dbsettings.StringValue('Google+ profile URL.',
                                         default=settings.GOOGLE_ORG_GOOGLEP,
                                         required=False)
    facebook_url = dbsettings.StringValue('Facebook profile URL.',
                                          default=settings.GOOGLE_ORG_FACEBOOK,
                                          required=False)
    instagram_url = dbsettings.StringValue('Instagram profile URL.',
                                           default=settings.GOOGLE_ORG_INSTAGRAM,
                                           required=False)
    linkedin_url = dbsettings.StringValue('LinkedIn profile URL.',
                                          default=settings.GOOGLE_ORG_LINKEDIN,
                                          required=False)
    pinterest_url = dbsettings.StringValue('Pinterest profile URL.',
                                          default=settings.GOOGLE_ORG_PINTEREST,
                                          required=False)
    tumblr_url = dbsettings.StringValue('Tumblr profile URL.',
                                          default=settings.GOOGLE_ORG_TUMBLR,
                                          required=False)
