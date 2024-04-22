import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# import random forest regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from load_data import read_data
from sklearn.preprocessing import StandardScaler


def write_model_to_blob(connection_string, container_name):

    # Step 1: read data from azure blob
    data, message = read_data("dk_data_clean")

    # Step 2: Split the data into train and test sets
    train_data = data.iloc[:37000]
    

    train_x = train_data.drop(columns=["DateTime", "SpotPriceDKK"])
    train_y = train_data["SpotPriceDKK"]

    # Step 3: Standardize the features
    scaler = StandardScaler()
    train_x_scaled = scaler.fit_transform(train_x)

    print("done")
    # Train the model. Random forest regression
    model = RandomForestRegressor()

    # Define the parameter grid
    param_grid = {
        "n_estimators": [
            10,
            50,
            100,
            200,
            300,
            500,
            1000,
        ],  # Number of trees in the forest
        "max_depth": [None, 10, 20, 50, 100, 200],  # Maximum depth of the trees
        "min_samples_split": [
            2,
            5,
            10,
            20,
            40,
            60,
        ],  # Minimum number of samples required to split a node
        "min_samples_leaf": [
            1,
            2,
            4,
            5,
            10,
            15,
            20,
        ],  # Minimum number of samples required at each leaf node
        "max_features": ['sqrt', 'log2'],  # Number of features to consider at each split
        "bootstrap": [True],
        "max_samples": [
            0.5,
            0.7,
            0.9,
            1.0,
        ],  # Percentage of samples used for fitting the individual base learners
    }

    # Perform Randomized Search CV
    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_grid,
        n_iter=5,
        cv=10,
        verbose=3,
        n_jobs=-1,
        scoring="neg_mean_squared_error",
    )

    # Fit the model
    random_search.fit(train_x_scaled, train_y)

    # step 3: serialize the model
    model_filename = "RandomForestModel.pkl"
    # joblib.dump(model, model_filename)

    with open(model_filename, "wb") as f:
        pickle.dump(random_search, f)

    # Step 4: Upload the Serialized Model to Azure Blob Storage
    # Upload the serialized model file to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Set the blob name (should be the same as model_filename)
    blob_name = model_filename

    # Get the blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the serialized model file to Azure Blob Storage
    with open(model_filename, "rb") as data:
        blob_client.upload_blob(
            data, overwrite=True, connection_timeout=14400, timeout=600
        )
    return "Model uploaded to Azure Blob Storage successfully."

if __name__ == "__main__":
    # run the function
    connection_string = "DefaultEndpointsProtocol=https;AccountName=luminaresourcegroupbf89;AccountKey=1w6aeiFsYO3KRkiE2eTwCtGASAtV/mtzerad4VKJXtmDSOfweXkGwt6WCT8tZnAwZQGmC6ZxIsup+AStduOCkA==;EndpointSuffix=core.windows.net"
    container_name = "spiriiblob"
    write_model_to_blob(connection_string, container_name)


