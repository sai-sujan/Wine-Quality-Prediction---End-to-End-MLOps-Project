# pipelines/utils.py
import pandas as pd

def get_data_for_test():
    """Returns sample data for inference testing"""
    df = pd.read_csv("data/olist_customers_dataset.csv")
    
    # Select only the columns the model expects for prediction
    columns_for_prediction = [
        "payment_sequential",
        "payment_installments",
        "payment_value",
        "price",
        "freight_value",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    
    df = df[columns_for_prediction].dropna().head(5)
    return df.to_json(orient="split")