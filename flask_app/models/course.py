
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "valley_golf"

class Course:
    def __init__(self, data):
        self.id = data['id']
        self.score = data['score']
        self.golf_course = data['golf_course']
        self.total_putts = data['total_putts']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM courses
                JOIN users on courses.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        courses = []
        for row in results:
            this_course = cls(row)
            user_data = {
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }

            this_course.creator = user.User(user_data)
            courses.append(this_course)
        return courses
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * 
                FROM courses
                JOIN users on courses.user_id = users.id
                WHERE courses.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        if not result:
            return False

        result = result[0]
        this_course = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_course.creator = user.User(user_data)
        return this_course

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO courses (score,golf_course,notes,user_id)
                VALUES (%(score)s,%(golf_course)s,%(notes)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE courses
                SET 
                score = %(score)s,
                golf_course = %(golf_course)s,
                notes = %(notes)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def destroy(cls,data):
        query = """
                DELETE FROM courses
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query,data)
    
    @staticmethod
    def validate_course(form_data):
        is_valid = True

        if len(form_data['score']) < 2:
            flash("score should be at least 2 characters long.")
            is_valid = False
        if len(form_data['golf_course']) < 5:
            flash("Golf Course name should be at least 5 characters long.")
            is_valid = False
        if len(form_data['notes']) < 1:
            flash("Notes should be greater than 0.")
            is_valid = False
        return is_valid
