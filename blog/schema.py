import graphene
from blog.models import Post
from framework.api.queries.user import UserBasicObj
from framework.api.APIException import APIException
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User


class PostObj(graphene.ObjectType):
    title = graphene.String(required=True)
    author = graphene.Field(UserBasicObj)
    date = graphene.Date(required=True)
    draft = graphene.Boolean()
    pinned = graphene.Boolean()
    description = graphene.String(required=True)

    def resolve_title(self, info):
        return self['title']

    def resolve_author(self, info):
        return User.objects.values().get(id=self['author_id'])

    def resolve_date(self, info):
        return self['date']

    def resolve_draft(self, info):
        return self['draft']

    def resolve_pinned(self, info):
        return self['pinned']

    def resolve_description(self, info):
        return self['description']


class postStatusObj(graphene.ObjectType):
    status = graphene.Boolean()


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        date = graphene.Date(required=True)
        draft = graphene.Boolean(required=True)
        pinned = graphene.Boolean(required=True)

    Output = postStatusObj

    @login_required
    def mutate(self, info, title, description, date, draft, pinned):
        post = Post.objects.filter(title=title)
        if post.count() == 0:
            post = Post.objects.create(
                title=title,
                description=description,
                date=date,
                author=info.context.user,
                draft=draft,
                pinned=pinned
            )
            post.save()
            return postStatusObj(status=True)
        else:
            raise APIException('Post already exists with same name',
                               code='POST_EXISTS')


class Query(graphene.ObjectType):
    posts = graphene.List(PostObj, username=graphene.String())
    post = graphene.Field(PostObj, title=graphene.String(required=True))

    def resolve_posts(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            Post.objects.values().filter(author__username=username)
        else:
            return Post.objects.values().all()

    def resolve_post(self, info, **kwargs):
        title = kwargs.get('title')
        if title is not None:
            Post.objects.values().get(title=title)
        else:
            raise APIException('Title is required',
                               code='TITLE_IS_REQUIRED')


class Mutation(graphene.ObjectType):
    createPost = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
