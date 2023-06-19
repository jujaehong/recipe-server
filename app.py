from flask import Flask         # 기본 틀
from flask_restful import Api
from config import Config
from resources.recipe import RecipeListResource  
from resources.recipe import RecipeResource
from resources.user import UserRegisterResource
from resources.user import UserLoginsource
from flask_jwt_extended import JWTManager
from resources.user import UserLogoutsource ,jwt_blocklist


app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)

# 로그아웃된 토큰으로 요청하는 경우! 이 경우는 비정상적인 경우
# 이므로, jwt 가 알아서 처리하도록 코드작성.
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)

# 경로(path)와 API동작코드(Resource)를 연결한다.
api.add_resource(RecipeListResource ,'/recipes')  # 포스트맨 get에서 보내면 여기 app.py 여기 줄에서 받는다.
api.add_resource(RecipeResource ,'/recipes/<int:recipe_id>' ) # recipes/뒤에 숫자가 나오면 <int:recipe_id> 처리해라 ( 숫자는 레시피 아이디 이다.)
api.add_resource(UserRegisterResource,'/user/register' ) # 회원가입
api.add_resource(UserLoginsource ,'/user/login' ) # 로그인
api.add_resource(UserLogoutsource ,'/user/logout' ) # 로그아웃

if __name__ == '__main__' :
    app.run()