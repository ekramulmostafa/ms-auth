"""Verification codes serializer"""

from app.models import ma

from app.models.verification_codes import VerificationCodes


class VerificationCodesModelSchema(ma.ModelSchema):
    """VerificationCodes model serializer"""

    class Meta:
        """Meta class"""
        model = VerificationCodes
