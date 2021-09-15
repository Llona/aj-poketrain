import settings
from settings import IniEnum
import utils
from fighting import Fighting
import random
import os
import sys
from time import sleep


class Init(object):
    def __init__(self):
        super(Init, self).__init__()
        self.retry_count = 0

        self.effect_file_exists()

    def effect_file_exists(self):
        need_check_again = False

        up_path = os.path.join(sys.path[0], '..')

        if not os.path.exists(settings.SETTING_PATH):
            settings.SETTING_PATH = os.path.join(up_path, settings.SETTING_FILENAME)
            need_check_again = True

        if not os.path.exists(settings.MONSTER_DB_PATH):
            settings.MONSTER_DB_PATH = os.path.join(up_path, settings.MONSTER_DB_FILENAME)
            need_check_again = True

        self.retry_count += 1

        if self.retry_count > 2:
            print("資料庫或設定檔路徑錯誤")
            raise
        if need_check_again:
            self.effect_file_exists()

    @staticmethod
    def init_parameter():
        ini_h = utils.IniControl(settings.SETTING_PATH)
        debug_mode = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.DEBUG_MODE.value))

        if debug_mode == 1:
            settings.DEBUG = True
        else:
            settings.DEBUG = False

        settings.PRINT_LINE = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.PRINT_LINE_KEY.value))
        settings.ASK_TIME_MIN = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.ASK_TIME_MIN_KEY.value))
        settings.ASK_TIME_MAX = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.ASK_TIME_MAX_KEY.value))
        settings.CHANGE_MONSTER_WEIGHT = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.CHANGE_MONSTER_WEIGHT_KEY.value))
        settings.NO_CHANGE_MONSTER_WEIGHT = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.NO_CHANGE_MONSTER_WEIGHT_KEY.value))
        settings.GENERAL_SKILL_WEIGHT = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.GENERAL_SKILL_WEIGHT_KEY.value))
        settings.SPECIAL_SKILL_1_WEIGHT = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.SPECIAL_SKILL_1_WEIGHT_KEY.value))
        settings.SPECIAL_SKILL_2_WEIGHT = int(ini_h.read_config(
            IniEnum.GENERAL_SECTION.value, IniEnum.SPECIAL_SKILL_2_WEIGHT_KEY.value))

        if settings.DEBUG:
            print(settings.DEBUG,
                  settings.ASK_TIME_MIN,
                  settings.ASK_TIME_MAX,
                  settings.CHANGE_MONSTER_WEIGHT,
                  settings.NO_CHANGE_MONSTER_WEIGHT,
                  settings.GENERAL_SKILL_WEIGHT,
                  settings.SPECIAL_SKILL_1_WEIGHT,
                  settings.SPECIAL_SKILL_2_WEIGHT)

    @staticmethod
    def get_monster_from_db():
        json = utils.JsonControl(settings.MONSTER_DB_PATH)
        return json.read_config()

        # json.write_config(self.monster_db)
        # print(self.monster_db)


class CLI(object):
    def __init__(self):
        super(CLI, self).__init__()
        self.monster_db = None

        self.setup()

    def setup(self):
        init = Init()
        init.init_parameter()
        self.monster_db = init.get_monster_from_db()

    def start(self, monster_max):
        monster_all = list(self.monster_db.keys())
        ask_time_sec = random.randint(settings.ASK_TIME_MIN, settings.ASK_TIME_MAX)

        run_fighting = Fighting(ask_time_sec)
        for i in range(monster_max):
            monster_num = random.randint(0, len(monster_all) - 1)
            monster_name = monster_all.pop(monster_num)
            run_fighting.add_monster({monster_name: self.monster_db[monster_name]})

        if settings.DEBUG:
            print(run_fighting.get_monster_list())
        activate_monster = run_fighting.start_fighting()

        self.test_user_for_energy(activate_monster)

    @staticmethod
    def test_user_for_energy(activate_monster):
        sleep(1)
        os.system("cls")
        print("戰鬥停止, 請輸入 "+activate_monster.monster_name+" 目前能量:")
        user_input = input()
        if int(user_input) != activate_monster.energy:
            print("答錯了, 正確答案是: "+str(activate_monster.energy))
        else:
            print("答對囉!!")


if __name__ == '__main__':
    os.system('')
    poke = CLI()
    poke.start(2)
