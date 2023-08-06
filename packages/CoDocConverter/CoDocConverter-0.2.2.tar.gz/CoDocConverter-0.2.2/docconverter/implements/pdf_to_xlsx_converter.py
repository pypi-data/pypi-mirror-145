import os
import threading
import time
import win32api
import win32gui
from os.path import exists, join
from subprocess import Popen, PIPE, STDOUT
import win32con
import xlrd

from docconverter.core.converter_base import DocConverterBase


class PdfToXlsxConverter(DocConverterBase):
    """
    PDF转Excel批量转换器
    """

    def __init__(self):
        self.check_time = time.time()

    def convert(self, input_file, output_dir, **args):
        """
        转换文件
        """
        output_files = self.bulk_convert([input_file], output_dir, **args)
        return output_files[0]

    def bulk_convert(self, input_files, output_dir, **args):
        """
        批量转换
        :param input_files: 输入文件列表
        :param output_dir: 输出目录
        :param args: 其它参数
        :return:
        """
        # 杀掉已存在adobe进程
        PdfToXlsxConverter._kill_tasks()

        # 如果没输出目录创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 列出所有需要转换pdf文件
        files = list(PdfToXlsxConverter._iter_files(input_files))
        files.sort()

        output_files = []
        for index, file in enumerate(files):
            # 文件不存在直接异常退出
            if not exists(file):
                raise FileNotFoundError

            # 判断输出文件是否已存在，存在则退出
            suffix = ".xlsx"
            if "suffix" in args:
                suffix = args["suffix"]
            name, _ = os.path.splitext(os.path.basename(file))
            save_path = join(output_dir, name + suffix)
            if os.path.exists(save_path):
                if self._check(save_path, args):
                    print('%d/%d 成功!' % (index + 1, len(files)))
                    continue
                else:
                    os.remove(save_path)
                    print('错误 xlsx, 请再次转换!')

            # 执行adobe 控制台转换pdf
            cmd = "%s -i %s -o %s -f %s" % (args["exe"],
                                            file, output_dir, "xlsx")
            print("转换命令:%s" % cmd)
            thread = threading.Thread(target=PdfToXlsxConverter._pdf_to_excel, args=(cmd,))
            thread.start()

            # 循环等待文件转换完成
            while True:
                # 验证是否在未超时前处理成功
                if os.path.exists(save_path):
                    print('%s 成功!' % save_path)
                    PdfToXlsxConverter._kill_tasks()
                    break

                # 超时处理
                if time.time() - self.check_time > args["timeout"]:
                    print('超时! %s 失败!' % save_path)
                    PdfToXlsxConverter._kill_tasks()
                    break

                # 阻塞任务
                PdfToXlsxConverter._blocking()

            output_files.append(save_path)

        return output_files


    def _check(self, file, args):
        """
        检查文件是否转换成功
        :param file:文件路径
        :param args:参数
        :return: 成功返回True,失败返回False
        """
        if os.path.exists(file):
            return True

        # 自循环阻塞检查文件是否转换成功
        while time.time() - self.check_time < args["timeout"]:
            PdfToXlsxConverter._blocking()
            try:
                _ = xlrd.open_workbook(file)
                return True
            except:
                continue

        return False

    @staticmethod
    def _blocking():
        """
        阻塞
        :return:
        """
        whd = win32gui.FindWindow(0, 'Adobe Acrobat')
        if whd > 0:
            hwnd_childs = PdfToXlsxConverter._get_child_windows(whd)
            for hwnd in hwnd_childs:
                try:
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    if (title == "确定(&O)" or title == "确定") and class_name == "Button":
                        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
                        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
                        break
                except:
                    continue

    @staticmethod
    def _iter_files(path):
        """
        迭代改路径下的所有文件
        """
        if hasattr(path, '__iter__'):
            for f in path:
                yield f
        elif os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            for dir_path, _, file_names in os.walk(path):
                for f in file_names:
                    if f.endswith(".pdf"):
                        yield os.path.join(dir_path, f)
        elif "," in path:
            for file in path.split(","):
                yield file
        else:
            raise RuntimeError('路径 %s 无效' % path)

    @staticmethod
    def _kill_tasks():
        """
        杀掉Acrobat相关进程
        :return:
        """

        try:
            task_list = ["Acrobat.exe", "AcroCEF.exe"]
            for task in task_list:
                cmd = "tasklist | findstr \"%s\"" % task
                kill = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
                info = kill.stdout.readlines()
                for each in info:
                    each = each.decode('utf-8')
                    Popen("taskkill /pid %s -t -f" % each.split()[1], stdout=PIPE, stderr=STDOUT, shell=True)
        except:
            print("杀掉Acrobat相关进程失败！")

    @staticmethod
    def _get_child_windows(parent):
        '''
         获得parent的所有子窗口句柄
         返回子窗口句柄列表
         '''
        if not parent:
            return
        hwnd_child_list = []
        try:
            win32gui.EnumChildWindows(
                parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
        except:
            return []
        return hwnd_child_list

    @staticmethod
    def _pdf_to_excel(cmd):
        """
        执行pdf转excel命令
        :param cmd:
        :return:
        """
        Popen(cmd, shell=True)



