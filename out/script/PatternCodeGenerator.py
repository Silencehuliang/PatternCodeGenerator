import sys
import traceback
import jinja2schema
from jinja2 import Environment, FileSystemLoader


class PatternCodeGenerator:
    def __init__(self, template_path, template_name):
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.template_name = template_name

    def check_template(self):
        """
        校验模版
        :return: 模板名对象或错误信息
        """
        try:
            template_obj = self.env.get_template(self.template_name)
        except Exception as err:
            exc_type, exc_value, exc_traceback_obj = sys.exc_info()  # 取得Call Stack
            last_call_stack = traceback.extract_tb(exc_traceback_obj)[-1]  # 取得Call Stack 最近一次的內容
            return "模板错误，错误行号：{}，错误原因：{}".format(last_call_stack[1], err.args[0])
        return template_obj

    def get_template_variable(self):
        """
        获取模版中的变量
        :return: 模版中的变量列表
        """
        template_obj = self.check_template()
        if type(template_obj) is not str:
            template_source = self.env.loader.get_source(self.env, self.template_name)[0]
            return jinja2schema.infer(template_source)
        else:
            return template_obj

    def render_template(self, data):
        """
        根据变量的值渲染模板
        :param data: 变量的值
        :return:
        """
        template_obj = self.check_template()
        if type(template_obj) is not str:
            return template_obj.render(data)
        else:
            return template_obj


if __name__ == '__main__':
    pcg = PatternCodeGenerator("./", "demo.txt")
    pcg.check_template()
    pcg.get_template_variable()
    print(pcg.render_template({"test": "test", "test_list": [{"test": "test"}]}))
