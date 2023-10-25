from pydantic import BaseModel, validator
from fastapi.exceptions import RequestValidationError


class Geometry(BaseModel):
	type: str | None = None
	coordinates: list | None = None

	@validator('type', pre=True, always=True)
	def type_validate(cls, field_value):
		if not field_value:
			raise RequestValidationError("'type' in 'geometry' must be specified")
		if field_value not in ["Polygon", "Point"]:
			raise RequestValidationError("Invalid geometry type")

		return field_value

	@validator('coordinates', pre=True, always=True)
	def coordinates_validate(cls, field_value, values):
		if not field_value:
			raise RequestValidationError("'coordinates' in 'geometry' must be specified")
		t = values["type"]
		if t == 'Point':
			if len(field_value) != 2:
				raise RequestValidationError("Point coordinates must contains two numbers")
		return field_value


class AggregationRequest(BaseModel):
	geometry: Geometry | None = None
	field: str | None = None
	aggr: str | None = None
	r: int | None = None

	@validator("geometry", pre=True, always=True)
	def geometry_validate(cls, geometry):
		if not geometry:
			raise RequestValidationError("'geometry' must be specified")
		return geometry

	@validator('aggr', pre=True, always=True)
	def aggr_validate(cls, aggr):
		if not aggr:
			raise RequestValidationError("'aggr' must be specified")
		if aggr not in ["sum","mean","min","max","avg"]:
			raise RequestValidationError("Invalid aggr field."
					"Choose 'aggr' from ['sum', 'mean', 'min', 'max', 'avg']")
		return aggr

	@validator('field', pre=True, always=True)
	def field_validate(cls, f_field):
		if not f_field:
			raise RequestValidationError("'field' must be specified")
		return f_field

	@validator('r', pre=True, always=True)
	def validate_r_for_point(cls, r, values):
		geometry = values.get('geometry')
		if geometry and geometry.type == 'Point':
			if not r:
				raise RequestValidationError("'r' is required for 'Point' geometry")
			if not isinstance(r, int):
				raise RequestValidationError("'r' must be an integer for 'Point' geometry")
		return r
