import os
import csv
import time

ile_plikow=0
ile_plikow_skipped=0
ile_plikow_powielono=0
def extract_information(file_path):
    # Modify this function to extract the desired information from the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        #print(content)

        # Example: Extracting lines containing 'keyword'
        extracted_data = [line.strip() for line in content.split('\n')
                          if 'Detected Time:' in line
                          or 'Job ID:' in line
                          or 'Client:' in line
                          or 'Agent Type:' in line
                          or 'Backup Set:' in line
                          or 'Subclient:' in line
                          or 'Failure Reason:' in line
                          ]
        print(extracted_data)
    return extracted_data

def process_folder(input_folder, output_csv):
    global ile_plikow, ile_plikow_skipped, ile_plikow_powielono
    # Ensure the output CSV file is created or overwritten
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Write header if needed
        #csv_writer.writerow(['FileName', 'ExtractedData'])  # Customize the header as needed

        # List to store unique first items
        unique_first_items = []

        # auto output
        auto_output = []

        # Iterate through files in the input folde
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                print(file_path)
                extracted_data = extract_information(file_path)

                #print(extracted_data)
                #extracted_data = extracted_data[1:]
                extracted_data = [item for item in extracted_data if not item.startswith("Temat:")]
                # Skip if first item is the same for a given filename

                #print(extracted_data)
                #print(type(extracted_data))

                # Remove everything before ":" in each element
                extracted_data = [item.split(':', 1)[-1].strip() for item in extracted_data]

                # Get the first item, or None if the list is empty
                first_item = extracted_data[1] if extracted_data else None
                # Append to the list only if the first item is different
                if first_item not in unique_first_items:
                    unique_first_items.append(first_item)
                    print(extracted_data)

                    # Write filename and extracted data to the CSV file
                    #csv_writer.writerow([filename, ', '.join(extracted_data)])
                    print(type(extracted_data))
                    print(extracted_data)
                    #if "The job will not run because activity is disabled." in extracted_data[-1]:
                    #    print("disabled")
                    #    auto_output = ["MD -> activity disabled"]
                    csv_writer.writerow(extracted_data)
                    # Remove the processed .txt file
                    try:
                        os.rename(file_path,os.path.join(input_folder+"/done/", filename))
                    except FileExistsError:
                        os.remove(os.path.join(input_folder+"/done/", filename))
                        ile_plikow_powielono = ile_plikow_powielono + 1
                        os.rename(file_path,os.path.join(input_folder+"/done/", filename))
                    ile_plikow=ile_plikow+1
                else:
                    try:
                        ile_plikow_skipped=ile_plikow_skipped+1
                        os.rename(file_path,os.path.join(input_folder+"/not_used/", filename))
                    except FileExistsError:
                        os.remove(os.path.join(input_folder+"/done/", filename))
                        ile_plikow_powielono = ile_plikow_powielono + 1
                        os.rename(file_path,os.path.join(input_folder+"/done/", filename))


# Specify the input folder containing text files and the output CSV file
input_folder_path = "C:/Users/mdziezok/OneDrive - COIG S.A/Pulpit/mail"
output_csv_path = "C:/Users/mdziezok/OneDrive - COIG S.A/Pulpit/mail/file"+str(time.time())+".csv"

# Process the folder and create the CSV file
process_folder(input_folder_path, output_csv_path)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Zrobiono '+str(ile_plikow)+" plików")
    print('Ominięto ' + str(ile_plikow_skipped) + " plików")
    print('Powielono ' + str(ile_plikow_powielono) + " plików")
