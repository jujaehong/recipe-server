from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error

from mysql_connection import get_connection


class MylistResource(Resource) : 
    @jwt_required()
    def get(self) : 
        user_id = get_jwt_identity()

        try : 
            connection = get_connection()
            query = '''select r.*, u.username 
                    from recipe r
                    join user u
                        on r.user_id = u.id
                    where u.id = %s;'''
            record = (user_id, )
            cursor = connection.cursor(dictionary=True) 
            cursor.execute(query, record)

            result_list = cursor.fetchall()
            print(result_list)
            cursor.close()
            connection.close()

        except Error as e : 
            print(e)
            return {'result':'fail', 'error':str(e)}, 500 

        i = 0
        for row in result_list :
            result_list[i]['created_at']= row['created_at'].isoformat()
            result_list[i]['updated_at']= row['updated_at'].isoformat()
            i = i + 1
            
        return {'result':'success', 'item':result_list}
        