from utils import EventKeys


class EventMarkerHelper:
    @staticmethod
    def get_event_keys_overview():
        return {
            EventKeys.TOGGLE_SEARCH.value: 'Elevation',
            EventKeys.INIT_TURN.value: 'Elevation',
            EventKeys.START_ROLLOUT.value: 'Elevation',
            EventKeys.STOP_ROLLOUT.value: 'Elevation',
            EventKeys.MAX_HORZ_SPEED.value: 'Horizontal speed'
        }

    @staticmethod
    def get_event_keys_speed():
        return {
            EventKeys.MAX_HORZ_SPEED.value: 'Horizontal speed',
            EventKeys.STOP_ROLLOUT.value: 'Horizontal speed',
            EventKeys.STOP_ESTIMATE.value: 'Horizontal speed'
        }

    @staticmethod
    def get_event_keys_side_view():
        return {
            EventKeys.INIT_TURN.value: 'Elevation',
            EventKeys.START_ROLLOUT.value: 'Elevation',
            EventKeys.TOGGLE_SEARCH.value: 'Elevation',
            EventKeys.STOP_ROLLOUT.value: 'Elevation',
            EventKeys.MAX_HORZ_SPEED.value: 'Horizontal speed'
        }

    @staticmethod
    def get_event_keys_overhead():
        return {
            EventKeys.TOGGLE_SEARCH.value: 'Elevation',
            EventKeys.INIT_TURN.value: 'Elevation',
            EventKeys.START_ROLLOUT.value: 'Elevation',
            EventKeys.STOP_ROLLOUT.value: 'Elevation',
            EventKeys.MAX_HORZ_SPEED.value: 'Horizontal speed'
        }

    @staticmethod
    def get_event_keys_2d_map():
        return {
            EventKeys.BASE_LEG.value: 'Elevation',
            EventKeys.TOGGLE_SEARCH.value: 'Elevation',
            EventKeys.INIT_TURN.value: 'Elevation',
            EventKeys.FRONT_RISER.value: 'Elevation',
            EventKeys.AFTER_RISER.value: 'Elevation',
            EventKeys.START_ROLLOUT.value: 'Vertical speed',
            EventKeys.MAX_HORZ_SPEED.value: 'Horizontal speed',
            EventKeys.STOP_ROLLOUT.value: 'Elevation'
        }