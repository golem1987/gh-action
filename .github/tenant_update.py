import re
import yaml
import sys

# Function to read realms from YAML file
def read_realms(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data.get('realms', [])

def is_valid_realm(realm):
    pattern = re.compile(r'^(gv|fp)\d{3}[a-z]{3}$')
    return bool(pattern.match(realm))

def add_realm(realms, realm):
    if is_valid_realm(realm):
        if realm not in realms:
            realms.append(realm)
            print(f"Realm '{realm}' added successfully.")
        else:
            print(f"Realm '{realm}' is already in the list.")
            sys.exit(1)
    else:
        print(f"Realm '{realm}' is not in the correct format.")
        sys.exit(1)
    return realms

def save_realms(file_path, realms):
    with open(file_path, 'w') as file:
        yaml.dump({"realms": realms}, file)

# Main function
def main():
    if len(sys.argv) != 2:
        print("Expecting one argument only")
        sys.exit(1)
    
    file_path = "realms.yaml"
    realms = read_realms(file_path)
    realm_to_add = sys.argv[1]
    
    realms = add_realm(realms, realm_to_add)
    
    save_realms(file_path, realms)
    print("Realm added to list")

if __name__ == "__main__":
    main()