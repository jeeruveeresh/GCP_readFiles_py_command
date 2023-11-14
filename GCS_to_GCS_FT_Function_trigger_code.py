1st Method--------------------------------------------------------------------------------
import pandas as pd
from io import StringIO
from google.cloud import storage

def transform_csv(event, context):
    """Cloud Function triggered by GCS file upload."""
    input_bucket_name = "input_buc"
    output_bucket_name = "output_buc"
    input_file = event['name']
    output_file = f"output_{input_file}"

    # Download the file from GCS
    client = storage.Client()
    input_bucket = client.bucket(input_bucket_name)
    output_bucket = client.bucket(output_bucket_name)

    blob = input_bucket.blob(input_file)
    content = blob.download_as_text()

    # Read the CSV file directly into a Pandas DataFrame
    df = pd.read_csv(StringIO(content))

    # Apply transformations using Pandas
    df = df.rename(columns={'Emp Id': 'Emp_Id'})
    df = df.head(2000)  # Take only the first 2000 records
    df = df.dropna()

    # Convert the transformed DataFrame back to CSV format
    transformed_content = df.to_csv(index=False)

    # Upload the transformed content to the output bucket
    output_blob = output_bucket.blob(output_file)
    output_blob.upload_from_string(transformed_content)


2nd method---------------------------------------------------------------------------------
## this code is to keep in main.py in google cloud function for  triggering
from google.cloud import storage


def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    # Initialize Google Cloud Storage client
    client = storage.Client()
    # source_bucket_name = file['bucket']
    source_bucket = client.get_bucket('input_buc')
    filename = [filename.name for filename in
                list(source_bucket.list_blobs(prefix=""))]
    for i in range(0, len(filename)):
        source_blob = source_bucket.blob(filename[i])
        destination_bucket = client.get_bucket("output_buc")
        new_blob = source_bucket.copy_blob(
            source_blob, destination_bucket, filename[i])

## keep this package in requirements.txt
# --- >    google-cloud-storage
