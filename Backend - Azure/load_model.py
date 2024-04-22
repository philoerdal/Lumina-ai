import pickle
import joblib
from azure.storage.blob import BlobServiceClient

# Read model from Azure Blob Storage
def load_azure_ml_model_from_blob(
    storage_account_name, storage_account_key, container_name, blob_name
):
    try:
        # Create a connection string
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"

        # Create a BlobServiceClient using the connection string
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        # Get a container client
        container_client = blob_service_client.get_container_client(container_name)

        # Get a blob client for the specified blob
        blob_client = container_client.get_blob_client(blob_name)

        # Download the blob data (model file)
        blob_data = blob_client.download_blob().readall()

        # Deserialize the model from the downloaded data
        loaded_model = pickle.loads(blob_data)
        #loaded_model = joblib.load(blob_data)
        return loaded_model, "Success"

    except Exception as e:
        return None, f"Error: {str(e)}"