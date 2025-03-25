import os
import argparse

def add_prefix(folder_path, prefix):
    """在指定目錄下的所有檔案名稱前新增前綴。"""
    try:
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                new_filename = prefix + filename
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                print(f"Renamed '{filename}' to '{new_filename}'")
        print("Done adding prefix.")
    except FileNotFoundError:
        print(f"Error: Directory '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_prefix(folder_path, prefix_length):
    """移除指定目錄下所有檔案名稱的前綴。"""
    try:
        for filename in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, filename)):
                new_filename = filename[prefix_length:]
                if new_filename != filename:
                    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                    print(f"Renamed '{filename}' to '{new_filename}'")
        print("Done removing prefix.")
    except FileNotFoundError:
        print(f"Error: Directory '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add or remove prefix from filenames in a directory.")
    parser.add_argument("action", choices=["add", "remove"], help="Action to perform: add or remove prefix.")
    parser.add_argument("--input", default=os.getcwd(), help="The input directory (default: current directory).")
    parser.add_argument("--prefix", help="Prefix to add (required for 'add' action).")
    parser.add_argument("--length", type=int, default=3, help="Length of prefix to remove (default: 3, required for 'remove' action).")
    args = parser.parse_args()

    if args.action == "add":
        if args.prefix:
            add_prefix(args.input, args.prefix)
        else:
            print("Error: --prefix is required for 'add' action.")
    elif args.action == "remove":
        remove_prefix(args.input, args.length)
