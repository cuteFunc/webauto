import sys
import yaml
import os
from buildconnect import UiAuto

path = sys.path[0]


class Run:
    init_dic: dict

    def __init__(self, filepath='ui_auto'):
        self.init_path = r'%s\%s' % (path, filepath)
        self.switch = 1

    def run(self, filename=''):
        if filename:  # 如果是文件，则进入__run
            filename += '.yml'
            try:
                with open(rf'{self.init_path}\{filename}', 'r', encoding='utf8') as f:
                    string = f.read()
            except Exception:
                raise FileNotFoundError(rf'{self.init_path}\{filename}没有找到')
            self.__run(string)
        else:  # 如果是文件夹，则单独进入__run
            for file in os.listdir(self.init_path):
                if file.split('.')[-1] not in ('yml', 'yaml'):
                    continue
                with open(rf'{self.init_path}\{file}', 'r', encoding='utf8') as f:
                    string = f.read()
                self.__run(string)

    def __run(self, string):
        self.__parse(string)
        keys = list(self.init_dic.keys())
        for key in keys:
            if key == 'mainweb':
                self.__run_mianweb(self.init_dic['mainweb'])
            elif key == 'testpoint':
                self.__run_testpoint(self.init_dic['testpoint'])
            else:
                continue
        self.browser.quit()

    def __run_mianweb(self, dic: dict):
        if not self.__exist_value(dic, 'domain'):
            raise Exception('domain没有填写')
        self.domain = dic['domain']
        if self.__exist_value(dic, 'url'):
            if self.__exist_value(dic, 'headers'):
                self.__open_web(f'{dic["domain"]}{dic["url"]}', self.switch, dic['headers'])
            else:
                self.__open_web(f'{dic["domain"]}{dic["url"]}', self.switch)
            self.switch = 0
        if self.__exist_value(dic, 'step'):
            self.__execute_step(dic['step'])

    def __run_testpoint(self, dic_list: list):
        for dic in dic_list:
            if self.__exist_value(dic, 'url'):
                if self.__exist_value(dic, 'headers'):
                    self.__open_web(f'{self.domain}{dic["url"]}', self.switch, dic['headers'])
                else:
                    self.__open_web(f'{self.domain}{dic["url"]}', self.switch)
            if self.__exist_value(dic, 'pre_step'):
                self.__execute_step(dic['pre_step'])
            if self.__exist_value(dic, 'ckeck_point'):
                self.__check(dic['chech_point'])
            if self.__exist_value(dic, 'down_step'):
                self.__execute_step(dic['down_step'])

    def __execute_step(self, dic_list):
        for step in dic_list:
            for key, values in step.items():
                self.__execute_web(key, values)

    def __open_web(self, url, switch, headers=None):
        if headers is None:
            headers = []
        if switch:
            self.browser = UiAuto(headers)
        self.browser.connect(url)

    def __execute_web(self, execute, xpath, text=''):
        if execute == 'xpath_click':
            self.browser.click(xpath)
        elif execute == 'xpath_click':
            self.browser.input(xpath, text)

    def __parse(self, input_string):
        self.init_dic = yaml.load(input_string, Loader=yaml.FullLoader)

    @staticmethod
    def __exist_value(dic: dict, key):
        if key in dic.keys() and dic[key]:
            return True
        else:
            return False

    def __check(self, dic_list):
        pass

    def send_email(self):
        pass


if __name__ == "__main__":
    a = Run()
    a.run()
