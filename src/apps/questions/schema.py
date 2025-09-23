from drf_spectacular.utils import extend_schema_view, extend_schema

question_schema = extend_schema_view(
    list=extend_schema(
        summary="List questions",
        description="Retrieve a paginated list of questions."
    ),
    create=extend_schema(
        summary="Create a question",
        description="Create a new question object."
    ),
    retrieve=extend_schema(
        summary="Retrieve a question",
        description="Retrieve a single question by its ID."
    ),
    destroy=extend_schema(
        summary="Delete a question",
        description="Delete a question object by its ID."
    ),
    update=extend_schema(
        summary="Update a question",
        description="Update all fields of a question object."
    ),
    partial_update=extend_schema(
        summary="Partially update a question",
        description="Update some fields of a question object."
    ),
)

alternative_schema = extend_schema_view(
    list=extend_schema(
        summary="List alternatives",
        description="Retrieve a list of alternatives. Staff users may filter by question ID using the `?question_id=` parameter.",
        tags=["alternatives"]
    ),
    create=extend_schema(
        summary="Create an alternative",
        description="Create a new alternative object.",
        tags=["alternatives"]
    ),
    retrieve=extend_schema(
        summary="Retrieve an alternative",
        description="Retrieve a single alternative by its ID.",
        tags=["alternatives"]
    ),
    destroy=extend_schema(
        summary="Delete an alternative",
        description="Delete an alternative object by its ID.",
        tags=["alternatives"]
    ),
    update=extend_schema(
        summary="Update an alternative",
        description="Update all fields of an alternative object.",
        tags=["alternatives"]
    ),
    partial_update=extend_schema(
        summary="Partially update an alternative",
        description="Update some fields of an alternative object.",
        tags=["alternatives"]
    ),
)

correct_answers_sources_schema = extend_schema_view(
    list=extend_schema(
        summary="List correct answer sources",
        description="Retrieve a list of sources for correct answers. Staff users may filter by question ID using the `?question_id=` parameter.",
        tags=["correct_answers_sources"]
    ),
    create=extend_schema(
        summary="Create a correct answer source",
        description="Create a new correct answer source object.",
        tags=["correct_answers_sources"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a correct answer source",
        description="Retrieve a single correct answer source by its ID.",
        tags=["correct_answers_sources"]
    ),
    destroy=extend_schema(
        summary="Delete a correct answer source",
        description="Delete a correct answer source object by its ID.",
        tags=["correct_answers_sources"]
    ),
    update=extend_schema(
        summary="Update a correct answer source",
        description="Update all fields of a correct answer source object.",
        tags=["correct_answers_sources"]
    ),
    partial_update=extend_schema(
        summary="Partially update a correct answer source",
        description="Update some fields of a correct answer source object.",
        tags=["correct_answers_sources"]
    ),
)
