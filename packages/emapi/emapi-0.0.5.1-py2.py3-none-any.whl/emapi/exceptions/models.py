from .base import BaseEmapiError


class ModelConflict(BaseEmapiError):
	"""Duplicate key in INSERT/UPDATE operation"""

	status_code = 409
