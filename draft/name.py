import os
import xml.etree.ElementTree as ET


def extract_unique_names_from_xml(directory_path):
    unique_names = set()  # Use a set to avoid duplicates

    for filename in os.listdir(directory_path):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory_path, filename)
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Loop through each 'object' element and find 'name' tags
                for obj in root.findall('object'):
                    name = obj.find('name').text
                    unique_names.add(name)
            except ET.ParseError as e:
                print(f"Error parsing {filename}: {e}")

    return unique_names


# Replace 'your_directory_path' with the path to your XML files
directory_path = r'C:\Users\chloe\OneDrive\桌面\Output\Output'
unique_names = extract_unique_names_from_xml(directory_path)

print("Unique names found in the XML files:")
for name in unique_names:
    print(name)
