from fastapi import FastAPI
from service.aggregator import app as aggregator_app
from service.data_loader import load_data
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
	return JSONResponse(f"Validation error: {exc}", status_code=422)


app.include_router(aggregator_app, prefix="/aggregator")



if __name__ == "__main__":
	data = load_data()
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)
