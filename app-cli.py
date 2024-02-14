import argparse
import os
import shutil
from script.classifier import FilesClassifier

def classify_files(input_folder, target_path):
    classifier = FilesClassifier()
    results = classifier.classify_folder(input_folder)

    total_files = len(results)
    print(f"Found {total_files} files for classification.")

    for index, result in enumerate(results, 1):
        file_name, class_label = result
        source_path = os.path.join(input_folder, file_name)
        destination_folder = os.path.join(target_path, class_label)

        destination_path = os.path.join(destination_folder, file_name)
        try:
            if not os.path.exists(os.path.dirname(destination_path)):
                print(f"Creating folder: {os.path.dirname(destination_path)}")
                os.makedirs(os.path.dirname(destination_path))

            shutil.move(source_path, destination_path)
            print(f"Moved {file_name} to {destination_path} ({index}/{total_files})")
        except FileNotFoundError:
            print(f"Error: {source_path} not found.")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

    print("Classification completed.")

def main():
    parser = argparse.ArgumentParser(description='File Classifier App')
    parser.add_argument('-i', '--input_folder', help='Path to the folder to be classified')
    parser.add_argument('-t', '--target_path', help='Path to the target folder for the classification results', required=True)

    args = parser.parse_args()

    input_folder = args.input_folder
    target_path = args.target_path

    if not os.path.exists(input_folder):
        print(f"Error: The specified input folder '{input_folder}' does not exist.")
        return

    if target_path is None:
        print("Error: The target folder path is not specified.")
        return

    if not os.path.exists(target_path):
        print(f"Error: The specified target folder '{target_path}' does not exist.")
        return

    confirm = input("Are you sure you want to proceed with classification? (yes/no): ").lower()
    if confirm != 'yes':
        print("Classification aborted.")
        return
    print("Starting classification...")
    classify_files(input_folder, target_path)

if __name__ == "__main__":
    main()
