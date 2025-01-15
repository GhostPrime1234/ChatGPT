import csv
import winreg
import subprocess


def list_installed_software():
    install_software_list = []
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")

        install_software_list = []
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                software_key_name = winreg.EnumKey(key, i)
                software_key = winreg.OpenKey(key, software_key_name)
                try:
                    software_name = winreg.QueryValueEx(software_key, "DisplayName")[0]
                    install_software_list.append(software_name)
                except FileNotFoundError:
                    # Handle the case where "DisplayName" is not present
                    pass
                except Exception as e:
                    # Log unexpected errors while accessing key values
                    print(f"Error reading key {software_key_name}: {e}")
            except FileNotFoundError:
                # Handle the case where a key cannot be accessed
                pass
            except Exception as e:
                # Log unexpected errors while iterating keys
                print(f"Error accessing key {i}: {e}")

    except Exception as e:
        # Log unexpected errors while accessing the registry
        print(f"Error accessing registry: {e}")

    return sorted(set(install_software_list))


def save_to_csv(save_software_list, filename="database/installed_software.csv"):
    try:
        with open(f"{filename}", "w", newline="", encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Software Name"])  # Write header
            for software in save_software_list:
                writer.writerow([software])
        print(f"Data saved to {filename}")
    except Exception as error:
        print(f"Error saving data to database: {error}")


def read_software_from_csv(m_filename="database/installed_software.csv"):
    m_software_list = []
    try:
        with open(m_filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                m_software_list.append(row[0])
    except Exception as e:
        print(f"Error reading data from CSV: {e}")
    return m_software_list


def install_software(software_name):
    try:
        print(f"Installing {software_name} using winget...")
        # Use winget to install the software
        command = ["winget", "install", "--id", software_name, "--silent"]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"{software_name} installed successfully.")
        else:
            print(f"Failed to install {software_name}. Error: {result.stderr}")
            
    except Exception as e:
        print(f"Error installing {software_name}: {e}")


def check_and_install_missing_software():
    # Read list of installed software
    installed_software = list_installed_software()
    # Read list of software from CSV
    csv_software_list = read_software_from_csv()

    # Create sets for comparison
    installed_set = set(installed_software)
    csv_set = set(csv_software_list)

    # Determine missing software
    missing_software = csv_set - installed_set

    if missing_software:
        print("Missing software to install:")
        for software in missing_software:
            print(f" - {software}")
            install_software(software)
    else:
        print("All software from CSV is already installed.")


if __name__ == "__main__":
    software_list = list_installed_software()
    save_to_csv(software_list)
    check_and_install_missing_software()
