import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwerty_123',
    database='mirrorverse'  # Replace 'your_database_name' with your actual database name
)

# Function to authenticate user
def authenticate(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM authenticate WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# Example usage
if __name__ == "__main__":
    input_username = input("Enter username: ")
    input_password = input("Enter password: ")

    if authenticate(input_username, input_password):
        print("Authentication successful!")
    else:
        print("Authentication failed. Invalid username or password.")
