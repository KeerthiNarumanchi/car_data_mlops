import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import logging

# Set up logging to output to both console and file
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # This ensures all log levels (DEBUG, INFO, ERROR, etc.) are logged

# Create handlers
console_handler = logging.StreamHandler()  # To log to the console
file_handler = logging.FileHandler('app_logs.log')  # To log to a file

# Set logging levels for handlers
console_handler.setLevel(logging.DEBUG)  # Adjust based on your needs (e.g., DEBUG, INFO)
file_handler.setLevel(logging.DEBUG)

# Create a formatter and attach it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Initialize the FastAPI app
app = FastAPI()

# Load the XGBoost model and preprocessing pipeline
try:
    model_pipeline = joblib.load('xgboost_model_pipeline.pkl')
    logger.info("Model loaded successfully!")
    # Validate pipeline components
    assert 'preprocessor' in model_pipeline.named_steps, "Missing preprocessor in pipeline."
    assert 'model' in model_pipeline.named_steps, "Missing model in pipeline."
except Exception as e:
    logger.error(f"Failed to load model: {e}", exc_info=True)
    raise RuntimeError("Failed to load model pipeline. Ensure the .pkl file is valid and correctly configured.")

# Define input data structure
class CarData(BaseModel):
    Mileage: float
    EngineV: float
    Year: int
    Brand: str
    Body: str
    Engine_Type: str
    Registration: str
    Model: str
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")


@app.post("/predict")
def predict(car_data: CarData):
    try:
        # Log raw input data
        logger.debug(f"Raw input data: {car_data.dict()}")

        # Convert input to DataFrame
        input_data = [[
            car_data.Mileage,
            car_data.EngineV,
            car_data.Year,
            car_data.Brand,
            car_data.Body,
            car_data.Engine_Type,
            car_data.Registration,
            car_data.Model
        ]]
        columns = ['Mileage', 'EngineV', 'Year', 'Brand', 'Body', 'Engine Type', 'Registration', 'Model']

        input_df = pd.DataFrame(input_data, columns=columns)
        logger.debug(f"Input DataFrame:\n{input_df}")

        # Preprocess input
        preprocessed_input = model_pipeline.named_steps['preprocessor'].transform(input_df)
        logger.debug(f"Preprocessed input:\n{preprocessed_input}")

        # Convert sparse matrix to dense
        preprocessed_input = preprocessed_input.toarray()
        logger.debug(f"Preprocessed dense input:\n{preprocessed_input}")

        # Make prediction
        predicted_price = model_pipeline.named_steps['model'].predict(preprocessed_input)[0]
        logger.info(f"Prediction: {predicted_price}")
        return {"prediction": predicted_price}

    except ValueError as ve:
        logger.error(f"ValueError during prediction: {ve}", exc_info=True)
        return {"error": f"Preprocessing or prediction failed. Error: {ve}"}

    except KeyError as ke:
        logger.error(f"KeyError: Missing expected column or key in input: {ke}", exc_info=True)
        return {"error": f"Input format error. Missing field: {ke}"}

    except Exception as e:
        logger.error(f"Unhandled error during prediction: {e}", exc_info=True)
        return {"error": f"Internal Server Error. Details: {e}"}
