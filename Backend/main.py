from flask import Flask
from applications.config import Config
from applications.database import db
from applications.models import *
from flask_restful import Api
from flask_security import Security, hash_password
from applications.user_datastore import user_datastore
from flask_cors import CORS
from celery.schedules import crontab
from celery_worker import create_celery_app 
from celery_tasks import daily_reminder, monthly_report


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    api = Api(app, prefix='/api/iescp2')
    app.security = Security(app, user_datastore)
    celery_app = create_celery_app()


    with app.app_context():
        db.create_all()

        admin_role = app.security.datastore.find_or_create_role(name='admin')
        sponsor_role = app.security.datastore.find_or_create_role(name='sponsor')
        influencer_role = app.security.datastore.find_or_create_role(name='influencer')

        if not app.security.datastore.find_user(email='ritam_admin@gmail.com'):
            app.security.datastore.create_user(username='Ritam_admin',
                                       email='ritam_admin@gmail.com',
                                       password=hash_password('ritam_admin'),
                                       is_approved=True,
                                       roles=[admin_role])
            
        db.session.commit()
    
    return app,api, celery_app 

app, api, celery_app = create_app()
CORS(app, resources={r"/api/*": {"origins": "*"}})
# celery_app = celery_init_app(app)

from applications.user_api import *

api.add_resource(UserRegistration, '/register')
api.add_resource(CheckEmailAPI, '/check-email')
api.add_resource(UserLogin, '/login')
api.add_resource(UpdateUserDetails, '/user/update-profile')
api.add_resource(UserLogout, '/logout')
 
from applications.crud_api import *


# admin api endpoints
api.add_resource(AdminApproveSponsor, '/admin/approve-sponsor/<int:sponsor_id>') #working properly
api.add_resource(PendingApprovals, '/admin/pending-approvals')                   #working properly
api.add_resource(AdminUserManagement, '/admin/user-management')                  #working properly
api.add_resource(AdminStatisticsResource, '/admin/statistics')                  #working properly
api.add_resource(AdminFlagResource, '/admin/flag')                              #working properly    
api.add_resource(FlaggedCampaignsAPI, '/flagged-campaigns')                     #working properly  
api.add_resource(AdminFlaggedUsersAPI, '/admin/flagged-users')                  #working properly     
api.add_resource(AdminResolveFlagResource, '/admin/resolve-flag/<int:flag_id>') #working properly
api.add_resource(AdminDeleteFlaggedResource, '/admin/delete-flagged/<int:flag_id>')#working properly
#api.add_resource(CampaignList, '/campaigns') # 


#sponsor and some common api endpoints

api.add_resource(GetAllInfluencersResource, '/sponsor/influencers')                 #working properly
api.add_resource(SearchInfluencersAPI, '/sponsor/search-influencers')               #done without usig api
api.add_resource(CreateCampaignAPI, '/sponsor/create-campaign')                     #working properly
api.add_resource(ViewCampaignsAPI, '/view-campaign')                                #working properly
# api.add_resource(SponsorDashboardResource, '/sponsor/dashboard')   
api.add_resource(UpdateCampaignAPI, '/sponsor/update-campaign/<int:campaign_id>')   #working properly
api.add_resource(DeleteCampaignAPI, '/sponsor/delete-campaign/<int:campaign_id>')   #working properly
api.add_resource(CreateAdRequestAPI, '/sponsor/create-adrequest')                   #working properly
api.add_resource(ViewAdRequestAPI, '/sponsor/view-adrequest')                       #working properly
api.add_resource(UpdateAdRequestAPI, '/sponsor/update-adrequest/<int:adrequest_id>')#working properly
api.add_resource(DeleteAdRequestAPI, '/sponsor/delete-adrequest/<int:adrequest_id>')#woring properly
api.add_resource(CampaignStatisticsAPI, '/sponsor/campaign-statistics/<int:campaign_id>')#woring properly
api.add_resource(SponsorRespondNegotiationAPI, '/sponsor/respond-negotiation/<int:adrequest_id>')#woring properly

#influencer api endpoints

api.add_resource(PublicCampaignSearchAPI, '/influencer/search-campaigns')           #done without using api
api.add_resource(InfluencerAdRequestsAPI, '/influencer/ad-requests')                #working properly
api.add_resource(InfluencerRespondAdRequestAPI, '/influencer/respond-adrequest/<int:adrequest_id>')  #working properly
api.add_resource(InfluencerCreateAdRequestAPI, '/influencer/create-adrequest/<int:campaign_id>')    #working properly

@celery_app.on_after_finalize.connect
def send_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=18, minute=11),
            daily_reminder,
        )

@celery_app.on_after_finalize.connect
def send_report_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=18, minute=11, day_of_month=3),
            monthly_report,
        )




if __name__ == '__main__':
    app.run(debug=True)
