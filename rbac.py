# Sample roles and permissions
roles = {
    "Admin": ["revoke_certificates", "add_device", "monitor_devices"],
    "User": ["monitor_devices"],
    "Device": ["send_data", "receive_commands"]
}

# Function to check access
def check_access(role, action):
    if action in roles.get(role, []):
        return True
    return False

# Test RBAC
if __name__ == "__main__":
    role = input("Enter your role (Admin/User/Device): ")
    action = input("Enter the action you want to perform: ")
    
    if check_access(role, action):
        print(f"Access granted for {role} to perform '{action}'.")
    else:
        print(f"Access denied for {role} to perform '{action}'.")
