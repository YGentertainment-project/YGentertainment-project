import functools
import io
import json
import logging

from django.http import HttpResponse
from django.views.generic import View
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

logger = logging.getLogger("")


class APIError(Exception):
    def __init__(self, msg, err=None):
        self.err = err
        self.msg = msg
        super().__init__(err, msg)


class ContentType(object):
    json_request = "application/json"
    json_response = "application/json;charset=UTF-8"
    url_encoded_request = "application/x-www-form-urlencoded"
    multipart_request = "multipart/form-data"
    binary_response = "application/octet-stream"


class JSONResponse(object):
    content_type = ContentType.json_response

    @classmethod
    def response(cls, data):
        resp = HttpResponse(json.dumps(data, indent=4), content_type=cls.content_type)
        resp.data = data
        return resp


# 정의 : Cutwom APIView
# 목적 : API View의 success, error 타입 등을 원하는 데로 수정하기 위해 제작
# 멤버함수 : _get_request_data, extract_errors, invalid_serializer, dispatch, validate_serializer
# 개발자 : 최영우, cyw7515@naver.com
# 최종수정일 : 2022-01-03
class APIView(View):
    """
      Django view의 부모 클래스와 django-rest-framework의 사용법은 기본적으로 동일합니다.
      - request.data 를 통해 parsed json or urlencoded data, dict type를 얻을 수 있습니다.
      - self.success, self.error and self.invalid_serializer는 의도에 맞게 수정할 수 있습니다.
        (success, error format을 수정할 수 있도록 따로 APIView를 제작)
      - self.response는 self.response_class에 구현된 django HttpResponse를 반환합니다.
      - parse request class는 request_parser에 정의되어야 하며, 현재는 requested data 파싱에 json 및 urlencoded types만 지원합니다.
    """
    response_class = JSONResponse
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def _get_request_data(self, request):
        if request.method not in ["GET", "DELETE"]:
            body = request.body
            content_type = request.META.get("CONTENT_TYPE")
            if not content_type:
                raise ValueError("content_type is required")
            for parser in self.parser_classes:
                if content_type.startswith(parser.media_type):
                    break
            # else means the for loop is not interrupted by break
            else:
                raise ValueError("unknown content_type '%s'" % content_type)
            if body:
                if parser == JSONParser:
                    return parser().parse(io.BytesIO(body))
                else:
                    return parser().parse(
                        io.BytesIO(body),
                        media_type=content_type,
                        parser_context={"request": request}
                    )
            return {}
        return request.GET

    def response(self, data):
        return self.response_class.response(data)

    def success(self, data=None):
        return self.response({"error": None, "data": data})

    def error(self, msg="error", err="error"):
        return self.response({"error": err, "data": msg})

    def extract_errors(self, errors, key="field"):
        if isinstance(errors, dict):
            if not errors:
                return key, "Invalid field"
            key = list(errors.keys())[0]
            return self.extract_errors(errors.pop(key), key)
        elif isinstance(errors, list):
            return self.extract_errors(errors[0], key)

        return key, errors

    def invalid_serializer(self, serializer):
        key, error = self.extract_errors(serializer.errors)
        if key == "non_field_errors":
            msg = error
        else:
            msg = f"{key}: {error}"
        return self.error(err=f"invalid-{key}", msg=msg)

    def server_error(self):
        return self.error(err="server-error", msg="server error")

    def dispatch(self, request, *args, **kwargs):
        if self.parser_classes:
            try:
                request.data = self._get_request_data(self.request)
            except ValueError as e:
                return self.error(err="invalid-request", msg=str(e))
        try:
            return super(APIView, self).dispatch(request, *args, **kwargs)
        except APIError as e:
            ret = {"msg": e.msg}
            if e.err:
                ret["err"] = e.err
            return self.error(**ret)
        except Exception:
            logger.exception(e)
            return self.server_error()


def validate_serializer(serializer):
    """
    @validate_serializer(TestSerializer)
    def post(self, request):
        return self.success(request.data)
    """
    def validate(view_method):
        @functools.wraps(view_method)
        def handle(*args, **kwargs):
            self = args[0]
            request = args[1]
            s = serializer(data=request.data)
            if s.is_valid():
                request.data = s.data
                request.serializer = s
                return view_method(*args, **kwargs)
            else:
                return self.invalid_serializer(s)

        return handle

    return validate
