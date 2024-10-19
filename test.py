import mysql.connector
import json

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="crypto_db"
)

cursor = conn.cursor()

# Load the JSON file
with open('real_data.json', encoding='utf-8') as file:
    data = json.load(file)

# Function to get or insert a coin and return the coin_id
def get_or_insert_coin(coin_name):
    # Check if the coin already exists
    cursor.execute("SELECT id FROM coin WHERE name = %s", (coin_name,))
    result = cursor.fetchone()

    if result:
        # If coin exists, return its id
        return result[0]
    else:
        # If coin does not exist, insert it and return the new id
        cursor.execute("INSERT INTO coin (name) VALUES (%s)", (coin_name,))
        return cursor.lastrowid

# Process messages and filter for predictions and verifications
messages = data['messages']
num_messages = len(messages)
# num_messages = 100


for i in range(num_messages):
    message = messages[i]
    # Check if the message is a prediction (type 4: prediction message)
    # if 'text' in message and isinstance(message['text'], list):
    if 'text' in message and message["text_entities"]:
        # Ensure this is a prediction with a coin name (starts with '🪙')
        if "text_entities" in message and message["text_entities"][0]["text"][0] == '🪙':
            # coin_name = message['text'][0].split('/')[0].strip('🪙 ')
            coin_name = message["text_entities"][0]["text"].split('/')[0].strip('🪙 ')
            # Get or insert the coin, and retrieve its coin_id
            coin_id = get_or_insert_coin(coin_name)

            # try:
            # # Determine prediction type (long or short)
            #     if isinstance(message['text'], list):
            #         prediction_type = 'long' if 'long' in message['text'][2].lower() else 'short'
            #     else:
            #         prediction_type = 'long' if 'long' in message['text'].lower() else 'short'
            # except:
            #     print(message['id'])
            #     print(message['text'][2])
            #     raise Exception("Sorry")
            # Insert prediction data
            prediction_type = 'long'
            cursor.execute("""
                INSERT INTO Prediction (coin_id, type, predicted_at)
                VALUES (%s, %s, %s)
            """, (coin_id, prediction_type, message['date_unixtime']))
            
            prediction_id = cursor.lastrowid  # Get the last inserted ID for Prediction

            # Search for verification messages starting from the next index
            for j in range(i + 1, num_messages):
                reply = messages[j]
                
                # Check if the reply message is a verification (reply to the prediction message)
                if reply.get('reply_to_message_id') == message['id']:
                    verified_at = reply['date_unixtime']
                    
                    # Update the Prediction table with verification time
                    cursor.execute("""
                        UPDATE Prediction 
                        SET verified_at = %s, is_succeeded = 1
                        WHERE id = %s
                    """, (verified_at, prediction_id))
                    break  # Exit loop once verification is found

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()

print("Data inserted into the database successfully!")
