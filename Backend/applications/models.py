from applications.database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime



class User(db.Model, UserMixin):
    user_id=db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(255),unique = True,nullable = False)
    username = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_approved = db.Column(db.Boolean(),nullable=False,default=False)


    roles = db.relationship('Role', secondary='user_roles', 
                            backref=db.backref('users', lazy=True))


    # sponsor specific fields
    company_name = db.Column(db.String(255),unique=False, nullable=True)
    industry = db.Column(db.String(100),unique=False, nullable=True)
    budget = db.Column(db.Float,unique=False, nullable=True)

    # FInfluencer specific fields
    category = db.Column(db.String(100),unique=False, nullable=True)
    niche = db.Column(db.String(100),unique=False, nullable=True)
    reach = db.Column(db.Integer,unique=False, nullable=True)

    # Relationship with campaigns and ad requests
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)
   # Relationships with AdHistory
    '''sponsored_histories = db.relationship(
        'AdHistory',
        foreign_keys='AdHistory.sponsor_id',
        back_populates='sponsor',  # Reflects the relationship in AdHistory
        lazy=True
    )
    influenced_histories = db.relationship(
        'AdHistory',
        foreign_keys='AdHistory.influencer_id',
        back_populates='influencer',  # Reflects the relationship in AdHistory
        lazy=True
    )'''
    # Below Fields are required for Flask-Security token based authentication
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True)
    active = db.Column(db.Boolean())


    def __repr__(self):
        roles = [role.name for role in self.roles]
        return f"<User {self.username}, Roles: {roles}>"


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),nullable=False)


class Campaign(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)  # "public" or "private"
    goals = db.Column(db.Text, nullable=True)
    
    # Relationships
    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)
    #ad_history = db.relationship('AdHistory', backref='campaign', lazy=True)

    def __repr__(self):
        return f"<Campaign {self.name}, Sponsor ID: {self.sponsor_id}>"


class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    messages = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # "Pending", "Accepted", "Rejected", "Completed"

    def __repr__(self):
        return f"<AdRequest ID: {self.id}, Status: {self.status}>"

class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flagged_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)  # User being flagged
    flagged_campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=True)  # Campaign being flagged
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending') # only 2 cases "Pending"/"Resolved"
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def validate_status(self):
        if self.status not in ['Pending', 'Resolved']:
            raise ValueError("Invalid status. Allowed values are 'Pending' and 'Resolved'.")

'''
class AdHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)  # Summary of the completed ad request
    
    # Relationships with explicit back_populates
    sponsor = db.relationship(
        'User',
        foreign_keys=[sponsor_id],
        back_populates='sponsored_histories'  # Use back_populates for bidirectional relation
    )
    influencer = db.relationship(
        'User',
        foreign_keys=[influencer_id],
        back_populates='influenced_histories'  # Use back_populates for bidirectional relation
    )

    def __repr__(self):
        return f"<AdHistory ID: {self.id}, Completed on: {self.completion_date}>"
'''