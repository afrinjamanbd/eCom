import graphene
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from .models import ProductTable

class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()
   verify_account = mutations.VerifyAccount.Field()
   token_auth = mutations.ObtainJSONWebToken.Field()
   update_account = mutations.UpdateAccount.Field()
   resend_activation_email = mutations.ResendActivationEmail.Field()
   send_password_reset_email = mutations.SendPasswordResetEmail.Field()
   password_reset = mutations.PasswordReset.Field()
   password_change = mutations.PasswordChange.Field()


class ProductType(DjangoObjectType):
   class Meta:
      model = ProductTable
      field = ("id","name", "price","description","total_peice", "image")


class Query(graphene.ObjectType):
    # Add the first and skip parameters
    products = graphene.List(
        ProductType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    # Use them to slice the Django queryset
    def resolve_products(self, info, search=None, first=None, skip=None, **kwargs):
        qs = ProductTable.objects.all().filter(stock_status='available')

        if search:
            filter = (
                Q(url__icontains=search) |
                Q(description__icontains=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip:]

        if first:
            qs = qs[:first]

        return qs


class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)