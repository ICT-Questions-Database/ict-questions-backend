from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample


user_register_schema = extend_schema_view(
    create=extend_schema(
        summary="Creates a user object",
        description="Creates a new user object.",
        examples=[
            OpenApiExample(
                "Exemplo de registro válido",
                summary="Cadastro de usuário",
                description="Exemplo de payload para criar um novo usuário",
                value={
                    "username": "joao.silva",
                    "password": "senha123",
                    "firstName": "João",
                    "lastName": "Silva",
                    "email": "joao.silva@example.com",
                },
                request_only=True,
                response_only=False,
            ),
        ],
    ),
)

user_profile_schema = extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a user's personal information",
        description="Returns a user's personal information.",
    ),
    update=extend_schema(
        summary="Updates a user personal information",
        description="Updates a user personal information.",
    ),
    partial_update=extend_schema(
        summary="Partially updates a user personal information",
        description="Partially updates a user personal information.",
    ),
    destroy=extend_schema(
        summary="Deletes a user",
        description="Deletes a user.",
    ),
)

user_actions_schema = extend_schema_view(
    change_password=extend_schema(
        summary="Changes user password",
        description="Changes authenticated user password.",
    ),
)

user_answers_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists all the answers from the user for the given exam",
        description="Lists all the answers from the user for the given exam.",
        tags=["user_answers"],
    ),
    create=extend_schema(
        summary="Creates an user_answer object",
        description="Creates an user_answer object in the database.",
        tags=["user_answers"],
    ),
)
