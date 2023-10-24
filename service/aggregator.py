from fastapi import FastAPI, APIRouter, HTTPException
from h3 import h3
from pydantic import BaseModel
from typing import List
from service.data_loader import load_data
from service.models import Geometry, AggregationRequest
import numpy as np


app = APIRouter()

data = load_data()

operations = {
	"sum": np.sum,
	"mean": np.mean,
	"min": np.amin,
	"max": np.amax,
	"avg": np.average
}



@app.post("/calculate_aggregation/")
async def calculate_aggregation(request: AggregationRequest):
	geometry = request.geometry
	match geometry.type:
		case "Point":
			lat, lon = geometry.coordinates[1], geometry.coordinates[0]
			h3_hex = h3.geo_to_h3(lat, lon, resolution=11)
			k_ring = h3.k_ring(h3_hex, k=request.r)
			filtered_data = data[data['h3_hex'].isin(k_ring)]
			result = operations[request.aggr](filtered_data[request.field])
			return {"data": float(round(result, 2))}
		case "Polygon":
			coors = [[(coor[1], coor[0]) for coor in path] for path in geometry.coordinates]
			poly = h3.polyfill({"type":"Polygon", "coordinates": coors}, res=11)
			filtered_data = data[data['h3_hex'].isin(poly)]
			result = operations[request.aggr](filtered_data[request.field])
			return {"data": float(round(result, 2))}

		case _:
			raise HTTPException(422, "Invalid geometry type")
