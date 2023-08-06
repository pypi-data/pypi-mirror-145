"""Flask blueprint for converting exceptions to JSON"""

from __future__ import annotations

__all__ = ('bp', 'handle_exception', 'JSONEncoder')

from typing import TYPE_CHECKING

import flask
import werkzeug

from .error import http_error

if TYPE_CHECKING:
    from typing import Any

bp = flask.Blueprint('json', __name__)


class JSONEncoder(flask.json.JSONEncoder):
    """JSONEncoder that converts unserializable objects to a string

    The object is converted to a str via `repr()`, and a warning is
    also logged
    """
    def default(self, obj: Any) -> Any:
        try:
            # Attempt to convert the object using the additional methods
            # defined by flask.json.JSONEncoder
            return super().default(obj)
        except TypeError:
            flask.current_app.logger.warning(
                'Encountered unserializable object when dumping to json: %r',
                obj
            )
            return repr(obj)


@bp.app_errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(e: werkzeug.exceptions.HTTPException) -> tuple[
    werkzeug.sansio.response.Response, int
]:
    """Return JSON instead of HTML for HTTP errors"""
    # Start with the correct headers and status code from the error
    response = e.get_response()

    # Create a JSONified response
    #
    # `flask.jsonify` is used instead of calling `flask.json.dumps`
    # directly because it pretty-prints the JSON depending on the app
    # config
    error = http_error.UnspecifiedError(e.name, e.code, e.description)
    jsonified_response = flask.jsonify(error.to_dict())

    # Replace the data in the original response with the JSONified data
    #
    # Mypy complains that `response` doesn't have the attribute `data`.
    # Not sure why, since it's an assignment
    response.data = jsonified_response.data  # type: ignore[attr-defined]
    response.content_type = jsonified_response.content_type

    return response, error.code
