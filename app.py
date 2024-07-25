from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import pandas as pd
import re

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chatdb"
)

# Load dataset from CSV
df = pd.read_csv('offensive_language_dataset.csv')

# Extract curse words from the dataset
curse_sentences = df['curseword'].tolist()

# Create a set of curse words for quick lookup
curse_words = set()
for sentence in curse_sentences:
    # Tokenize the sentence and add each word to the curse words set
    words = re.findall(r'\b\w+\b', sentence)
    curse_words.update(word.lower() for word in words)

# Function to replace curse words with * of the same length
def replace_with_stars(word):
    return '*' * len(word)

# Function to filter a sentence
def filter_sentence(sentence):
    # Tokenize and process each word
    def process_word(word):
        # Check if the word is in the curse words list
        if word.lower() in curse_words:
            return replace_with_stars(word)
        return word

    # Process the sentence and reconstruct it
    filtered_sentence = re.sub(r'\b\w+\b', lambda match: process_word(match.group(0)), sentence)
    return filtered_sentence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    username = request.form['username']
    message = request.form['message']

    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (username, message) VALUES (%s, %s)", (username, message))
    db.commit()
    cursor.close()

    return redirect(url_for('index'))

@app.route('/get_messages', methods=['GET'])
def get_messages():
    cursor = db.cursor()
    cursor.execute("SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    cursor.close()

    # Filter each message
    filtered_messages = [
        (username, filter_sentence(message), timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        for username, message, timestamp in messages
    ]
    
    return jsonify(filtered_messages)

if __name__ == '__main__':
    app.run(debug=True,port=7148)
