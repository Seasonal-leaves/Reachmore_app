# celery_tasks.py

from celery import Celery
from flask import render_template, current_app
from applications.models import User, Campaign
from datetime import datetime, timedelta
from mail_service import send_message  # Assuming send_message is a utility function for sending emails
celery = Celery()

# Define the Celery tasks
@celery.task()
def daily_reminder():
    with current_app.app_context(): 
            recent_login_threshold = datetime.now() - timedelta(days=1)
            
            users = User.query.filter_by(role_id=3).all()
            data1 = []
            for user in users:
                
                if user.last_login is None or user.last_login < recent_login_threshold:
                    user_data = {
                        'name': user.name,
                        'email': user.email,
                    }
                    data1.append(user_data)

            html_content_template = render_template('user_reminder.html', data=data1)
            for user_data in data1:
                personalized_content = render_template('user_reminder.html', data=user_data['name'])
                send_message(to=user_data['email'], subject=f"Reminder ", content_body=personalized_content)


@celery.task()
def monthly_report():
    with current_app.app_context(): 
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            current_month = end_date.strftime('%B %Y')

            sponsors = User.query.filter_by(role_id=2).all()
            data = []
            for sponsor in sponsors:
                campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
                if not campaigns:
                    total_budget = 0
                    campaigns_count = 0
                else:
                    total_budget = sum(campaign.budget for campaign in campaigns)
                    campaigns_count = len(campaigns)

                sponsor_data = {
                    'name': sponsor.name,
                    'email': sponsor.email,
                    'total_budget': total_budget,
                    'campaigns_count': campaigns_count
                }
                data.append(sponsor_data)

            html_content_template = render_template('monthly_report.html', month=current_month, data=data)
            for sponsor_data in data:
                personalized_content = render_template('monthly_report.html', month=current_month, data=[sponsor_data])
                send_message(to=sponsor_data['email'], subject=f"Monthly Progress Report - {current_month}", content_body=personalized_content)
