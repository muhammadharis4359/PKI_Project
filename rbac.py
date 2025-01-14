# Sample roles and permissions
roles = {
    "Admin": ["revoke_certificates", "add_device", "monitor_devices"],
    "User": ["monitor_devices"],
    "Device": ["send_data", "receive_commands"]
}

# Function to check access
def check_access(role, action):
    """ Check if the given role is allowed to perform the action """
    if action in roles.get(role, []):
        return True
    return False
