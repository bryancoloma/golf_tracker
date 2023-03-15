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
        self.golfer_id = data['golfer_id']


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
                INSERT INTO courses (title,description,price,user_id)
                VALUES (%(title)s,%(description)s,%(price)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def update(cls,form_data):
        query = """
                UPDATE courses
                SET 
                title = %(title)s,
                description = %(description)s,
                price = %(price)s
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
    def validate_coures(form_data):
        is_valid = True

        if len(form_data['title']) < 2:
            flash("Title should be at least 2 characters long.")
            is_valid = False
        if len(form_data['description']) < 10:
            flash("Description should be at least 10 characters long.")
            is_valid = False
        if len(form_data['price']) < 1:
            flash("Price should be greater than 0.")
            is_valid = False
        return is_valid
