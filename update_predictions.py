import mysql.connector
import json

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="crypto_db"
)

cursor = conn.cursor(buffered=True)

with open('19oct.json', encoding='utf-8') as file:
    data = json.load(file)

messages = data['messages']
num_messages = len(messages)

for i in range(0, num_messages):
    reply = messages[i]
    # print(reply.get('reply_to_message_id'))
    if reply.get('reply_to_message_id'):
        coin_name = reply['text'].split('/')[0].strip('👉 ')
        cursor.execute("SELECT id FROM coin WHERE name = %s", (coin_name,))
        coin_id = cursor.fetchone()[0]
        print(coin_name)
        verified_at = reply['date_unixtime']
        predicted_at = str (int(verified_at) - 259200)
        cursor.execute("SELECT id FROM prediction WHERE coin_id = %s and predicted_at > %s and is_succeeded = 0;", (coin_id, predicted_at))
        prediction_id = cursor.fetchone()
        if prediction_id:
            prediction_id = prediction_id[0]
        print(prediction_id)
        if prediction_id:
            cursor.execute("UPDATE prediction SET is_succeeded = 1, verified_at = %s;", (verified_at,))


conn.commit()
cursor.close()
conn.close()

print("Predictions updated successfully!")

