import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from framework.api.queries.user import UserBasicObj


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password',)


class userStatusObj(graphene.ObjectType):
    status = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    Output = userStatusObj

    def mutate(self, info, username, password, email):
        newUser = get_user_model()(
            username=username,
            email=email,
            is_active=False,
        )
        newUser.set_password(password)
        newUser.save()

        return userStatusObj(status=True)


class Query(graphene.ObjectType):
    user = graphene.Field(UserBasicObj, username=graphene.String(required=True))
    users = graphene.List(UserBasicObj, sort=graphene.String())

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.values().get(username=username)
        else:
            raise Exception('Username is a required parameter')

    def resolve_users(self, info, **kwargs):
        sort = kwargs.get('sort')
        if sort is None:
            sort = 'username'
        return User.objects.values().all().order_by(sort)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
