from google.cloud import storage

# TODO
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"

def create_bucket(name):
    storage_client = storage.Client()
    new_bucket = storage_client.create_bucket(name, location="us")
    return new_bucket

if __name__ == "__main__":
    bucket_name = "jj_bucket_ouah2"  # Replace with your desired bucket name
    new_bucket = create_bucket(bucket_name)
    print(f"Bucket created: {new_bucket.name}")

