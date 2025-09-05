import requests  # A simple HTTP library for Python
import os  # Provides a way of using operating system dependent functionality
import time  # Used for adding delays (if needed)
import hashlib  # Provides a way to create hash objects (Used for duplicate detection)
from urllib.parse import urlparse  # Extracts filenames from URLs

def fetch_image(url, downloaded_hashes):
    """Fetch a single image from the given URL and save it locally"""
    try:
        #Send a GET request to the URL with a 15-second timeout
        #stream=True means the content is fetched in chunks, useful for large files
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5, stream=True)

        response.raise_for_status() #Raise an error if HTTP status is not 200 (Okay)
        
        #Check the Content-Type header to ensure we are downloading an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"Skipping: URL does not point to an image ({content_type})")
            return None #Exit function if the URL is not an image
        
        #Extract filename from the URL path
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        #If no filename exists in the URL, give it a default name
        if not filename:
         filename = f"unsplash_{int(time.time())}.jpg"
         
        # Ensure filename has an extension (default .jpg)
        if not os.path.splitext(filename)[1]:
         filename += ".jpg"
        
        #Build the full path where the file will be saved inside "Fetched_Images"
        filepath = os.path.join("Fetched_Images", filename)
        
        #Compute a hash of the image content to check for duplicates
        file_hash = hashlib.md5(response.content).hexdigest()
        if file_hash in downloaded_hashes:
            print(f"Duplicate Skipped: ({filename})")
            return None  #Skip saving if the image is already downloaded
        downloaded_hashes.add(file_hash) #Add hash to the set to track downloads
        
        #Save the images in binary mode ("wb")
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
                
        #Success Message
        print(f"Successfully fetched: {filename}")
        print(f"Image saved to {filepath}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        #Handles network-related errors 
        print(f"Connection error for {url}: {e}")
    except Exception as e:
        #Catched any other unexpected errors
        print(f"An error occured for {url}: {e}")
    return None

def main():
    """Main function to handle user input and multiple downloads"""
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images for the web\n")
    
    #Create "Fetched_Images" directory if it doesn't already exist
    os.makedirs("Fetched_Images", exist_ok=True)
    
    #Ask the user to input one or more URLs (comma-separated)
    urls = input("Please enter image URLs (comma-separated): ").split(",")
    
    #A set to store hashes of downloaded images (for duplicates)
    downloaded_hashes = set()
    
    #Loop through each URL provided by the user 
    for url in urls:
        url = url.strip() #Remove extra spaces
        if url:           #Only process non-empty URLs
            fetch_image(url, downloaded_hashes) 
            
    #Closing message
    print("\nConnection strengthened. Community enriched.")
    
#Run the program only if this file is executed directly(not as a module)
if __name__ =="__main__":
        main()
      
    
    