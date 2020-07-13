import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from framework.api.queries.user import UserBasicObj
import blog.schema
from django.core.mail import send_mail
from framework import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import hashlib

secret_key = settings.SECRET_KEY
from_email = settings.EMAIL_HOST_USER


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password',)


class userStatusObj(graphene.ObjectType):
    status = graphene.Boolean()


class VerifyOTP(graphene.Mutation):
    class Arguments:
        otp = graphene.String(required=True)

    Output = userStatusObj

    def mutate(self, info, otp):
        user = User.objects.values().get(username=info.context.user)
        s = secret_key + user['email']
        hashEncoded = hashlib.md5(s.encode())
        encodedHash = hashEncoded.hexdigest()[:4]
        if encodedHash == otp:
            user.is_active = True
            user.save()
            status = True
        else:
            status = False
        return userStatusObj(status=status)


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
        s = secret_key + email
        hashEncoded = hashlib.md5(s.encode())
        otp = hashEncoded.hexdigest()[:4]
        context = {
            "otp": otp,
            "username": username
        }
        message = render_to_string('email/verify_email.html', context)
        send_mail('Verification | Micro Blogging', strip_tags(message), from_email, [email], fail_silently=False,
                  html_message=message)

        return userStatusObj(status=True)


class Query(blog.schema.Query, graphene.ObjectType):
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


class Mutation(blog.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()
    verify_otp = VerifyOTP.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
