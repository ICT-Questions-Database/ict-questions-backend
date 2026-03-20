from drf_spectacular.utils import extend_schema_view, extend_schema


question_submissions_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists a set of question_submissions",
        description="Lists all question_submissions if the user is an admin; otherwise, returns only the question submissions submitted by the user",
        tags=["question_submissions"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a question_submission object",
        description="Retrieve a question_submission object",
        tags=["question_submissions"],
    ),
    create=extend_schema(
        summary="Creates a question_submission object",
        description="Creates a question_submission_object.",
        tags=["question_submissions"],
    ),
    update=extend_schema(
        summary="Updates a question_submission object",
        description="Updates a question_submission object.",
        tags=["question_submissions"],
    ),
    partial_update=extend_schema(
        summary="Partially updates a question_submission instance",
        description="Partially updates a question_submission instance",
        tags=["question_submissions"],
    ),
    review=extend_schema(
        summary="Updates a reviewed question in the database.",
        description="Updates a reviewed question in the database, populating submitted_by.",
        tags=["question_submissions"],
    ),
    destroy=extend_schema(
        summary="Deletes a question_submission object",
        description="Deletes a question_submission object.",
        tags=["question_submissions"],
    ),
)


correct_submissions_answers_sources_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists all CorrectSubmissionAnswersSources from the user",
        description="Lists all CorrectSubmissionAnswersSources from the user",
        tags=["correct_submission_answers_sources"],
    ),
    retrieve=extend_schema(
        summary="Retrieves a CorrectSubmissionAnswersSources submitted by the user",
        description="Retrieves a CorrectSubmissionAnswersSources submitted by the user",
        tags=["correct_submission_answers_sources"],
    ),
    create=extend_schema(
        summary="Creates a CorrectSubmissionAnswersSources object",
        description="Creates a CorrectSubmissionAnswersSources in the database.",
        tags=["correct_submission_answers_sources"],
    ),
    update=extend_schema(
        summary="Updates a CorrectSubmissionAnswersSources object",
        description="Updates a CorrectSubmissionAnswersSources object",
        tags=["correct_submission_answers_sources"],
    ),
    destroy=extend_schema(
        summary="Deletes a CorrectSubmissionAnswersSources object",
        description="Deletes a CorrectSubmissionAnswersSources object in the database.",
        tags=["correct_submission_answers_sources"],
    ),
)


alternative_submissions_schema = extend_schema_view(
    list=extend_schema(
        summary="Lists all AlternativeSubmission from the user",
        description="Lists all AlternativeSubmission from the user",
        tags=["alternative_submissions"],
    ),
    retrieve=extend_schema(
        summary="Retrieves a AlternativeSubmission submitted by the user",
        description="Retrieves a AlternativeSubmission submitted by the user",
        tags=["alternative_submissions"],
    ),
    create=extend_schema(
        summary="Creates a AlternativeSubmission object",
        description="Creates a AlternativeSubmission in the database.",
        tags=["alternative_submissions"],
    ),
    update=extend_schema(
        summary="Updates a AlternativeSubmission object",
        description="Updates a AlternativeSubmission object",
        tags=["alternative_submissions"],
    ),
    partial_update=extend_schema(
        summary="Partially updates a AlternativeSubmission object",
        description="Partially updates a AlternativeSubmission object",
        tags=["alternative_submissions"],
    ),
    destroy=extend_schema(
        summary="Deletes a AlternativeSubmission object",
        description="Deletes a AlternativeSubmission object in the database.",
        tags=["alternative_submissions"],
    ),
)
