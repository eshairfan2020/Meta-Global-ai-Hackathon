"""Technical error states. These are deliberately separate from model assessments:
'insufficient_evidence' is something the model concludes; these mean processing failed."""


class AppError(Exception):
    status = 500
    code = "internal_error"
    default_message = "Something went wrong."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class BadInput(AppError):
    status, code = 422, "invalid_input"
    default_message = "The input is not valid."


class CaseNotFound(AppError):
    status, code = 404, "case_not_found"
    default_message = "Case not found. Backend restarts clear temporary cases."


class ProviderBusy(AppError):
    status, code = 429, "model_busy"
    default_message = "The local model is busy with another request. Try again in a moment."


class ProviderUnavailable(AppError):
    status, code = 503, "model_unavailable"
    default_message = "The local Ollama service could not be reached. Is it running?"


class ModelNotInstalled(AppError):
    status, code = 503, "model_not_installed"
    default_message = "The configured model is not installed in Ollama."


class ProviderTimeout(AppError):
    status, code = 504, "model_timeout"
    default_message = "The local model did not answer in time (CPU inference can be slow)."


class InvalidModelOutput(AppError):
    status, code = 502, "invalid_model_output"
    default_message = "The model did not return a valid structured assessment, even after one retry."


class MockNoFixture(AppError):
    status, code = 422, "mock_no_fixture"
    default_message = (
        "Mock mode only has predefined results for the four synthetic examples. "
        "Analyzing arbitrary or edited text requires AI_PROVIDER=ollama."
    )
