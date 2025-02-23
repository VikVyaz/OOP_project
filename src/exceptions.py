class FileEmptyError(Exception):
    """Кастомная ошибка. Ошибка 'пустого файла'"""

    def __init__(self, message):
        super().__init__(message)


class WrongAttributeChoiceError(Exception):
    """Кастомная ошибка. Ошибка 'неправильного аттрибута'"""

    def __init__(self, message):
        super().__init__(message)
