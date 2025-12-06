from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)
from utils.serializers import MessageResponseSerializer


register_schema = extend_schema_view(
    post=extend_schema(
        summary="Registra um usuário no sistema",
        description="Registra um usuário e gera os tokens de autenticação JWT",
        responses={
            201: MessageResponseSerializer,
        },
    )
)


login_schema = extend_schema_view(
    post=extend_schema(
        summary="Autentica o usuário no sistema",
        description="Faz a autenticação do usuário e devolve os tokens",
        responses={
            200: MessageResponseSerializer,
        },
    )
)


logout_schema = extend_schema_view(
    post=extend_schema(
        summary="Faz o logout seguro do usuário no sistema",
        description="Realiza o logout do usuário colocando o token na blacklist",
        responses={
            200: MessageResponseSerializer,
        },
    )
)
