import os
import tarfile

def extract_tar_gz(tar_file_path: str, destination_path: str) -> bool:
    """Extract the content of a .tar.gz file to a destination directory."""
    try:
        os.makedirs(destination_path, exist_ok=True)

        with tarfile.open(tar_file_path, "r:gz") as tar:
            print(f"Extracting files from file: {tar_file_path}")
            tar.extractall(path=destination_path)
            print(f"Extraction completed to directory: {destination_path}")
            return True
    except tarfile.TarError as e:
        print(f"Error opening or extracting the .tar.gz file: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: File not found in {tar_file_path}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    tar_file_path = "data/equipment_failure_sensors.tar.gz"
    destination_path = "data/extracted"

    if extract_tar_gz(tar_file_path, destination_path):
        pass


if __name__ == "__main__":
    main()
