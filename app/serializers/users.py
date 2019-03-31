"""User serializer"""

import datetime

import flask_bcrypt

from dateutil.relativedelta import relativedelta
from marshmallow import fields, post_load, validates, ValidationError, Schema

from app.models import ma
from app.models.users import Users

DATE_FORMAT = '%Y-%m-%d'


class UsersModelSchema(ma.ModelSchema):
    """User model serializer"""
    id = fields.String(dump_only=True)
    google_access_token = fields.String(load_only=True, required=False)
    birth_date = fields.Date(DATE_FORMAT)
    email = fields.Email(required=True)
    password = fields.String(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        """Meta class"""
        model = Users

    @post_load
    def customized_data(self, data):
        """data customization"""
        if hasattr(data, 'password') or ('password' in list(data.keys())):
            data['password'] = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')

        return data

    @validates('email')
    def validate_email(self, email):
        """email validation : email length shouldn't be more than 50"""
        max_length = 50
        if self.instance:
            if self.instance.email != email:
                raise ValidationError('User email can not be changed')
        elif not self.instance:
            if len(email) > max_length:
                raise ValidationError('Email length should not be greater than 50')
            user = Users.query.filter(Users.email == email).count()
            if user > 0:
                raise ValidationError('A registered user found with this email')

    @validates('status')
    def validate_status(self, status):
        """user status : 1. Regular, 2. locked, 3.Blocked"""
        status_found = [item for item in Users.STATUS if status in item]
        if not status_found:
            raise ValidationError('Invalid status code')

    @validates('birth_date')
    def validate_birth_date(self, birth_date):
        """user birthday validation , input taken in yyyy-mm-dd format"""
        age_limit = 5
        difference_in_years = relativedelta(datetime.datetime.now(), birth_date).years
        if difference_in_years < age_limit:
            raise ValidationError('User should be greater than 5')


class UsersFilterSerializer(Schema):
    """User filter parameter validation"""

    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    username = fields.String(required=False)
    email = fields.Email(required=False)
    phone = fields.String(required=False)
    birth_date = fields.Date(DATE_FORMAT, required=False)

    active = fields.Boolean(required=False)
    status = fields.String(required=False)
    updated_at = fields.DateTime(DATE_FORMAT, required=False)

    @post_load
    def customized_params(self, data):
        """User filter parameter customization"""
        if hasattr(data, 'status') or ('status' in list(data.keys())):
            status = [item for item in Users.STATUS if data['status'].capitalize() in item]
            try:
                data['status'] = status[0][0]
            except IndexError:
                data['status'] = 1
        if hasattr(data, 'updated_at') or ('updated_at' in list(data.keys())):
            data['updated_at'] = data['updated_at'].date()
        return data
