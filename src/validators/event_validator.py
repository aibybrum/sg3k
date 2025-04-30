from utils import ErrorHandler


class EventValidator:
    @staticmethod
    def validate_event_names(event_names, key_events):
        for event in event_names:
            if event not in key_events:
                ErrorHandler.log_and_raise_error(ValueError, f"Event name '{event}' not found in key events.")