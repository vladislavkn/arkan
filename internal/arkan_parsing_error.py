class ArkanParsingError(RuntimeError):
    def __init__(self, line, message):
        formatted_message = f"Arkan parsing error on line {line}: {message}"
        super(ArkanParsingError, self).__init__(formatted_message)