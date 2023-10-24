from pydantic import BaseModel, validator, Field
from typing import Optional, Any
from fastapi.exceptions import RequestValidationError

class Geometry(BaseModel):
	type: str | None = None
	coordinates: list | None = None

	@validator('type')
	def type_validate(cls, field_value):
		if not field_value:
			raise RequestValidationError("Type must be specified")
		if field_value not in ["Polygon", "Point"]:
			raise RequestValidationError("Invalid geometry type")

		return field_value

	@validator('coordinates')
	def coordinates_validate(cls, field_value, values):
		if not field_value:
			raise RequestValidationError("Coordinates must be specified")
		t = values["type"]
		if t == 'Point':
			if len(field_value) != 2:
				raise RequestValidationError("Point coordinates must contains two numbers")
		return field_value

class AggregationRequest(BaseModel):
	geometry: Geometry
	field: str | None = None
	aggr: str
	r: int | None = None

	@validator('aggr')
	def aggr_validate(cls, aggr):
		if aggr not in ["sum","mean","min","max","avg"]:
			raise RequestValidationError("Invalid aggr field")
		return aggr

	@validator('field', always=True)
	def field_validate(cls, f_field):
		if not f_field:
			raise RequestValidationError("Field must be specified")
		return f_field

	@validator('field', always=True)
	def r_validate(cls, r):
		if not r:
			raise RequestValidationError("Field must be specified")
		return r

	@validator('r', pre=True, always=True)
	def validate_r_for_point(cls, r, values):
		t = values["type"]
		if t == 'Point':
			if not r:
				raise RequestValidationError("'r' is required for 'Point' geometry")
			if not isinstance(r, int):
				raise RequestValidationError("'r' must be an integer for 'Point' geometry")
		return r
