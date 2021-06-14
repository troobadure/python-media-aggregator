import psycopg2
from config import config
import mock

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
    profile_id          serial  primary key,
    user_id             int,
    profile_type        text,
    profile_name        text,
    
    foreign key(user_id) references users(user_id)
    );''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS criterias (
    criteria_id         serial primary key,
    profile_id          int,
    criteria_type       text,
    criteria_value      int,
    
    foreign key(profile_id) references profiles(profile_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS posts (
    post_id             text    primary key,
    profile_type        text,
    profile_name        text,
    publication_date    text,
    download_date       text,
    filename            text
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS seen_posts (
    seen_post_id        int primary key,
    user_id             int,
    post_id             text,
    view_date           text,
    
    foreign key(user_id) references users(user_id),
    foreign key(post_id) references posts(post_id)
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
    path                text primary key,
    post_id             text,
    
    foreign key(post_id) references posts(post_id)
    )
    ''')
    
    c.execute('''INSERT INTO users (user_id, user_name, curr_state) VALUES
                (402027899, \'Vlood\', \'main_menu\')''')

    conn.commit()


def insert_user(user_id, user_name, curr_state, registration_date, last_activity):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (user_id, user_name, curr_state, last_activity, registration_date) VALUES (%s, %s, %s, %s, %s)',
            (user_id, user_name, curr_state, last_activity, registration_date)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        print('User already exists')


def update_state(user_id, user_name, curr_state, last_activity):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE users SET user_name = %s, curr_state = %s, last_activity = %s WHERE user_id = %s',
        (user_name, curr_state, last_activity, user_id)
    )
    conn.commit()

    print(user_name + ' at ' + curr_state)


def get_state(user_id: str):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'SELECT curr_state FROM users WHERE user_id = %s',
            (user_id,)
        )

        return c.fetchone()[0]

    except TypeError:
        return 'NoneType error on state fetch'


def insert_profile(user_id, profile_type, profile_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO profiles (user_id, profile_type, profile_name) VALUES (%s, %s, %s)',
        (user_id, profile_type, profile_name)
    )
    conn.commit()


def get_profile_id(user_id, profile_type, profile_name):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'SELECT profile_id FROM profiles WHERE user_id = %s and profile_type = %s and profile_name = %s',
            (user_id, profile_type, profile_name)
        )
        
        return c.fetchone()[0]

    except TypeError:
        return 'NoneType error on profile get'


def insert_criteria(profile_id, criteria_type, criteria_value):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO criterias (profile_id, criteria_type, criteria_value) VALUES (%s, %s, %s)',
        (profile_id, criteria_type, criteria_value)
    )
    conn.commit()


def get_profiles(user_id):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'SELECT (profile_id, profile_type, profile_name) FROM profiles WHERE user_id = %s',
            (user_id, )
        )
        
        res = c.fetchall()
        def make_profile(raw_record):
            record = raw_record[0].split('(')[1].split(')')[0].split(',')
            profile = mock.Mock()
            profile.profile_id = record[0]
            profile.profile_type = record[1]
            profile.profile_name = record[2]
            return profile

        profiles = map(make_profile, res)
        return profiles

    except TypeError:
        return []


def get_criteria_value(profile_id, criteria_type):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'SELECT criteria_value FROM criterias WHERE profile_id = %s and criteria_type = %s ORDER BY criteria_value',
            (profile_id, criteria_type)
        )
        
        return c.fetchone()[0]

    except TypeError:
        return 0


def insert_post(post_id, profile_type, profile_name, publication_date, download_date, filename):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO posts (post_id, profile_type, profile_name, publication_date, download_date, filename) VALUES (%s, %s, %s, %s, %s, %s)',
            (post_id, profile_type, profile_name, publication_date, download_date, filename)
        )
        conn.commit()

    except psycopg2.errors.UniqueViolation:
        print('Post already exists')
