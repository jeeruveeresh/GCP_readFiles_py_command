
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