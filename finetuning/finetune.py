import os
import time
from openai import AzureOpenAI

# === Step 1: Azure OpenAI Client Setup ===
client = AzureOpenAI(
    azure_endpoint="https://23june6219719860.openai.azure.com/",
    api_key="CdDWBOr8vEQ8lc0hz3NQbL8aNnXi3OLHn9U12n3YcOK9pMawQw0tJQQJ99BFACHYHv6XJ3w3AAAAACOGZYe3",
    api_version="2024-12-01-preview"
)

# === Step 2: File Names ===
training_file_name = 'training_set.jsonl'
validation_file_name = 'validate_set.jsonl'

# === Step 3: Upload Files ===
print("Uploading training file...")
training_response = client.files.create(file=open(training_file_name, "rb"), purpose="fine-tune")
training_file_id = training_response.id
print(f"Training file uploaded. ID: {training_file_id}")

print("Uploading validation file...")
validation_response = client.files.create(file=open(validation_file_name, "rb"), purpose="fine-tune")
validation_file_id = validation_response.id
print(f"Validation file uploaded. ID: {validation_file_id}")

# === Step 4: Wait for Files to be Processed ===
def wait_for_file_processing(file_id, timeout=120, interval=5):
    print(f"Waiting for file {file_id} to be processed...")
    elapsed = 0
    while elapsed < timeout:
        file_info = client.files.retrieve(file_id)
        status = file_info.status
        if status == "processed":
            print(f"File {file_id} is processed.")
            return
        elif status == "error":
            raise Exception(f"File {file_id} failed to process.")
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"File {file_id} did not process in time.")

wait_for_file_processing(training_file_id)
wait_for_file_processing(validation_file_id)

# === Step 5: Start Fine-Tuning Job ===
print("Starting fine-tuning job...")
response = client.fine_tuning.jobs.create(
    training_file=training_file_id,
    validation_file=validation_file_id,
    model="gpt-4o",  # Replace with the correct model name in your deployment if needed
    seed=105
)

# === Step 6: Output Job Details ===
print("\n✅ Fine-tuning job submitted successfully!")
print(f"Job ID: {response.id}")
print(f"Status: {response.status}")
print(response.model_dump_json(indent=2))
