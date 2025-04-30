from enum import Enum


class EventKeys(Enum):
    TOGGLE_SEARCH = 'toggle_search'
    INIT_TURN = 'init_turn'
    START_ROLLOUT = 'start_rollout'
    STOP_ROLLOUT = 'stop_rollout'
    MAX_HORZ_SPEED = 'max_horz_speed'
    MAX_VERT_SPEED = 'max_vert_speed'
    STOP_ESTIMATE = 'stop_estimate'
    BASE_LEG = 'base_leg'
    FRONT_RISER = 'front_riser'
    AFTER_RISER = 'after_riser'
    AFTER_TURN = 'after_turn'