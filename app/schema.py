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
      field = ("id","name", "price","description","total_peice", "stock_status", "image")


class Query(UserQuery, MeQuery, graphene.ObjectType):
    all_products = graphene.List(ProductType)

    def reolve_all_products(root, info):
      return ProductTable.objects.all()


class Mutation(AuthMutation, graphene.ObjectType):
   pass

schema = graphene.Schema(query=Query, mutation=Mutation)