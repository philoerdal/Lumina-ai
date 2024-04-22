import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import pandas as pd


# Function to get Excel data from a blob
def __get_excel_data_from_blob(
    storage_account_name, storage_account_key, container_name, blob_name
):
    try:
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)

        # Check if the blob exists
        if not blob_client.exists():
            return None, "Blob not found"

        # Download the blob data (assuming it's in binary format)
        blob_data = blob_client.download_blob().readall()

        # Convert bytes data to a file-like object
        blob_data_filelike = io.BytesIO(blob_data)

        # Now you can process the Excel data using pandas
        excel_data = pd.read_csv(blob_data_filelike)

        data_tail = excel_data.tail(1821)

        # Change the read function based on your file format
        return data_tail, "Success"
    except Exception as e:
        return None, f"Error: {str(e)}"

def read_data(dataset):
    # Open prediction dataset
    # payload
    storagename = "luminaresourcegroupbf89"
    storagekey = "1w6aeiFsYO3KRkiE2eTwCtGASAtV/mtzerad4VKJXtmDSOfweXkGwt6WCT8tZnAwZQGmC6ZxIsup+AStduOCkA=="
    containername = "spiriiblob"
    blobname = f"{dataset}.csv"

    return __get_excel_data_from_blob(storage_account_name=storagename, storage_account_key=storagekey, container_name=containername, blob_name=blobname)