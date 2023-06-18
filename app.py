from flask import Flask
import psycopg2
import redis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def hello():
    conn = psycopg2.connect(
        database=os.environ.get('DATABASE_NAME'),
        user=os.environ.get('DATABASE_USER'),
        password=os.environ.get('DATABASE_PASSWORD'),
        host=os.environ.get('DATABASE_HOST'),
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    conn.close()
    return f"Database version: {db_version[0]}"

@app.route('/redis')
def redis_test():
    r = redis.Redis(
        host=os.environ.get('REDIS_HOST'),
        port=os.environ.get('REDIS_PORT'),
        db=0
    )
    r.set('key', 'Hello, Redis!')
    value = r.get('key').decode('utf-8')
    return f'Redis value: {value}'

if __name__ == '__main__':
    app.run()
