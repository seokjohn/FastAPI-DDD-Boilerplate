from sqlalchemy import (
    func,
)

from app.user.enums import SnsType
from app.user.entity import (
    Users,
    Profiles,
    UserStatus
)
from app.user.repository import (
    user_repository,
    profile_repository,
)

from core.db import Transactional
from app.user.exceptions import (
    InvalidTokenEx,
    WithdrawalUserEx

)
from core.utils.google.oauth import verify_token


class UserOauthService:
    def __init__(self):
        ...
    
    @Transactional()
    async def goog_login(self, id_token: str):
        try:
            email, _, picture_url = await verify_token(id_token)
        except Exception as e:
            raise InvalidTokenEx(ex=e)
        
        user = await user_repository.get_by_filter(
            email=email,
            sns_type= SnsType.google
        )

        if not user:
            user = await user_repository.save(
                Users(
                    email=email, 
                    sns_type=SnsType.google
                )
            )
            await profile_repository.save(
                Profiles(
                    user_id=user.id,
                    nick_name=nick_name,
                    picture_url=picture_url
                )
            )

        else:
            if user.status == UserStatus.deleted:
                raise WithdrawalUserEx()

            await user_repository.update_by_id(
                user.id, {"last_service_used": func.current_timestamp()}
            )
            profile = await profile_repository.get_by_filter(user_id=user.id)

            nick_name = profile.nick_name
            picture_url = profile.picture_url
        #토큰 생성 및 구글 유저 가져오기
        result_dict = {}
        #result_dict = get_tokens(user)
        result_dict["user_id"] = user.id
        result_dict["nick_name"] = nick_name
        result_dict["picture_url"] = picture_url
        return result_dict

user_oauth_service = UserOauthService()