# conda create -n lambda_app python=3.10
# conda env remove -n lambda_app
# lambda_app 가상환경에서 작업. 

from flask import Flask
from flask_restful import Api
from config import Config
from resources.my_list import MylistResource
from resources.recipe import MyRecipeListResource, RecipeListResource, RecipePublishResource, RecipeResource
from resources.user import UserLogoutResource, UserRegisterResource, UserLoginResource, jwt_blocklist
from flask_jwt_extended import JWTManager


app = Flask(__name__)


# 환경변수 셋팅 
app.config.from_object(Config) # 클래스를 넣어줬다.

# JWT 매니저 초기화 
jwt = JWTManager(app)
#플라스크 프레임워크에 jwt를 적용했다. 

# 고르아웃된 토큰으로 요청하는 경우! 이 경우는 비정상적인 경우 
# jwt가 알아서 처리하도록 코드 작성 . 
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)
# app을 플라스크 api에 넣어서 사용하겠어. 

# 경로(path)와 API동작코드(resource)를 연결한다. flask의 문법대로. flask에게 알려주기. 
api.add_resource( RecipeListResource, '/recipes' )
api.add_resource( RecipeResource, '/recipes/<int:recipe_id_abc>' )
api.add_resource( UserRegisterResource, '/user/register' )
api.add_resource( UserLoginResource, '/user/login' )
api.add_resource( UserLogoutResource, '/user/logout' )
api.add_resource( MylistResource, '/my_list')
api.add_resource( RecipePublishResource, '/recipes/<int:recipe_id>/publish') # 플라스크의 문법 
api.add_resource( MyRecipeListResource, '/recipes/me')


# (class, path) class 이름은 플라스크의 리소스를 상속받은 애구나 라는 걸 한 눈에 알 수 있게 Resource 붙여주는 게 좋다. 

if __name__ == '__main__' : 
    app.run()

