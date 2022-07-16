from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


class Tvshow:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = data['posted_by']
        self.posted_by_name = data['posted_by_name']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO tvshows (title, network, release_date, description, posted_by, created_at, updated_at ) VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s,%(posted_by)s, NOW() , NOW() );"
        return connectToMySQL('tvshows_schema').query_db( query, data )

    @classmethod
    def get_all(cls):
        query = """SELECT tvshows.id, title, network, release_date, description, posted_by, tvshows.created_at, tvshows.updated_at, users.first_name as posted_by_name
        from tvshows
        join users on posted_by = users.id;
                """
        results = connectToMySQL('tvshows_schema').query_db(query)
        tvshows = []
        for tvshow in results:
            tvshows.append(cls(tvshow))
        return tvshows

    @classmethod
    def delete(cls, id ):
        query = "DELETE FROM tvshows WHERE id ="+id+";"
        return connectToMySQL('tvshows_schema').query_db( query)

    @classmethod
    def getonebyid(cls, id ):
        query = "SELECT tvshows.id, title, network, description,release_date, posted_by, tvshows.created_at, tvshows.updated_at, concat(first_name, ' ', last_name) as owner_name from tvshows join users on posted_by = users.id WHERE tvshows.id ="+id+";"
        
        tvshow = connectToMySQL('tvshows_schema').query_db( query)
        print(tvshow)
        return tvshow

    @classmethod
    def update_tvshow(cls,data, id):
        query = "UPDATE tvshows SET title=%(title)s, network=%(network)s, description=%(description)s, release_date=%(release_date)s,tvshows.updated_at = NOW() WHERE tvshows.id ="+id+";"
        return connectToMySQL('tvshows_schema').query_db( query, data)

    @staticmethod
    def validate_tvshow(tvshow):

        print(tvshow)

        is_valid = True

        if len(tvshow['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False

        if len(tvshow['network']) < 3:
            flash("Network must be at least 3 characters.")
            is_valid = False

        if len(tvshow['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if tvshow['release_date'] == '':
            flash("Date field is required")
            is_valid = False

        return is_valid

    @classmethod
    def save_like(cls, data ):
        query = "INSERT INTO likes (user_likes_id, show_liked_id, created_at, updated_at) VALUES (%(user_likes_id)s,%(show_liked_id)s, NOW() , NOW() );"
        return connectToMySQL('tvshows_schema').query_db( query, data )

    @classmethod
    def shows_liked_by_id(cls, id ):
        query = "SELECT show_liked_id FROM likes WHERE user_likes_id="+str(id)+";"
        result = connectToMySQL('tvshows_schema').query_db( query )
        shows_id=[]
        for dic in result:
            shows_id.append(dic['show_liked_id'])
        print(shows_id, "///////////")
        return shows_id

    @classmethod
    def del_like(cls, data ):
        query = "DELETE FROM likes WHERE user_likes_id = %(user_likes_id)s AND show_liked_id = %(show_liked_id)s;"
        return connectToMySQL('tvshows_schema').query_db( query, data )

    @classmethod
    def likes_count(cls, id ):
        query = "SELECT COUNT(user_likes_id) as count FROM likes WHERE show_liked_id ="+id+";"
        return connectToMySQL('tvshows_schema').query_db( query)