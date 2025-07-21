import requests
from time import sleep
import os
import re
import json
import csv
import cv2
import shutil
from openpyxl import Workbook, load_workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


# Check for internet connection
def check_internet_connection():
    timer = 0
    for i in range(10):
        try:
            requests.get("http://www.google.com", timeout=5)
            return True
        except (requests.ConnectionError):
            timer += 5
            print(f"No internet connection. Waiting for {timer} seconds.")
            sleep(timer)
    else:
        print("Exceed max time limit to wait.")
        sys.exit(0)
        return False

# def check_visibility(d, elem):
#     connection = check_internet_connection()
#     if connection == False:
#         print("No internet connection.")
#         return False
#     wait_time = 2
#     data_visibility =  False
#     wait_count  = 1
#     while not data_visibility or wait_count>=5:
#         try:
#             print("Checking for element visibility...")
#             wait = WebDriverWait(d, wait_time)
#             # Check for web element availability
#             selenium_element = wait.until(EC.visibility_of_element_located(By.XPATH, elem))
#             if selenium_element:
#                 data_visibility = True
#                 print("Element visible. Proceeding further....")
#                 return selenium_element
#         except:
#             wait_time += 10
#             print("Element not visible yet. Wait for 10 more seconds...")
#     else:
#         print("Could not load the page. Exceeded max try limit.")
#         sys.exit(0)
#         return False

def check_visibility(d, elem):
    connection = check_internet_connection()
    if connection == False:
        print("No internet connection.")
        return False
    wait_time = 2
    data_visibility =  False
    wait_count  = 1
    while not data_visibility or wait_count>=5:
        try:
            print("Checking for element visibility...")
            wait = WebDriverWait(d, wait_time)
            # Check for web element availability
            selenium_element = wait.until(EC.visibility_of_element_located((By.XPATH, elem)))
            if selenium_element:
                data_visibility = True
                print("Element visible. Proceeding further....")
                return selenium_element
        except:
            wait_time += 10
            print("Element not visible yet. Wait for 10 more seconds...")
    else:
        print("Could not load the page. Exceeded max try limit.")
        return False

def extract_digits_regex(text):
    """Extracts only digits from a string using regex.

    Args:
        text: The string to extract digits from.

    Returns:
        A string containing only the digits from the input text.
    """

    # Use a regular expression to match one or more digits
    digits = re.findall(r"\d+", text)
    
    # Join the matched digits into a single string (optional)
    if digits:
        return int("".join(digits))
    else:
        return 0
  
# Function to separate the code
def separate_text(text):
    if isinstance(text, str):
        lines=text.splitlines()
        if len(lines)>0:
            return lines[-1].strip()
        else:
            return "Second line not found"
       
    else:
        return "Input is not a string."

def whats_my_ip():
    url = "https://api.ipify.org?format=text"
    response = requests.get(url)
    try:
        if response.status_code == 200:
            public_ip = response.text.strip()
            return public_ip
    except:
        check_internet_connection()
        if response.status_code == 200:
            public_ip = response.text.strip()
            return public_ip
        
def whats_my_address():
    url="https://ipinfo.io/json"
    response=requests.get(url)
    try: 
        if response.status_code == 200:
            data=response.json()
            city=data.get('city')
            region=data.get('region')
            country=data.get('country')
            address=(city+ ","+region + "," + country)
            return address

    except:
        check_internet_connection()
        if response.status_code == 200:
            data=response.json()
            city=data.get('city')
            region=data.get('region')
            country=data.get('country')
            address=(city+ ","+region + "," + country)
            return address


def create_folder(filepath):
    # Create the directory
    try:
        os.mkdir(filepath)
        print(f"Folder created successfully!: {filepath}")
    except FileExistsError:
        print(f"Folder already exists!: {filepath}")
        
def scroll_to_view(driver, element):
    # JavaScript scroll options
    driver.execute_script("""
        arguments[0].scrollIntoView({
            behavior: 'smooth',
            block: 'end',
            inline: 'end'
        });
    """, element)
def scroll_to_bottom1(driver):
    element = driver.find_element(By.TAG_NAME, 'body')
    while True:
        element.send_keys(Keys.PAGE_DOWN)
        sleep(5)

def scroll_to_bottom2(driver):
    try:
        sleep(5)
        previous_height = driver.execute_script('return document.body.scrollHeight')
        while True:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            sleep(5)
            new_height = driver.execute_script('return document.body.scrollHeight')
            if new_height == previous_height:
                break
            previous_height = new_height
        print("Successfully scrolled to the bottom of the page.")
    except:
        print("Could not scroll to the bottom.")
        pass
        
def clean_file_folder_name(filename):
    filename = filename.strip()
    filename = filename.replace("/", "_")
    filename = filename.replace(",", "_")
    filename = filename.replace(" ", "_")
    filename = filename.replace("-", "_")
    filename = filename.replace(":", "")
    return filename

def switch_to_new_window(driver, link_element):
    # Open a new tab and switch focus
    new_window = driver.switch_to.new_window()
    # Click the link (focus is already on the new tab)
    driver.get(link_element)


def append_dict_to_csv(data, file_path):
    # Extract keys from the dictionary
    fieldnames = list(data.keys())

    # Check if the file already exists
    try:
        with open(file_path, 'r') as file:
            # Check if the file has any data
            has_data = bool(file.read())
    except FileNotFoundError:
        has_data = False

    # Append data to the CSV file
    with open(file_path, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # If the file is empty, write header
        if not has_data:
            writer.writeheader()

        # Write data
        writer.writerow(data)



def create_file(filename, content=None):
    """Creates a new text file with optional content, checking for existence.

    Args:
        filename: The name of the file to create.

    Returns:
        True if the file was created successfully, False if it already exists.
    """

    if os.path.exists(filename):
        print(f"File already exists. Skipping creation.")
        return False
      # Add file creation logic
    wb = Workbook()
    wb.save(filename)
    fname = filename.split("/")[-1]
    print(f"File created successfully: {fname}")
    return True


def join_images_cv(image1_path, image2_path, output_path, crop_top_second=0, delete_originals=False):
  """
  Joins two images vertically with optional cropping and deletion.

  Args:
      image1_path: Path to the first image.
      image2_path: Path to the second image.
      output_path: Path to save the combined image.
      crop_top_second: Number of pixels to crop from the top of the second image (default: 0).
      delete_originals: Boolean flag indicating whether to delete the original images (default: False).
  """

  # Read images
  img1 = cv2.imread(image1_path)
  img2 = cv2.imread(image2_path)

  # Check if images have the same width (required for cv2.vconcat)
  if img1.shape[1] != img2.shape[1]:
      raise ValueError("Images must have the same width to join vertically with OpenCV.")

  # Crop top of second image (if specified)
  if crop_top_second > 0:
      height, width, channels = img2.shape
      crop_height = int(crop_top_second * (height / 300))  # Convert mm to pixels
      img2 = img2[crop_height:, :]  # Vertically slice to remove top pixels

  # Vertically stack images
  combined_img = cv2.vconcat([img1, img2])

  # Save combined image
  cv2.imwrite(output_path, combined_img)

  # Optionally delete original images
  if delete_originals:
      os.remove(image1_path)
      os.remove(image2_path)
      print(f"Deleted original images: {image1_path}, {image2_path}")
      


def rename_and_move_image(source_path, destination_path, new_filename):
  """
  Renames and moves an image file to a new location.

  Args:
      source_path: Path to the original image file.
      destination_path: Path to the destination folder.
      new_filename: The desired new filename for the image (without extension).

  Raises:
      ValueError: If the source file doesn't exist or the destination path is not a directory.
      OSError: If there are errors during the rename or move operation.
  """

  # Check if source file exists
  if not os.path.exists(source_path):
      raise ValueError(f"Source file not found: {source_path}")

  # Check if destination path is a directory
  if not os.path.isdir(destination_path):
      raise ValueError(f"Destination path is not a directory: {destination_path}")

  # Get the original filename and extension
  filename, extension = os.path.splitext(os.path.basename(source_path))

  # Construct the new full path with the desired filename and extension
  new_full_path = os.path.join(destination_path, f"{new_filename}{extension}")

  # Perform the rename and move operation using shutil.move
  try:
      shutil.move(source_path, new_full_path)
      print(f"Image renamed and moved successfully: {source_path} -> {new_full_path}")
  except OSError as error:
      raise OSError(f"Error renaming and moving image: {error}")

