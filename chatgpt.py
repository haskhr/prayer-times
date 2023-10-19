import time
import requests

# Function to read time from file
def read_time_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Function to send trigger to API endpoint
def send_trigger(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        print("Trigger sent successfully!")
    else:
        print(f"Failed to send trigger. Status code: {response.status_code}")

# Main function
def main():
    file_path = "time.txt"  # Path to the file containing the due time
    api_url = "https://api-v2.voicemonkey.io/trigger?token=3e11ab769d91d03c3f4910f9b4143f3d_122245bfd9a759e2697e6252d14adc09&device=abu-dhabi-azan"

    while True:
        due_time = read_time_from_file(file_path)
        current_time = time.strftime("%H:%M")

        if current_time == due_time:
            send_trigger(api_url)
        
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
