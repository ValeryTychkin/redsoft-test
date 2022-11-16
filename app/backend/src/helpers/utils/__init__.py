from rest_framework import status


class ApiCallException(Exception):

    def __init__(self, message, url, content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.url = url
        self.response_content = content
        self.status_code = status_code
        super().__init__(message)

    def __str__(self):
        return '\n'.join([
            f'url = {self.url}',
            f'status_code = {self.status_code}',
            f'response_content = {self.response_content}',
            f'error_message = {self.message}',
        ])
