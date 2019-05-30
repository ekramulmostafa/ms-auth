"""User service and required helper methods"""

from smtplib import SMTPException

from datetime import datetime, timedelta
from uuid import uuid4

from jinja2 import TemplateNotFound
from sqlalchemy import or_
from sqlalchemy import cast, DATE
from sqlalchemy.orm.exc import NoResultFound

from flask import current_app as app, render_template

from app.models import db
from app.models.users import Users
from app.models.verification_codes import VerificationCodes

from app.serializers.users import UsersModelSchema, UsersFilterSerializer, UsersLoginSerializer
from app.logging import Logger

from app.utils.utils import send_email, decode_auth_token, encode_auth_token, response_generator

user_schema = UsersModelSchema()
users_schema = UsersModelSchema(many=True)

logger = Logger(__name__)


class UsersServices:
    """User services to call internally"""

    def get_all_users(self, params=None):
        """
            GET all users
            api: /v1/user/
                 /v1/user/?search=admin11
                 /v1/user/?sorted_by=username&order_by=asc&offset=0&limit=5&search=admin11
                 /v1/user/?sorted_by=username&active=true&status=regular&updated_at=2019-03-11
        """
        logger.info("User list get")
        query = db.session.query(Users)

        valid_param, errors = UsersFilterSerializer().load(params)
        if errors:
            logger.warning("User validation failed", data=errors)
            return {'status': 'error', 'data': {}, 'message': errors}, 400

        updated_at = None
        if 'updated_at' in list(valid_param.keys()):
            updated_at = valid_param.pop('updated_at')

        sub_params = {
            'search': params.pop('search'),
            'offset': params.pop('offset'),
            'limit': params.pop('limit'),
            'sort_by': params.pop('sort_by'),
            'order_by': params.pop('order_by')
        }

        if sub_params['search']:
            search_query = []
            for searchable_field in Users.__searchable__:
                search_query.append(
                    Users.__getattribute__(
                        Users, searchable_field).like("%"+sub_params['search']+"%")
                )
            query = query.filter(or_(*tuple(search_query)))
        else:
            query = query.filter_by(**valid_param)
        if updated_at:
            query = query.filter(cast(Users.updated_at, DATE) == updated_at)

        query = query.order_by(sub_params['sort_by']+" "+sub_params['order_by'].lower())
        limit_query = query.offset(sub_params['offset'])
        limit_query = limit_query.limit(sub_params['limit'])
        all_users = limit_query.all()
        total = query.count()

        users_data = users_schema.dump(all_users)
        response = {
            'total': total,
            'offset': sub_params['offset'],
            'limit': sub_params['limit'],
            'users': users_data.data
        }
        return {'status': 'success', 'data': response, 'message': ''}, 200

    def get_user_details(self, uuid):
        """User details method"""

        logger.info("User Detail get", data={'uuid': str(uuid)})
        try:
            user = Users.query.get(uuid)
            if not user:
                return {'status': 'error', 'data': {}, 'message': 'No user found'}, 400
            response_data = user_schema.dump(user)
            return {'status': 'success', 'data': response_data.data, 'message': ''}, 200
        except NoResultFound as ex:
            logger.warning("User no result found", data=str(ex))
            return {'status': 'error', 'data': {}, 'message': str(ex)}, 400

    def create(self, data: dict):
        """User create method"""
        if not data:
            raise Exception('No input data provided')
        result_data, errors = user_schema.load(data)
        if errors:
            return {'status': 'error', 'data': {}, 'message': errors}, 422
        result_data.save()
        response_data = user_schema.dump(result_data).data
        VerificationCodes.save_verification_code(user=result_data, types=2, status=1)
        return {'status': 'success', 'data': response_data, 'message': ''}, 201

    def update(self, data: dict, uuid):
        """specific User update"""
        logger.info("User update", data={'uuid': str(uuid)})
        user = Users.query.filter_by(id=uuid).first()
        if not user:
            return {'status': 'error', 'data': {}, 'message': 'No user found'}, 400
        result_data, errors = user_schema.load(data, instance=user, partial=True)
        if errors:
            logger.info("User update input", data=data)
            logger.warning("User update error", data=errors)
            return {'status': 'error', 'data': {}, 'message': errors}, 422
        result_data.save()
        response_data = user_schema.dump(result_data).data
        return {'status': 'success', 'data': response_data, 'message': ''}, 200

    def login(self, data: dict):
        """ user login"""
        login_schema = UsersLoginSerializer()
        result_data, errors = login_schema.load(data)
        if errors:
            return {'status': 'error', 'data': {}, 'message': errors}, 422

        user = None

        if 'email' in result_data:
            user = Users.query.filter_by(email=data['email']).first()
        elif 'phone' in result_data:
            user = Users.query.filter_by(phone=data['phone']).first()

        is_correct_password = False
        if user:
            is_correct_password = Users.check_password(user.password, result_data['password'])

        if is_correct_password:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': str(user.id),
                'roles': [str(role.id) for role in user.roles]
            }
            jwt_token = encode_auth_token(payload)
            return {'status': 'success',
                    'data': {
                        'token': jwt_token
                    },
                    'message': ''}, 200
        return {'status': 'error', 'data': {}, 'message': 'Incorrect password'}, 400

    def forget_password(self, data: dict):
        """forget password"""
        user = None
        if 'email' in data:
            user = Users.query.filter_by(email=data['email']).first()
        elif 'phone' in data:
            user = Users.query.filter_by(phone=data['phone']).first()

        if not user:
            return {'status': 'error', 'data': {}, 'message': 'No User found'}, 400

        reset_code = uuid4()
        email_data = {
            "subject": "Forget Password",
            "sender": app.config.get('MAIL_USERNAME'),
            "recipients": [user.email],
            'html': render_template('reset_password.html', code=reset_code)
        }
        try:
            send_email(email_data)
            VerificationCodes.save_verification_code(user=user, code=reset_code, types=1, status=1)
            return {'status': 'success',
                    'data': {},
                    'message': 'A password reset code has been sent to email address'
                    }, 200
        except TemplateNotFound:
            return {'status': 'error',
                    'data': {},
                    'message': 'Email template not found'
                    }, 400
        except SMTPException:
            return {'status': 'error',
                    'data': {},
                    'message': 'sending email failed'
                    }, 400

    def verify_user(self, verification_code=None):
        """user verification"""
        vc_obj = VerificationCodes.query.filter_by(code=verification_code,
                                                   types=2,
                                                   status=1).first()
        user = vc_obj.verified_user if vc_obj else None
        if user:
            if vc_obj.expired_at and (vc_obj.expired_at < datetime.utcnow()):
                return {'status': 'error',
                        'data': {},
                        'message': 'verification code has been expired'}, 400
            if user.verified:
                return {'status': 'error', 'data': {}, 'message': 'User already verified'}, 400
            user.verified = True
            user.verified_at = datetime.utcnow()
            vc_obj.status = 2
            vc_obj.updated_by = str(vc_obj.user_id)
            db.session.commit()
            response_data = user_schema.dump(user).data
            return {'status': 'success', 'data': response_data, 'message': ''}, 200
        return {'status': 'error', 'data': {}, 'message': 'user verification failed'}, 400

    def reset_password(self, data: dict, code=None):
        """user password reset"""
        vc_obj = VerificationCodes.query.filter_by(code=code,
                                                   types=1,
                                                   status=1).first()
        user = vc_obj.verified_user if vc_obj else None
        if user:
            if vc_obj.expired_at and (vc_obj.expired_at < datetime.utcnow()):
                return {'status': 'error',
                        'data': {},
                        'message': 'password reset code has been expired'}, 400
            self.update({
                "password": data['password']
            }, uuid=str(user.id))
            vc_obj.status = 2
            vc_obj.updated_by = str(vc_obj.user_id)
            db.session.commit()
            return {'status': 'success',
                    'data': {},
                    'message': 'password updated successfully'}, 200
        return {'status': 'error', 'data': {}, 'message': 'Reset password failed'}, 400

    def get_user_from_token(self, token=None):
        """
        get user from token
        response : object
        """
        token = token.split(' ')[1]
        jwt_resp = decode_auth_token(token)['data']
        user = Users.query.filter_by(id=jwt_resp['sub']).first()
        return user

    def update_password(self, data: dict, user=None):
        """specific User update"""

        logger.info("current user password update", data={'uuid': str(user.id)})
        is_correct_password = Users.check_password(user.password, data['current_password'])
        if not is_correct_password:
            return {'status': 'error', 'data': {}, 'message': 'Incorrect password'}, 400

        response = self.update({
            "password": data['new_password'],
            "updated_by": str(user.id)
        }, uuid=str(user.id))
        if response[1] != 200:
            return {'status': 'error', 'data': {}, 'message': 'password can not be updated'}, 400
        return {'status': 'success',
                'data': {},
                'message': 'password updated successfully'}, 200

    def get_all(self):
        """User get all"""
        logger.info("User list get")
        all_users = Users.query.all()
        result = users_schema.dump(all_users)
        return response_generator(status='success', data=result, message=''), 200

    def fetch(self, uuid=None):
        """User details method"""

        if uuid:
            return self.get_user_details(uuid)
        else:
            return self.get_all()
