from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["session"]=user.session

        return token