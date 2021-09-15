import sys
from os import path
import enum

MONSTER_DB_FILENAME = 'monsters.json'
SETTING_FILENAME = 'settings.ini'

MONSTER_DB_PATH = path.join(sys.path[0], MONSTER_DB_FILENAME)
SETTING_PATH = path.join(sys.path[0], SETTING_FILENAME)


DEBUG = False
PRINT_LINE = 0

ASK_TIME_MIN = 0
ASK_TIME_MAX = 0

CHANGE_MONSTER_WEIGHT = 0
NO_CHANGE_MONSTER_WEIGHT = 0

GENERAL_SKILL_WEIGHT = 0
SPECIAL_SKILL_1_WEIGHT = 0
SPECIAL_SKILL_2_WEIGHT = 0


class IniEnum(enum.Enum):
    GENERAL_SECTION = 'General'
    DEBUG_MODE = 'debug'
    PRINT_LINE_KEY = 'print_line'
    ASK_TIME_MIN_KEY = 'test_time_min'
    ASK_TIME_MAX_KEY = 'test_time_max'
    CHANGE_MONSTER_WEIGHT_KEY = 'change_monster_weight'
    NO_CHANGE_MONSTER_WEIGHT_KEY = 'no_change_monster_weight'
    GENERAL_SKILL_WEIGHT_KEY = 'general_skill_weight'
    SPECIAL_SKILL_1_WEIGHT_KEY = 'special_skill_1_weight'
    SPECIAL_SKILL_2_WEIGHT_KEY = 'special_skill_2_weight'


class SkillEnum(enum.IntEnum):
    GENERAL = 0
    SPECIAL_1 = 1
    SPECIAL_2 = 2
