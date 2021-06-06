import psycopg2
from config import config

def get_connection():
    db = psycopg2.connect(config.DATABASE_STRING)
    return db


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''DROP TABLE IF EXISTS users CASCADE ;
                 DROP TABLE IF EXISTS profiles CASCADE ;
                 DROP TABLE IF EXISTS criterias CASCADE ;
                 DROP TABLE IF EXISTS posts CASCADE ;
                 DROP TABLE IF EXISTS seen_posts CASCADE ;
                 DROP TABLE IF EXISTS files CASCADE ;
              ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
    user_id             int  primary key,
    user_name           text,
    curr_state          text,
    registration_date   text,
    last_activity       text
     );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
    profile_id          int  primary key,
    user_id             int,
    profile_type        text,
    social_id           text,
    
    foreign key(user_id) references users(user_id)
    );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS criterias (
    criteria_id         int primary key,
    user_id             int,
    profile_id          int,
    criteria_type       text,
    criteria_value      int,
    
    foreign key(user_id) references users(user_id),
    foreign key(profile_id) references profiles(profile_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
    post_id             text primary key,
    user_id             int,
    profile_id          int,

    foreign key(user_id) references users(user_id),
    foreign key(profile_id) references profiles(profile_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS seen_posts (
    seen_post_id        int primary key,
    user_id             int,
    profile_id          int,
    post_id             text,
    
    foreign key(user_id) references users(user_id),
    foreign key(profile_id) references profiles(profile_id),
    foreign key(post_id) references posts(post_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
    post_id             text,
    profile_id          int,
    path                text primary key,
    
    foreign key(post_id) references posts(post_id),
    foreign key(profile_id) references profiles(profile_id)
    )
    ''')

    conn.commit()


def register_user(user_id, user_name: str, curr_state: str, registration_date: str, last_activity: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO users (user_id, user_name, curr_state, last_activity, registration_date) VALUES (%s, %s, %s, %s, %s)',
        (user_id, user_name, curr_state, last_activity, registration_date,)
    )
    conn.commit()


def update_state(user_id, user_name, curr_state, last_activity):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET user_name = %s, curr_state = %s, last_activity = %s WHERE user_id = %s',
        (user_id, user_name, curr_state, last_activity)
    )
    conn.commit()


def get_state(user_id: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            'SELECT curr_state FROM users WHERE user_id = %s',
            (user_id,)
        )

        q = c.fetchone()
        return q[0]

    except TypeError:
        return 'NoneType error on state fetch'