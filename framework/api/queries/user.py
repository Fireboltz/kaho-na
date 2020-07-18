import graphene
from users.models import Profile


class UserBasicObj(graphene.ObjectType):
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    isActive = graphene.Boolean()
    phone = graphene.String()
    bio = graphene.String()
    private = graphene.Boolean()
    isAdmin = graphene.Boolean()
    joinDateTime = graphene.types.datetime.DateTime()

    def resolve_firstName(self, info):
        return self['first_name']

    def resolve_lastName(self, info):
        return self['last_name']

    def resolve_fullName(self, info):
        return self['first_name'] + " " + self['last_name']

    def resolve_joinDateTime(self, info):
        return self['date_joined']

    def resolve_isActive(self, info):
        return self['is_active']

    def resolve_phone(self, info):
        return Profile.objects.values().get(user__username=self['username'])['phone']

    def resolve_bio(self, info):
        return Profile.objects.values().get(user__username=self['username'])['bio']

    def resolve_private(self, info):
        return Profile.objects.values().get(user__username=self['username'])['private']

    def resolve_isAdmin(self, info):
        return self['is_superuser']
