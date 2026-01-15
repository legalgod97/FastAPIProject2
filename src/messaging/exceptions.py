class KafkaError(Exception):
    pass


class KafkaNotStartedError(KafkaError):
    pass


class ConsumerError(Exception):
    pass


class ValidationError(ConsumerError):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


class AlreadyProcessedError(ConsumerError):
    def __init__(self, message_id: str):
        self.message_id = message_id
        super().__init__(f"Message '{message_id}' already processed")


class ProcessingError(ConsumerError):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(f"Processing error: {detail}")