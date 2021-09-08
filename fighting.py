import settings
from settings import SkillEnum
from time import sleep
import random
import datetime


class Bcolors:
    MESSAGE = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR


class Monster(object):
    def __init__(self):
        super(Monster, self).__init__()
        self.skill_list = None
        self.monster_name = None
        self.energy = 0

    def config_skill(self, monster_data):
        if len(monster_data) > 1:
            print('error! monster data format is error')
            raise

        for k, v in monster_data.items():
            self.monster_name = k
            self.skill_list = v

        # print(self.monster_name)
        # print(self.monster_name, self.skill_list)

    def get_skill_date(self, skill_type):
        skill_name, skill_data = list(self.skill_list[skill_type].items())[0]
        return skill_name, skill_data

    def get_skill_energy(self, skill_type):
        skill_name, skill_data = self.get_skill_date(skill_type)
        return skill_data[1]

    def use_specify_skill(self, skill_type):
        skill_name, skill_data = self.get_skill_date(skill_type)
        skill_take_time = skill_data[0]
        skill_add_energy = skill_data[1]

        log_str = Bcolors.MESSAGE + self.monster_name+Bcolors.RESET+" 使用招式: "+Bcolors.MESSAGE+skill_name+Bcolors.RESET

        if settings.DEBUG:
            log_str = log_str + \
                      " 花費時間: " + \
                      Bcolors.MESSAGE + str(skill_take_time) + \
                      Bcolors.RESET + \
                      " 秒" + " 能量 " + \
                      Bcolors.MESSAGE + \
                      str(skill_add_energy) + \
                      Bcolors.RESET

        print(log_str)
        # print(bcolors.MESSAGE+self.monster_name +
        #       bcolors.RESET+" 使用招式: " +
        #       bcolors.MESSAGE+skill_name +
        #       bcolors.RESET+" 花費時間: " +
        #       bcolors.MESSAGE+str(skill_take_time) +
        #       bcolors.RESET+" 秒"+" 能量 " +
        #       bcolors.MESSAGE+str(skill_add_energy)+bcolors.RESET)

        sleep(skill_take_time)
        self.energy += skill_add_energy

        if settings.DEBUG:
            print(self.monster_name + " 目前能量 " + str(self.energy))


class Fighting(object):
    def __init__(self, ask_time_sec):
        super(Fighting, self).__init__()
        self.ask_time_sec = ask_time_sec
        self.monster_class_list = []
        # self.monster_list = []
        self.monster_activate = None
        self.monster_activate_index = 0
        self.monster_all_num = 0

    def start_fighting(self):
        self.monster_all_num = len(self.monster_class_list)
        # self.print_log(self.monster_all_num)
        print("開始戰鬥")
        self.choice_monster_random()
        print(self.monster_activate.monster_name)

        start_time = datetime.datetime.now()
        while True:
            self.use_skill()
            is_monster_change = self.choice_monster_random()
            if is_monster_change:
                # print()
                print(Bcolors.WARNING+'*****************'+Bcolors.RESET)
                print(Bcolors.WARNING+"切換: " + Bcolors.FAIL + self.monster_activate.monster_name + Bcolors.RESET)
                print(Bcolors.WARNING+'*****************'+Bcolors.RESET)
                # print()

            if self.is_time_up(start_time):
                break

        return self.monster_activate

    def is_time_up(self, start_time):
        now_time = datetime.datetime.now()
        count_time = (now_time - start_time).seconds
        if settings.DEBUG:
            print("測驗秒數%s, 已經過%s 秒" % (self.ask_time_sec, count_time))

        if count_time >= self.ask_time_sec:
            print("戰鬥停止")
            return True
        return False

    def use_skill(self):
        # print("special_1:%s, special_2:%s" % (abs(self.monster_activate.get_skill_energy(SkillEnum.SPECIAL_1.value)),
        #                                       abs(self.monster_activate.get_skill_energy(SkillEnum.SPECIAL_2.value))))
        # print(random.choices(range(len(SkillEnum)), weights=[60, 50, 50])[0])
        if self.monster_activate.energy > abs(self.monster_activate.get_skill_energy(SkillEnum.SPECIAL_1.value)):
            skill_index = random.choices([0, SkillEnum.SPECIAL_1.value],
                                         weights=[settings.GENERAL_SKILL_WEIGHT, settings.SPECIAL_SKILL_1_WEIGHT])[0]
        elif self.monster_activate.energy > abs(self.monster_activate.get_skill_energy(SkillEnum.SPECIAL_2.value)):
            skill_index = random.choices([0, SkillEnum.SPECIAL_2.value],
                                         weights=[settings.GENERAL_SKILL_WEIGHT, settings.SPECIAL_SKILL_2_WEIGHT])[0]
        elif self.monster_activate.energy >= 90:
            skill_index = random.choices([SkillEnum.SPECIAL_1.value, SkillEnum.SPECIAL_2.value],
                                         weights=[settings.SPECIAL_SKILL_1_WEIGHT, settings.SPECIAL_SKILL_2_WEIGHT])[0]
        else:
            skill_index = SkillEnum.GENERAL.value

        # print(skill_index)

        self.monster_activate.use_specify_skill(skill_index)

    def choice_monster_random(self):
        monster = random.choices(self.monster_class_list)[0]
        if not self.monster_activate:
            self.monster_activate = monster
            return True

        if not self.monster_activate == monster:
            need_change = random.choices([True, False],
                                         weights=[settings.CHANGE_MONSTER_WEIGHT, settings.NO_CHANGE_MONSTER_WEIGHT])
            if need_change:
                self.monster_activate = monster
                return True

        return False

    def add_monster(self, moster_data):
        # self.monster_list.append(moster_data)
        monster = Monster()
        monster.config_skill(moster_data)
        self.monster_class_list.append(monster)

    def get_monster_list(self):
        monster_name = []
        for i in self.monster_class_list:
            monster_name.append(i.monster_name)
        return monster_name

    @staticmethod
    def print_log(message):
        print(message)
