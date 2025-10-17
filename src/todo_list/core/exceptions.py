class TodoListError(Exception):

    pass


class ValidationError(TodoListError):

    pass


class DuplicateError(TodoListError):

    pass


class LimitExceededError(TodoListError):

    pass


class NotFoundError(TodoListError):

    pass