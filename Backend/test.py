from werkzeug.security import generate_password_hash, check_password_hash

# Create a password hash
password = "admin123"
hashed = generate_password_hash(password)

# Print the hashed password
print("Hashed password:", hashed)