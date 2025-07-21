import os
import pandas as pd
from seleniumbase import SB
import time

input_folder = r"C:\Users\manik\OneDrive\Desktop\selenium\Knob\Knob"   #folder containing input files 
output_folder = r"C:\Users\manik\OneDrive\Desktop\selenium\Knob\Knob\output"    #folder containing output files

# Get all Excel files in the input folder
excel_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

# def pop_up_close(sb):
#     try:
#         close_button = sb.wait_for_element(".selectRoleBoxContentHeaderClose", timeout=20)
#         close_button.click()
#         print("Popup closed successfully")
#     except Exception as e:
#         print(f"Popup not found or failed to close: {e}")

# Iterate through each Excel file in the folder
for excel_file in excel_files:
    excel_file_path = os.path.join(input_folder, excel_file)
    output_excel_file = os.path.join(output_folder, excel_file)

    print(f"Processing file: {excel_file_path}")

    # Read the Excel file and drop rows with empty 'part_number_input' values
    df = pd.read_excel(excel_file_path, skiprows=6)
    part_numbers = df['part_number_input'].dropna().unique().tolist()

    # Count duplicates in part numbers
    part_number_counts = df['part_number_input'].value_counts()
    duplicate_part_numbers = part_number_counts[part_number_counts > 1]

    # Calculate the sum of counts of duplicate part numbers (extra occurrences)
    duplicate_count_sum = (duplicate_part_numbers - 1).sum()

    # Print the number of unique and duplicate part numbers
    print(f"Number of unique part numbers in {excel_file}: {len(part_numbers)}")
    print(f"Number of duplicate part numbers in {excel_file}: {len(duplicate_part_numbers)}")
    print(f"Sum of duplicate part numbers (extra occurrences): {duplicate_count_sum}")

    # Check if the output Excel file already exists
    try:
        df_results = pd.read_excel(output_excel_file)
        # Extract the part numbers and clean them by removing the last character (e.g., '①')
        df_results['Cleaned Part Number'] = df_results['Part Number'].apply(lambda x: x[:-1] if isinstance(x, str) and x.endswith('①') else x)
        already_scraped_part_numbers = df_results['Cleaned Part Number'].tolist()

        cleaned_part_numbers = [p[:-1] if isinstance(p, str) and p.endswith('①') else p for p in part_numbers]
        part_numbers_to_scrape = [p for p in cleaned_part_numbers if p not in already_scraped_part_numbers]
        print(f"Part numbers to scrape (excluding already scraped): {len(part_numbers_to_scrape)}")

        # Filter out the part numbers with product name "500"
        incorrect_part_numbers = df_results[df_results['Product Name'] == "500"]['Cleaned Part Number'].tolist()
        part_numbers_to_scrape += [p for p in incorrect_part_numbers if p not in part_numbers_to_scrape]
        print(f"Part numbers to re-scrape (incorrect product name '500'): {len(incorrect_part_numbers)}")

    except FileNotFoundError:
        part_numbers_to_scrape = part_numbers
        print(f"Output file not found. Scraping all {len(part_numbers_to_scrape)} part numbers.")

    # List to store the results
    results = []

    # Initialize SeleniumBase for the browser automation
    with SB(uc=True, incognito=True, maximize=True, locale_code="en", skip_js_waits=True, headless=False) as sb:
        url = 'https://xyz.com/'
        sb.driver.get(url)
        
        # pop_up_close(sb)
        try:
            close_button = sb.wait_for_element(".selectRoleBoxContentHeaderClose", timeout=20)
            close_button.click()
            print("Popup closed successfully")
        except Exception as e:
            print(f"Popup not found or failed to close: {e}")

        # Wait for the search bar to become visible and interact with it
        try:
            search_bar = sb.wait_for_element("//div[@class='searchInput el-input el-input-group el-input-group--append el-input--prefix']", timeout=10)
            search_bar.click()
            print("Found and clicked the search bar")
        except Exception as e:
            print(f"Error interacting with the search bar: {e}")

        # Iterate over each part number that needs to be scraped
        for part_number in part_numbers_to_scrape:
            try:
                # Clean the part number if necessary
                cleaned_part_number = part_number[:-1] if part_number.endswith('①') else part_number
                print(f"Searching for: {cleaned_part_number}")

                # Clear the search bar and input the cleaned part number
                search_input = sb.wait_for_element("//input[@class='el-input__inner']", timeout=10)
                search_input.clear()
                search_input.send_keys(cleaned_part_number)
                time.sleep(5)

                # Click the search button
                search_button = sb.wait_for_element("//div[@class='el-input-group__append']", timeout=15)
                search_button.click()

                #modification for changed ui

                try:
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                    time.sleep(1)
                    sb.find_element("//button[@class='el-button el-button--text el-button--mini']",timeout=15).click()
                    time.sleep(1)
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                    sb.find_element("//button[@class='el-button el-button--text el-button--mini']",timeout=15).click()
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                    sb.wait_for_element("//button[@class='el-button el-button--primary']",timeout=15).click()
                

                except:
                    pass

                

                try:
                    sb.find_element("//button[@class='el-button el-button--text el-button--mini']",timeout=15).click()
                    time.sleep(1)

                except:
                    continue


                

                # pop_up_close(sb)
                sb.find_element("//div[@class='topTitle']//p[@class='productNameStyle']", timeout=10)
                time.sleep(5)

                # Click the additional button with class 'el-button el-button--default'
                try:
                    default_button = sb.wait_for_element("//button[@class='el-button el-button--default']", timeout=10)
                    default_button.click()
                except Exception as e:
                    print(f"Failed to click the default button: {e}")

                # Handle potential pop-ups during the scraping process
                try:
                    close_button = sb.wait_for_element(".selectRoleBoxContentHeaderClose", timeout=5)
                    close_button.click()
                    print(f"Popup appeared again and was closed for part number: {cleaned_part_number}")

                  
                    
                except Exception:
                    pass

                time.sleep(6)

                # Extract the product name
                product_name = sb.find_element("//div[@class='topTitle']//p[@class='productNameStyle']").text()
                print(f"Found product name for {cleaned_part_number}: {product_name}")

                # Append the cleaned part number and product name to the results list
                results.append({"Part Number": cleaned_part_number, "Product Name": product_name})

                # Check if the output Excel file exists and append the results
                if not pd.io.common.file_exists(output_excel_file):
                    df_results = pd.DataFrame(results)
                    df_results.to_excel(output_excel_file, index=False)
                else:
                    df_existing = pd.read_excel(output_excel_file)
                    df_new_results = pd.DataFrame(results)
                    df_all = pd.concat([df_existing, df_new_results], ignore_index=True).drop_duplicates(subset=['Part Number'])
                    df_all.to_excel(output_excel_file, index=False)

                time.sleep(2)  # Adjust sleep time

            except Exception as e:
                print(f"Error occurred while searching for {part_number}: {e}")

    print(f"Scraping complete for file: {excel_file}")

    
