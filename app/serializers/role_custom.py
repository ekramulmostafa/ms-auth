"""Role custom model Schema"""
from marshmallow import fields
from app.models import ma


class RoleCustomSchema(ma.ModelSchema):
    """Role custom model Schema"""
    id = fields.String()
    name = fields.String()
    active = fields.String()
    created_at = fields.String(dump_only=True)
    updated_at = fields.String(dump_only=True)
