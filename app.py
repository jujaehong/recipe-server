from flask import Flask         # 기본 틀
from flask_restful import Api
from resources.recipe import RecipeListResource  
from resources.recipe import RecipeResource
from resources.recipe import UserRegisterResource

app = Flask(__name__)

api = Api(app)

# 경로(path)와 API동작코드(Resource)를 연결한다.
api.add_resource(RecipeListResource ,'/recipes')  # 포스트맨 get에서 보내면 여기 app.py 여기 줄에서 받는다.
api.add_resource(RecipeResource ,'/recipes/<int:recipe_id>' ) # recipes/뒤에 숫자가 나오면 <int:recipe_id> 처리해라 ( 숫자는 레시피 아이디 이다.)
api.add_resource(UserRegisterResource,'/user/register' )


if __name__ == '__main__' :
    app.run()