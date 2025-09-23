from drf_spectacular.utils import extend_schema_view, extend_schema

exam_attempt_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists all authenticated user questions",
        description="Lists all authenticated user questions at once.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific question",
        description="Retrieve a specific question from the authenticated user.",
    ),
    start_exam=extend_schema(
        summary="Creates an exam instance",
        description="Creates an exam instance to be completed.",
    ),
    finish_exam=extend_schema(
        summary="Updates an exam instance",
        description="Updates an exam instance filling the incomplete data.",
    ),
)

exam_question_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists all authenticated user questions",
        description="Lists all authenticated user questions at once.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific question",
        description="Retrieve a specific question from the authenticated user.",
    ),
    create=extend_schema(
        summary="Creates an exam_question object",
        description="Creates an exam_question object."
    )
)
