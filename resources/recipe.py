from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from flask import request
# api 동작하게 만드는 메소드
import mysql.connector
from mysql.connector import Error

from mysql_connection import get_connection



# API 동작하는 코드를 만들기 위해서는 
# class를 만들어야 한다. 

# class란 ???? 비슷한 데이터끼리 모아놓은 것 (테이블이랑 비슷한 개념)
# 클래스는 변수와 함수로 구성된 묶음 
# 테이블과 다른 점 : 함수가 있다. 


# API를 만들기 위해서는 flask_restful 라이브러리의 Resource 클래스를 상속받아서 만들어야 한다. 파이썬에서 상속은 괄호! 
# 먼저 만들어보다가 추상적인 개념 설명하겠슴니당.
# class 클래스이름(상속받는애): 변수+함수
# 프레임워크로 제공되는 함수 def post():
 


class MyRecipeListResource(Resource):
    @jwt_required()
    def get(self) : 
        user_id = get_jwt_identity() # 복호화해서 갖다놓는다. 
        try:
            connection = get_connection()
            query = '''select * from recipe
                    where user_id = %s;'''
            record = ( user_id, )
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            result_list = cursor.fetchall()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return{'result':'fail', 'error':str(e)}, 400
        
        print(result_list)

        # 가공이 필요하면 가공한다. 
        i = 0
        for row in result_list :
            result_list[i]['created_at']= row['created_at'].isoformat()
            result_list[i]['updated_at']= row['updated_at'].isoformat()
            i = i + 1

        return {'result':'success', 'count':len(result_list), 'items':result_list}



class RecipePublishResource(Resource) :
    @jwt_required() 
    def put(self, recipe_id) : 
        # 1. 클라이언트로부터 데이터 받아온다.
        # API 명세서를 본다. 
        user_id = get_jwt_identity()

        # 2. DB처리한다. 
        try : 
            connection = get_connection()
            query = '''update recipe 
                    set is_publish = 1
                    where id = %s and user_id = %s;'''
            record = ( recipe_id, user_id )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}, 500
        
        return {'result':'success'}
    
    @jwt_required() 
    def delete(self, recipe_id) : 
        # 1. 클라이언트로부터 데이터 받아온다.
        # API 명세서를 본다. 
        user_id = get_jwt_identity()

        # 2. DB처리한다. 
        try : 
            connection = get_connection()
            query = '''update recipe 
                    set is_publish = 0
                    where id = %s and user_id = %s;'''
            record = ( recipe_id, user_id )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}, 500
        
        return {'result':'success'}


# 경로가 다르면 새로운 클래스 생성해야 함. 
class RecipeResource(Resource) : 
    # GET 메소드에서 경로로 넘어오는 변수는 GET함수의 파라미터로 적어주면 된다. 

    def get(self, recipe_id_abc) : 
        # 1. 클라이언트로부터 데이터를 받아온다. 
        # 위의 recipe_id_abc에 담겨있다. 
        print(recipe_id_abc)

        # 2. 데이터베이스에 레시피 아이디록 쿼리한다. (데려오라고.)
        try : 
            connection = get_connection()
            query = '''select r.*, u.username 
                    from recipe r
                    join user u
                        on r.user_id = u.id
                    where r.id = %s;'''
            
            record = (recipe_id_abc, )
            # 2-3. 커서 가져온다. 
            cursor = connection.cursor(dictionary=True) # JSON 형식으로 불러오려면. 이렇게. 
            # 2-4. 쿼리문을 커서로 실행한다. 
            
            cursor.execute(query, record)

            result_list = cursor.fetchall()
            # fetchall은 리스트로 가져옴
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e : 
            print(e)
            return {'result':'fail', 'error':str(e)}, 500 # 디버깅, 터미널 확인, 포스트맨 확인. 

        # 3. 결과를 클라이언트에 응답한다. 
        # 데이터가공이 필요하면, 가공한 후에 클라이언트에 응답한다. 
        i = 0
        for row in result_list :
            result_list[i]['created_at']= row['created_at'].isoformat()
            result_list[i]['updated_at']= row['updated_at'].isoformat()
            i = i + 1
            
        if len(result_list) != 1 : 
            return 
        else : 
            return {'result':'success', 'item':result_list[0]}


    @jwt_required()
    def put(self, recipe_id_abc) :

        # 1. 클라이언트로부터 데이터 받아온다.
        # body에 있는 json 데이터를 받아온다. 
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # 2.데이터베이스에 update한다. 
        try : 
            connection = get_connection()
            # make query 컬럼과 매칭되는 정보는 %s 쓸 수 있다. 
            query = '''update recipe 
                    set name = %s, description = %s, num_of_servings = %s, cook_time = %s, directions = %s, is_publish = %s
                    where id = %s and user_id = %s;'''
            record = ( data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'], data['is_publish'], recipe_id_abc, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e : 
            print(e)
            return {'result':'fail', 'error':str(0)}, 500


        return {'result':'success'}

    @jwt_required()
    def delete(self, recipe_id_abc) : 
        # 1. 클라이언트로부터 데이터 받아온다. 
        print(recipe_id_abc)
        user_id = get_jwt_identity()

        # 2. DB에서 삭제한다. 
        try : 
            connection = get_connection()
            query = '''delete from recipe where id = %s and user_id = %s;'''
            record = (recipe_id_abc, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()
        except Error as e : 
            print(e)
            return {'result':'success', 'error':str(e)}, 500

        # 3. 결과를 응답한다. 
    
        return {'result':'success'}


class RecipeListResource(Resource) : 
    @jwt_required()
    def post(self) : 
        # 포스트로 요청한 것을 처리하는 코드 작성을 우리가 한다!! class 함수에서는 무조건 self 써줘야 함. 함수 소속이라는 뜻 . 
        
        # 로직을 짠다. 무언가가 처리되는 순서를 짜는 것. 
        # 데이터 한 세트 복사해서 형식 보이게 해 두고.. 
            # {
            #     "name": "김치찌게",
            #     "description": "맛있게 끓이는 방법",
            #     "num_of_serving": 4,
            #     "cook_time": 30,
            #     "directions": "고기 볶고 김치 넣고 물 붓고 두부 넣고 끓임",
            #     "is_publish": 1
            # }
        
        # 1. 클라이언트가 보낸 데이터를 받아온다. 
        data = request.get_json()
        # 1-1. 추가 : 헤더에 담긴 JWT 토큰 받아온다. 
        user_id = get_jwt_identity()
        print(data)

        # 2. DB에 저장한다. 

       
        try : 
            # 2-1. 데이터베이스를 연결한다. 
            connection = get_connection()
            # 2-2. 쿼리문 만든다. ############## 중요!!!! 컬럼과 매칭되는 데이터만 %s로 바꿔준다. ### user_id 추가 
            query = '''insert into recipe 
                    (name, description, num_of_servings, cook_time, directions, is_publish, user_id)
                    values
                    (%s, %s, %s, %s, %s, %s, %s);'''
            # 2-3. 쿼리에 매칭되는 변수 처리!  중요! 튜플로 처리해준다! 컬럼명 변수 명 같은 정보 이름 통일 중요
            record = ( data['name'], data['description'], data['num_of_servings'], data['cook_time'], data['directions'], data['is_publish'], user_id)
            # 2-4. 커서를 가져온다. 
            cursor = connection.cursor()
            # 2-5. 쿼리문을 커서로 실행한다.
            cursor.execute(query, record) 
            # 2-6. DB에 반영 완료하라는 commit 해줘야 한다. 
            connection.commit()
            # 2-7. 자원해제
            cursor.close()
            connection.close()

        except Error as e : 
            print(e)
            return{'result':'fail', 'error':str(e)}, 500
            # internal server error

        # 3. 에러 났으면 에러났다고 알려주고, 그렇지 않으면, 잘 저장되었다고 알려준다. (return)

        # 필요에 따라 추가하자. 
        return{'result':'success'}
    
    def get(self):
        print("레시피 가져오는 API 동작했음")
        # 로직을 짜자 1,2,3

        # 1. 클라이언트로부터 데이터를 받아온다. 

        # 2. 저장된 레시피 리스트를 DB로부터 가져온다.
        # 2-1. DB 커넥션 
        try : 
            connection = get_connection()
            # 2-2. 쿼리문 작성
            query = '''select r.*, u.username 
                    from recipe r
                    join user u
                        on r.user_id = u.id
                    where is_publish = 1;'''
            # 2-3. 커서 가져온다. 
            cursor = connection.cursor(dictionary=True)
            # 2-4. 쿼리문을 커서로 실행한다. 
            cursor.execute(query)
            # 2-5. 실행 결과를 가져온다. 
            result_list = cursor.fetchall()
            # 디버깅할 유닛테스트 확인
            print(result_list) # 프린트하면 튜플로 나온다. 테이블 / JSON 형태로 바꿔져야됨.  
            cursor.close()
            connection.close()

            # restful api서버 

            # 3. 데이터가공이 필요하면, 가공한 후에 클라이언트에 응답한다. 
            i = 0
            for row in result_list :
                result_list[i]['created_at']= row['created_at'].isoformat()
                result_list[i]['updated_at']= row['updated_at'].isoformat()
                i = i + 1


        except Error as e :
            print(e)
            return {'result':'fail', 'error':str(e)}, 500
        

        return {'result':'success', 'count':len(result_list), 'items': result_list}, 400
        # , 400은 상태코드 설정. 
