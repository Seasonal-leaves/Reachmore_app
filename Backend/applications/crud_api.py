from flask_restful import Resource, reqparse
from flask import jsonify, request, make_response
from applications.database import db
from sqlalchemy.orm import aliased
from applications.models import *
from flask_security import auth_token_required, roles_accepted, roles_required, current_user
from datetime import datetime


'admin api'

class AdminApproveSponsor(Resource):
    @auth_token_required
    @roles_required('admin')
    def put(self, sponsor_id):
        """Approve a sponsor by setting is_approved to True"""
        user = User.query.get(sponsor_id)
        if not user:
            return make_response(jsonify({'message': 'Sponsor not found'}), 404)

        # Ensure the user is a sponsor
        if 'sponsor' not in [role.name for role in user.roles]:
            return make_response(jsonify({'message': 'User is not a sponsor'}), 400)

        # Approve the sponsor
        user.is_approved = True
        db.session.commit()

        return make_response(jsonify({'message': 'Sponsor approved successfully'}), 200)
    
    def delete(self, sponsor_id):
        
        sponsor = User.query.get(sponsor_id)
        if not sponsor:
            return {"message": f"User with ID {sponsor_id} not found"}, 404
        
        # Reject (delete) the sponsor
        db.session.delete(sponsor)
        db.session.commit()
        return {"message": f"Sponsor {sponsor.username} rejected and deleted"}, 200

'''
from flask_security import RoleMixin
class PendingApprovals(Resource):
    def get(self):
        
        pending_sponsors = (
            User.query.join(User.roles)  # Join with roles table
            .filter(Role.name == "sponsor")  # Filter for sponsors
            .filter(User.is_approved == False)  # Filter for pending approval
            .all()
        )

        response = [
            {
                "user_id": sponsor.user_id,
                "username": sponsor.username,
                "email": sponsor.email,
                "company_name": sponsor.company_name,
                "industry": sponsor.industry,
                "budget": sponsor.budget,
            }
            for sponsor in pending_sponsors
        ]
        return {"pending_sponsors": response}, 200'''


class PendingApprovals(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch all users with the role 'sponsor' and `is_approved` is False
        all_sponsors = Role.query.filter_by(name="sponsor").first()
        
        if not all_sponsors:
            return {"message": "Sponsor role not found"}, 404

        pending_sponsors = (
            User.query.filter(
                User.roles.contains(all_sponsors),
                User.is_approved == False
            ).all()
        )
        if not pending_sponsors:
            return {"message": "No pending approvals for sponsors"}, 404
        response = [
            {
                "user_id": sponsor.user_id,
                "username": sponsor.username,
                "email": sponsor.email,
                "company_name": sponsor.company_name,
                "industry": sponsor.industry,
                "budget": sponsor.budget,
            }
            for sponsor in pending_sponsors
        ]
        return {"pending_sponsors": response}, 200

class AdminUserManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        try:
            # Initialize user groups
            users_by_role = {
                'influencers': [],
                'sponsors': []
            }

            # Fetch flagged user IDs
            flagged_user_ids = db.session.query(Flag.flagged_user_id).filter(
                Flag.status == 'Pending',
                Flag.flagged_user_id.isnot(None)
            ).subquery()

            # Fetch all users excluding flagged users
            all_users = User.query.filter(User.user_id.notin_(flagged_user_ids)).all()
            
            for user in all_users:
                role_names = [role.name for role in user.roles]

                # Group influencers
                if "influencer" in role_names:
                    users_by_role['influencers'].append({
                        'id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                        'niche': user.niche,
                        'category': user.category,
                        'reach': user.reach
                    })

                # Group sponsors (pending approval and approved)
                if "sponsor" in role_names:
                    sponsor_data = {
                        'id': user.user_id,
                        'username': user.username,
                        'email': user.email,
                        'company_name': user.company_name,
                        'industry': user.industry,
                        'budget': user.budget,
                        'is_approved': user.is_approved
                    }
                    if user.is_approved:
                        users_by_role['sponsors'].append(sponsor_data)

            response = {
                'message': 'User management data retrieved successfully',
                'users_by_role': users_by_role
            }
            return make_response(jsonify(response), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)


class AdminStatisticsResource(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        try:
            # Total users grouped by roles
            total_sponsors = User.query.filter(User.company_name.isnot(None)).count()
            total_influencers = User.query.filter(User.category.isnot(None)).count()

            # Campaign statistics
            total_campaigns = Campaign.query.count()
            public_campaigns = Campaign.query.filter_by(visibility='public').count()
            private_campaigns = Campaign.query.filter_by(visibility='private').count()

            # Ad request statistics
            ad_requests_status = db.session.query(
                AdRequest.status,
                db.func.count(AdRequest.id)
            ).group_by(AdRequest.status).all()

           # Flagged entities - only "Pending" status
            total_flagged_users = Flag.query.filter(
                Flag.flagged_user_id.isnot(None),
                Flag.status == 'Pending'
            ).count()

            total_flagged_campaigns = Flag.query.filter(
                Flag.flagged_campaign_id.isnot(None),
                Flag.status == 'Pending'
            ).count()
            # Preparing statistics response
            statistics = {
                'total_users': {
                    'sponsors': total_sponsors,
                    'influencers': total_influencers
                },
                'total_campaigns': total_campaigns,
                'campaign_visibility': {
                    'public': public_campaigns,
                    'private': private_campaigns
                },
                'ad_requests_status': {
                    status: count for status, count in ad_requests_status
                },
                'flagged_entities': {
                    'users': total_flagged_users,
                    'campaigns': total_flagged_campaigns
                }
            }

            return make_response(jsonify({
                'message': 'Statistics retrieved successfully',
                'data': statistics
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)



'''
 class AdminCampaignManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        """Retrieve all campaigns"""
        campaigns = Campaign.query.all()
        return jsonify([
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'sponsor_id': campaign.sponsor_id,
                'budget': campaign.budget,
                'visibility': campaign.visibility
            } for campaign in campaigns
        ])

    @auth_required("token")
    def delete(self, campaign_id):
        """Delete a flagged campaign"""
        campaign = Campaign.query.get(campaign_id)
        if not campaign:
            return make_response(jsonify({'message': 'Campaign not found'}), 404)

        db.session.delete(campaign)
        db.session.commit()
        return make_response(jsonify({'message': 'Campaign deleted successfully'}), 200)

  
  
        '''

'''
class AdminAdHistory(Resource):
    @auth_required("token")
    def get(self):
        """Retrieve all completed ad histories"""
        histories = AdHistory.query.all()
        return jsonify([
            {
                'id': history.id,
                'ad_request_id': history.ad_request_id,
                'campaign_id': history.campaign_id,
                'sponsor_id': history.sponsor_id,
                'influencer_id': history.influencer_id,
                'completion_date': history.completion_date,
                'details': history.details
            } for history in histories
        ])  '''

class AdminFlagResource(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self):
        flag_data = request.get_json()
        flagged_user_id = flag_data.get('flagged_user_id')
        flagged_campaign_id = flag_data.get('flagged_campaign_id')
        reason = flag_data.get('reason')

        # Validation checks
        if not reason:
            return make_response(jsonify({'message': 'Reason for flagging is required'}), 400)

        if len(reason) > 255:
            return make_response(jsonify({'message': 'Reason is too long. Maximum 255 characters allowed'}), 400)

        if not flagged_user_id and not flagged_campaign_id:
            return make_response(jsonify({'message': 'Either flagged_user_id or flagged_campaign_id is required'}), 400)

        if flagged_user_id and flagged_campaign_id:
            return make_response(jsonify({'message': 'Only one of flagged_user_id or flagged_campaign_id can be set'}), 400)

        try:
            # Check for flagged user or campaign existence
            if flagged_user_id:
                user = User.query.get(flagged_user_id)
                if not user:
                    return make_response(jsonify({'message': 'User not found'}), 404)
                existing_flag = Flag.query.filter_by(flagged_user_id=flagged_user_id, status='Pending').first()
                if existing_flag:
                    return make_response(jsonify({'message': 'User is already flagged with a pending status'}), 400)

            if flagged_campaign_id:
                campaign = Campaign.query.get(flagged_campaign_id)
                if not campaign:
                    return make_response(jsonify({'message': 'Campaign not found'}), 404)
                existing_flag = Flag.query.filter_by(flagged_campaign_id=flagged_campaign_id, status='Pending').first()
                if existing_flag:
                    return make_response(jsonify({'message': 'Campaign is already flagged with a pending status'}), 400)

            # Create a flag entry
            flag = Flag(
                flagged_user_id=flagged_user_id,
                flagged_campaign_id=flagged_campaign_id,
                reason=reason,
                status='Pending'
            )
            db.session.add(flag)
            db.session.commit()

            # Return the full flag data
            return make_response(jsonify({
                'message': 'Entity successfully flagged',
                'flag': {
                    'id': flag.id,
                    'flagged_user_id': flag.flagged_user_id,
                    'flagged_campaign_id': flag.flagged_campaign_id,
                    'reason': flag.reason,
                    'status': flag.status,
                    'timestamp': flag.timestamp
                }
            }), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

class FlaggedCampaignsAPI(Resource):
    @auth_token_required
    def get(self):
        try:
            # Get the role of the logged-in user
            role = [role.name for role in current_user.roles][0]

            # Base query to fetch flagged campaigns with their associated flags
            base_query = db.session.query(
                Campaign,
                Flag.reason,
                Flag.id.label('flag_id')
            ).join(Flag, Flag.flagged_campaign_id == Campaign.id).filter(Flag.status == 'Pending')

            # Filter by role
            if role == 'sponsor':
                flagged_campaigns = base_query.filter(
                    Campaign.sponsor_id == current_user.user_id
                ).all()
            elif role == 'admin':
                flagged_campaigns = base_query.all()
            else:
                return make_response(jsonify({'message': 'Unauthorized access'}), 403)

            # Format flagged campaign data for response
            flagged_campaigns_data = [
                {
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date,
                    'end_date': campaign.end_date,
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'reason': reason,
                    'flag_id': flag_id
                }
                for campaign, reason, flag_id in flagged_campaigns
            ]

            return make_response(jsonify({'flagged_campaigns': flagged_campaigns_data}), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)



class AdminFlaggedUsersAPI(Resource):
    @auth_token_required
    @roles_required('admin')  # Restrict access to admins only
    def get(self):
        try:
            # Fetch all flags related to users with status "Pending"
            flagged_users = Flag.query.filter(
                Flag.flagged_user_id.isnot(None),
                Flag.status == 'Pending'
            ).all()

            # Format flagged user data
            flagged_users_data = [
                {
                    'flag_id': flag.id,
                    'user_id': flag.flagged_user_id,
                    'username': User.query.get(flag.flagged_user_id).username,
                    'reason': flag.reason,
                    'status': flag.status,
                    'timestamp': flag.timestamp
                }
                for flag in flagged_users
            ]

            return make_response(jsonify({
                'message': 'Flagged users retrieved successfully',
                'flagged_users': flagged_users_data
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)



class AdminResolveFlagResource(Resource):
    @auth_token_required
    @roles_required('admin')
    def put(self, flag_id):
        try:
            # Retrieve the flag
            flag = Flag.query.get(flag_id)
            if not flag:
                return make_response(jsonify({'message': 'Flag not found'}), 404)

            # Update status to Resolved
            flag.status = 'Resolved'
            db.session.commit()

            return make_response(jsonify({'message': f'Flag (ID: {flag_id}) resolved successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

import traceback

class AdminDeleteFlaggedResource(Resource):
    @auth_token_required
    @roles_required('admin')
    def delete(self, flag_id):
        try:
            # Retrieve the flag entry
            flag = Flag.query.get(flag_id)
            if not flag:
                return make_response(jsonify({'message': 'Flag not found'}), 404)

            # Ensure the flag status is "Pending"
            if flag.status != 'Pending':
                return make_response(jsonify({'message': 'Only flags with status "Pending" can be deleted'}), 403)

            # Check if the flagged entity is a user
            if flag.flagged_user_id:
                user = User.query.get(flag.flagged_user_id)
                if not user:
                    return make_response(jsonify({'message': 'Flagged user not found'}), 404)
                # Delete associated AdRequests
                AdRequest.query.filter_by(influencer_id=user.user_id).delete() 
                db.session.delete(user)

            # Check if the flagged entity is a campaign
            if flag.flagged_campaign_id:
                campaign = Campaign.query.get(flag.flagged_campaign_id)
                if not campaign:
                    return make_response(jsonify({'message': 'Flagged campaign not found'}), 404)
                # Delete associated AdRequests
                AdRequest.query.filter_by(campaign_id=campaign.id).delete()
                db.session.delete(campaign)

            # Delete the flag entry
            db.session.delete(flag)
            db.session.commit()

            return make_response(jsonify({'message': f'Flagged entity (Flag ID: {flag_id}) deleted successfully'}), 200)
        except Exception as e:
                    # Log the error for debugging
                    print(f"Error: {str(e)}")
                    print(f"Stacktrace: {traceback.format_exc()}")
                    db.session.rollback()
                    return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)




# the below api is blocked as influencers also can see all the campaigns whether made public or not

'''
class CampaignList(Resource):
    @auth_token_required
    def get(self):
        user_roles = [role.name for role in current_user.roles]
        # Admin and Influencers see all campaigns
        if 'admin' in user_roles or 'influencer' in user_roles:
            campaigns = Campaign.query.all()

        # Sponsors see only their own campaigns
        elif 'sponsor' in user_roles:
            campaigns = Campaign.query.filter_by(sponsor_id=current_user.id).all()

        else:
            return make_response(jsonify({'message': 'Role not authorized to view campaigns'}), 403)

        # Format response
        campaign_list = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d') if campaign.end_date else None,
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
                'sponsor_id': campaign.sponsor_id
            } for campaign in campaigns
        ]

        return make_response(jsonify({'campaigns': campaign_list}), 200)'''



' Sponsor api'
class GetAllInfluencersResource(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def get(self):
        try:
             # Check if the sponsor is flagged
            is_flagged_sponsor = db.session.query(Flag).filter(
                Flag.flagged_user_id == current_user.user_id,
                Flag.status == 'Pending'
            ).first()

            if is_flagged_sponsor:
                # Return the reason for flagging
                return make_response(jsonify({
                    'message': f"Access denied. You are flagged and cannot view influencers. Reason: {is_flagged_sponsor.reason}"
                }), 403)
            # Fetch the influencer role
            influencer_role = Role.query.filter_by(name="influencer").first()
            if not influencer_role:
                return make_response(jsonify({'message': 'Influencer role not found'}), 404)

             # Step 1: Fetch all influencers
            all_influencers = User.query.filter(User.roles.contains(influencer_role)).all()

            # Step 2: Get IDs of users with "Pending" flags
            flagged_user_ids = [
                flag.flagged_user_id for flag in Flag.query.filter(Flag.status == 'Pending').all()
            ]

            # Step 3: Filter out influencers whose flag status is "Pending"
            unflagged_influencers = [
                influencer for influencer in all_influencers if influencer.user_id not in flagged_user_ids
            ]
            # Format response
            influencer_data = [
                {
                    'user_id': influencer.user_id,
                    'username': influencer.username,
                    'email':influencer.email,
                    'category':influencer.category,
                    'niche': influencer.niche,
                    'reach': influencer.reach,
                }
                for influencer in unflagged_influencers
            ]

            return make_response(jsonify({
                'message': 'Influencers retrieved successfully',
                'influencers': influencer_data
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)

class SearchInfluencersAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def get(self):
        try:
            # Parse query parameters
            parser = reqparse.RequestParser()
            parser.add_argument('niche', type=str, required=False, help="Filter by niche")
            parser.add_argument('category', type=str, required=False, help="Filter by category")
            parser.add_argument('min_reach', type=int, required=False, help="Minimum reach")
            parser.add_argument('max_reach', type=int, required=False, help="Maximum reach")
            args = parser.parse_args()

            # Build query to exclude flagged influencers
            query = User.query.join(User.roles).filter(
                Role.name == 'influencer',
                User.user_id.notin_(
                    db.session.query(Flag.flagged_user_id).filter(Flag.status == 'Pending')
                )
            )

            # Apply filters
            if args['niche']:
                query = query.filter(User.niche.ilike(f"%{args['niche']}%"))
            if args['category']:
                query = query.filter(User.category.ilike(f"%{args['category']}%"))
            if args['min_reach']:
                query = query.filter(User.reach >= args['min_reach'])
            if args['max_reach']:
                query = query.filter(User.reach <= args['max_reach'])

            influencers = query.all()

            # Format response
            influencer_data = [
                {
                    'id': influencer.user_id,
                    'username': influencer.username,
                    'email': influencer.email,
                    'niche': influencer.niche,
                    'category': influencer.category,
                    'reach': influencer.reach,
                }
                for influencer in influencers
            ]

            return make_response(jsonify({
                'message': 'Influencers retrieved successfully',
                'influencers': influencer_data
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)




class CreateCampaignAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def post(self):
        try:
            campaign_data = request.get_json()
            name = campaign_data.get('name')
            description = campaign_data.get('description','')
            start_date = campaign_data.get('start_date')
            end_date = campaign_data.get('end_date')
            budget = campaign_data.get('budget')
            visibility = campaign_data.get('visibility', 'public')
            goals = campaign_data.get('goals','')

            # Validate data
            if not name or not start_date or not budget:
                return make_response(jsonify({'message': 'Name, start_date, and budget are required'}), 400)
            if visibility not in ['public', 'private']:
                return make_response(jsonify({'message': 'Visibility must be either "public" or "private"'}), 400)
            
            # Parse dates
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                return make_response(jsonify({'message': 'Invalid start_date format. Use YYYY-MM-DD'}), 400)

            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
            except ValueError:
                return make_response(jsonify({'message': 'Invalid end_date format. Use YYYY-MM-DD'}), 400)


            # Create Campaign
            campaign = Campaign(
                sponsor_id=current_user.user_id,
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                budget=budget,
                visibility=visibility,
                goals=goals
            )
            db.session.add(campaign)
            db.session.commit()

            return make_response(jsonify({'message': 'Campaign created successfully'}), 201)
        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

class UpdateCampaignAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def put(self, campaign_id):
        try:
            # Fetch the campaign
            campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=current_user.user_id).first()
            if not campaign:
                return make_response(
                    jsonify({'message': 'Campaign not found or you are not authorized to update this campaign'}),
                    403
                )

            # Get request data
            campaign_data = request.get_json()

            # Parse and validate dates
            if 'start_date' in campaign_data:
                try:
                    campaign.start_date = datetime.strptime(campaign_data['start_date'], "%Y-%m-%d").date()
                except ValueError:
                    return make_response(
                        jsonify({'message': 'Invalid format for start_date. Use yyyy-MM-dd'}),
                        400
                    )

            if 'end_date' in campaign_data and campaign_data['end_date']:
                try:
                    campaign.end_date = datetime.strptime(campaign_data['end_date'], "%Y-%m-%d").date()
                except ValueError:
                    return make_response(
                        jsonify({'message': 'Invalid format for end_date. Use yyyy-MM-dd'}),
                        400
                    )

            # Update other fields
            campaign.name = campaign_data.get('name', campaign.name)
            campaign.description = campaign_data.get('description', campaign.description)
            campaign.budget = campaign_data.get('budget', campaign.budget)
            campaign.visibility = campaign_data.get('visibility', campaign.visibility)
            campaign.goals = campaign_data.get('goals', campaign.goals)

            # Commit changes
            db.session.commit()

            return make_response(jsonify({'message': 'Campaign updated successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)


class ViewCampaignsAPI(Resource):
    @auth_token_required
    def get(self):
        try:
            # Get the role of the logged-in user
            role = [role.name for role in current_user.roles][0]

            # Get query parameters
            campaign_id = request.args.get('id')  # Optional parameter for specific campaign

            # Check if the user is flagged
            is_flagged_user = db.session.query(Flag).filter(
                Flag.flagged_user_id == current_user.user_id,
                Flag.status == 'Pending'
            ).first()
            if is_flagged_user and role == 'influencer':
                return make_response(jsonify({'message': f'Access denied. You are flagged and cannot view campaigns. Reason: {is_flagged_user.reason}'
                }), 403)

            # Fetch IDs of flagged influencers
            flagged_influencer_ids = db.session.query(Flag.flagged_user_id).filter(
                Flag.status == 'Pending',
                Flag.flagged_user_id.isnot(None)
            ).subquery()

            # Fetch IDs of flagged campaigns
            flagged_campaign_ids = db.session.query(Flag.flagged_campaign_id).filter(
                Flag.status == 'Pending',
                Flag.flagged_campaign_id.isnot(None)
            ).subquery()

            # Handle specific campaign query (e.g., for editing)
            if campaign_id:
                campaign = Campaign.query.filter_by(id=campaign_id).first()

                # Ensure sponsor can access their flagged campaign
                if role == 'sponsor' and campaign.sponsor_id != current_user.user_id:
                    return make_response(
                        jsonify({'message': 'Campaign not found or unauthorized access'}),
                        403
                    )

                # Ensure the campaign exists
                if not campaign:
                    return make_response(jsonify({'message': 'Campaign not found'}), 404)

                # Format the single campaign response
                ad_requests = AdRequest.query.join(User, AdRequest.influencer_id == User.user_id).filter(
                    AdRequest.campaign_id == campaign.id,
                    User.user_id.notin_(flagged_influencer_ids)
                ).all()

                ad_request_data = [
                    {
                        'id': ad_request.id,
                        'influencer_id': ad_request.influencer_id,
                        'influencer_name': ad_request.influencer.username,
                        'requirements': ad_request.requirements,
                        'payment_amount': ad_request.payment_amount,
                        'status': ad_request.status
                    }
                    for ad_request in ad_requests
                ]

                campaign_data = {
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date,
                    'end_date': campaign.end_date,
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'ad_requests': ad_request_data
                }

                return make_response(jsonify({'campaigns': [campaign_data]}), 200)

            # Query campaigns based on user role
            if role == 'sponsor':
                campaigns = Campaign.query.filter(
                    Campaign.sponsor_id == current_user.user_id,
                    Campaign.id.notin_(flagged_campaign_ids)
                ).all()

            elif role == 'admin':
                campaigns = Campaign.query.filter(
                    Campaign.id.notin_(flagged_campaign_ids)
                ).all()

            else:  # Influencer
                campaigns = Campaign.query.filter(
                    Campaign.visibility == 'public',
                    Campaign.id.notin_(flagged_campaign_ids)
                ).all()

            # Format campaigns and ad requests
            campaigns_data = []
            for campaign in campaigns:
                # Fetch ad requests excluding flagged influencers
                ad_requests = AdRequest.query.join(User, AdRequest.influencer_id == User.user_id).filter(
                    AdRequest.campaign_id == campaign.id,
                    User.user_id.notin_(flagged_influencer_ids)
                ).all()

                # Format ad requests for the campaign
                ad_request_data = [
                    {
                        'id': ad_request.id,
                        'influencer_id': ad_request.influencer_id,
                        'influencer_name': ad_request.influencer.username,
                        'requirements': ad_request.requirements,
                        'payment_amount': ad_request.payment_amount,
                        'status': ad_request.status
                    }
                    for ad_request in ad_requests
                ]

                # Append campaign details with filtered ad requests
                campaigns_data.append({
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date,
                    'end_date': campaign.end_date,
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'ad_requests': ad_request_data
                })

            return make_response(jsonify({'campaigns': campaigns_data}), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)


class DeleteCampaignAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def delete(self, campaign_id):
        try:
            # Fetch the campaign
            campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=current_user.user_id).first()
            if not campaign:
                return make_response(jsonify({'message': 'Campaign not found or you are not authorized to delete this campaign'}), 403)

            # Delete the campaign and associated ad requests
          
            AdRequest.query.filter_by(campaign_id=campaign.id).delete()
            db.session.delete(campaign)
            db.session.commit()

            return make_response(jsonify({'message': 'Campaign deleted successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)


class CreateAdRequestAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def post(self):
        try:
            # Get request data
            ad_data = request.get_json()
            campaign_id = ad_data.get('campaign_id')
            influencer_id = ad_data.get('influencer_id')
            requirements = ad_data.get('requirements')
            payment_amount = ad_data.get('payment_amount')

            # Validate required fields
            if not campaign_id or not influencer_id or not requirements or not payment_amount:
                return make_response(jsonify({
                    'message': 'Campaign ID, Influencer ID, Requirements, and Payment Amount are required'
                }), 400)

            # Ensure payment_amount is positive
            if not isinstance(payment_amount, (int, float)) or payment_amount <= 0:
                return make_response(jsonify({'message': 'Payment amount must be a positive number'}), 400)

            # Validate campaign ownership
            campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=current_user.user_id).first()
            if not campaign:
                return make_response(jsonify({'message': 'You can only create ad requests for your campaigns'}), 403)

            # Check if the ad request already exists between the same campaign and influencer
            existing_ad_request = AdRequest.query.filter_by(
                campaign_id=campaign_id,
                influencer_id=influencer_id
            ).first()
            if existing_ad_request:
                return make_response(jsonify({'message': 'An ad request for this influencer already exists for the campaign'}), 400)

            # Create the Ad Request
            ad_request = AdRequest(
                campaign_id=campaign_id,
                influencer_id=influencer_id,
                requirements=requirements,
                payment_amount=payment_amount,
                status='Pending'
            )

            db.session.add(ad_request)
            db.session.commit()

            return make_response(jsonify({'message': 'Ad request created successfully'}), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

class ViewAdRequestAPI(Resource):
    @auth_token_required
    def get(self):
        try:
            # Get the role of the logged-in user
            user = current_user
            role_names = [role.name for role in user.roles]

            # Parse query parameters
            status_filter = request.args.get('status', None)
            campaign_id_filter = request.args.get('campaign_id', None)

            # Base query
            query = AdRequest.query.join(Campaign).join(User, AdRequest.influencer_id == User.user_id)

            if "sponsor" in role_names:
                # Sponsors can view ad requests for their campaigns only
                query = query.filter(Campaign.sponsor_id == user.user_id)

            elif "influencer" in role_names:
                # Influencers can view only ad requests assigned to them
                query = query.filter(AdRequest.influencer_id == user.user_id)

            # Apply additional filters if provided
            if status_filter:
                query = query.filter(AdRequest.status == status_filter)
            if campaign_id_filter:
                query = query.filter(AdRequest.campaign_id == campaign_id_filter)

            # Retrieve filtered results
            ad_requests = query.all()

            # Format response
            ad_requests_data = [
                {
                    'id': ad_request.id,
                    'campaign_name': ad_request.campaign.name,
                    'influencer_name': ad_request.influencer.username,
                    'messages': ad_request.messages,
                    'requirements': ad_request.requirements,
                    'payment_amount': ad_request.payment_amount,
                    'status': ad_request.status,
                }
                for ad_request in ad_requests
            ]

            response = {
                'message': 'Ad requests retrieved successfully',
                'ad_requests': ad_requests_data
            }
            return make_response(jsonify(response), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)



class UpdateAdRequestAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def put(self, adrequest_id):
        try:
            # Fetch the ad request
            ad_request = AdRequest.query.join(Campaign).filter(
                AdRequest.id == adrequest_id,
                Campaign.sponsor_id == current_user.user_id
            ).first()
            if not ad_request:
                return make_response(jsonify({'message': 'Ad request not found or you are not authorized to update this ad request'}), 403)

            # Get request data
            ad_data = request.get_json()

            # Update fields
            ad_request.requirements = ad_data.get('requirements', ad_request.requirements)
            ad_request.payment_amount = ad_data.get('payment_amount', ad_request.payment_amount)

            db.session.commit()

            return make_response(jsonify({'message': 'Ad request updated successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

class DeleteAdRequestAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def delete(self, adrequest_id):
        try:
            # Fetch the ad request
            ad_request = AdRequest.query.join(Campaign).filter(
                AdRequest.id == adrequest_id,
                Campaign.sponsor_id == current_user.user_id
            ).first()
            if not ad_request:
                return make_response(jsonify({'message': 'Ad request not found or you are not authorized to delete this ad request'}), 403)

            # Delete the ad request
            db.session.delete(ad_request)
            db.session.commit()

            return make_response(jsonify({'message': 'Ad request deleted successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)


class CampaignStatisticsAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def get(self, campaign_id):
        try:
            # Verify campaign ownership
            campaign = Campaign.query.filter_by(id=campaign_id, sponsor_id=current_user.user_id).first()
            if not campaign:
                return make_response(jsonify({'message': 'Campaign not found or unauthorized access'}), 403)

            # Calculate budget utilization
            total_budget = campaign.budget
            spent_budget = db.session.query(db.func.sum(AdRequest.payment_amount)).filter_by(
                campaign_id=campaign_id,
                status='Accepted'
            ).scalar() or 0
            remaining_budget = total_budget - spent_budget

            # Count ad request statuses
            ad_request_statuses = db.session.query(
                AdRequest.status,
                db.func.count(AdRequest.id)
            ).filter_by(campaign_id=campaign_id).group_by(AdRequest.status).all()

            ad_request_counts = {status: count for status, count in ad_request_statuses}

            # Format response
            campaign_stats = {
                'campaign_id': campaign.id,
                'name': campaign.name,
                'total_budget': total_budget,
                'spent_budget': spent_budget,
                'remaining_budget': remaining_budget,
                'ad_request_counts': ad_request_counts
            }

            return make_response(jsonify({
                'message': 'Campaign statistics retrieved successfully',
                'campaign_statistics': campaign_stats
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)


class SponsorRespondNegotiationAPI(Resource):
    @auth_token_required
    @roles_required('sponsor')
    def put(self, adrequest_id):
        try:
            # Fetch the ad request
            ad_request = AdRequest.query.join(Campaign).filter(
                AdRequest.id == adrequest_id,
                Campaign.sponsor_id == current_user.user_id
            ).first()
            if not ad_request:
                return make_response(jsonify({'message': 'Ad request not found or unauthorized access'}), 403)

            # Parse the input payload
            data = request.get_json()
            status = data.get('status')  # "Accepted", "Rejected", or "Negotiated"
            payment_amount = data.get('payment_amount')  # Required for "Negotiated"
            message = data.get('message', None)  # Optional message

            if status not in ['Accepted', 'Rejected', 'Negotiated']:
                return make_response(jsonify({'message': 'Invalid status'}), 400)

            # Update ad request
            ad_request.status = status
            if status == 'Negotiated':
                if not payment_amount:
                    return make_response(jsonify({'message': 'Payment amount is required for negotiation'}), 400)
                ad_request.payment_amount = payment_amount
                ad_request.messages = message if message else "Terms updated by sponsor."

            db.session.commit()

            return make_response(jsonify({
                'message': 'Ad request updated successfully',
                'ad_request_id': ad_request.id,
                'new_status': ad_request.status,
                'updated_payment_amount': ad_request.payment_amount
            }), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)




'''Influencer api'''
class PublicCampaignSearchAPI(Resource):
    @auth_token_required
    @roles_required('influencer')
    def get(self):
        try:
            # Parse query parameters
            parser = reqparse.RequestParser()
            parser.add_argument('niche', type=str, required=False, help="Filter by niche")
            parser.add_argument('budget_min', type=float, required=False, help="Minimum budget")
            parser.add_argument('budget_max', type=float, required=False, help="Maximum budget")
            args = parser.parse_args()

            # Build query for public campaigns excluding flagged ones
            query = Campaign.query.filter(
                (Campaign.visibility == 'public') &
                (Campaign.id.notin_(
                    db.session.query(Flag.flagged_campaign_id).filter(Flag.status == 'Pending')
                ))
            )

            # Apply filters
            if args['niche']:
                query = query.filter(Campaign.goals.ilike(f"%{args['niche']}%"))
            if args['budget_min']:
                query = query.filter(Campaign.budget >= args['budget_min'])
            if args['budget_max']:
                query = query.filter(Campaign.budget <= args['budget_max'])

            campaigns = query.all()

            # Format response
            campaign_data = [
                {
                    'campaign_id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'budget': campaign.budget,
                    'goals': campaign.goals
                }
                for campaign in campaigns
            ]

            return make_response(jsonify({
                'message': 'Public campaigns retrieved successfully',
                'campaigns': campaign_data
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal error', 'error': str(e)}), 500)

class InfluencerAdRequestsAPI(Resource):
    @auth_token_required
    @roles_required('influencer')
    def get(self):
        try:
            # Fetch ad requests for the logged-in influencer, excluding flagged campaigns
            ad_requests = AdRequest.query.filter(
                AdRequest.influencer_id == current_user.user_id,
                AdRequest.campaign_id.notin_(
                    db.session.query(Flag.flagged_campaign_id).filter(Flag.status == 'Pending')
                )
            ).join(Campaign).add_columns(
                Campaign.name.label('campaign_name'),
                Campaign.description.label('campaign_description'),
                Campaign.start_date,
                Campaign.budget
            ).all()

            # Format response
            ad_request_data = [
                {
                    'ad_request_id': ad_request.AdRequest.id,
                    'campaign_id': ad_request.AdRequest.campaign_id,
                    'campaign_name': ad_request.campaign_name,
                    'campaign_description': ad_request.campaign_description,
                    'messages': ad_request.AdRequest.messages,
                    'requirements': ad_request.AdRequest.requirements,
                    'payment_amount': ad_request.AdRequest.payment_amount,
                    'status': ad_request.AdRequest.status
                }
                for ad_request in ad_requests
            ]

            return make_response(jsonify({
                'message': 'Ad requests retrieved successfully',
                'ad_requests': ad_request_data
            }), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)

class InfluencerRespondAdRequestAPI(Resource):
    @auth_token_required
    @roles_required('influencer')
    def put(self, adrequest_id):
        try:
            # Fetch the ad request
            ad_request = AdRequest.query.filter_by(id=adrequest_id, influencer_id=current_user.user_id).first()
            if not ad_request:
                return make_response(jsonify({'message': 'Ad request not found or unauthorized access'}), 403)

            # Parse the input payload
            data = request.get_json()
            status = data.get('status')  # "Accepted", "Rejected", or "Negotiated"
            payment_amount = data.get('payment_amount')  # Optional, only for "Negotiated"
            message = data.get('message', None)  # Optional negotiation message

            if status not in ['Accepted', 'Rejected', 'Negotiated']:
                return make_response(jsonify({'message': 'Invalid status'}), 400)

            # Update ad request
            ad_request.status = status
            if status == 'Negotiated':
                if not payment_amount:
                    return make_response(jsonify({'message': 'Payment amount is required for negotiation'}), 400)
                ad_request.payment_amount = payment_amount
                ad_request.messages = message if message else "Negotiated terms by influencer."

            db.session.commit()

            return make_response(jsonify({
                'message': 'Ad request updated successfully',
                'ad_request_id': ad_request.id,
                'new_status': ad_request.status,
                'updated_payment_amount': ad_request.payment_amount
            }), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)


class InfluencerCreateAdRequestAPI(Resource):
    @auth_token_required
    @roles_required('influencer')
    def post(self, campaign_id):
        try:
            # Fetch the public, non-flagged campaign
            campaign = Campaign.query.filter(
                Campaign.id == campaign_id,
                Campaign.visibility == 'public',
                Campaign.id.notin_(
                    db.session.query(Flag.flagged_campaign_id).filter(Flag.status == 'Pending')
                )
            ).first()
            # Check if an ad request already exists for this campaign and influencer
            existing_ad_request = AdRequest.query.filter_by(
                campaign_id=campaign_id,
                influencer_id=current_user.user_id
            ).first()

            if existing_ad_request:
                return make_response(jsonify({'message': 'An ad request for this campaign already exists'}), 400)

            if not campaign:
                return make_response(jsonify({'message': 'Campaign not found or it is flagged'}), 404)

            # Parse request data
            data = request.get_json()
            requirements = data.get('requirements')
            payment_amount = data.get('payment_amount')

            if not requirements or not payment_amount:
                return make_response(jsonify({'message': 'Requirements and payment amount are required'}), 400)

            # Create a new ad request
            ad_request = AdRequest(
                campaign_id=campaign_id,
                influencer_id=current_user.user_id,
                messages=data.get('message', 'Ad request created by influencer'),
                requirements=requirements,
                payment_amount=payment_amount,
                status='Negotiated'
            )

            db.session.add(ad_request)
            db.session.commit()

            return make_response(jsonify({
                'message': 'Ad request created successfully',
                'ad_request_id': ad_request.id,
                'campaign_id': campaign_id,
                'status': ad_request.status
            }), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': 'Internal server error', 'error': str(e)}), 500)
