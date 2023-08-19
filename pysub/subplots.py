import argparse
import math
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import proplot as pplt
import toml
import wx
from proplot import rc

# 声明全局变量 LAYOUT，用于操控子图的排版
LAYOUT = "auto"
# 声明全局变量 DPI，用于操控保存图片的分辨率
DPI = 300
# 声明全局变量 SAVE_FORMAT，用于操控保存图片的格式
SAVE_FORMAT = "png"
# 声明全局变量 FONT_SIZE，用于操控字号
FONT_SIZE = [10.5, 12, 14]
# 声明全局变量 FONT_NAME，用于操控字体
FONT_NAME = "Arial"
# 声明全局变量 FIGURE_SIZE，用于操控画布的大小
FIGURE_SIZE = "auto"
# 声明全局变量 IS_SERIAL，用于操控是否开启子图序号
IS_SERIAL = True
# 声明全局变量 IS_SHARE，用于操控是否共用坐标轴
IS_SHARE = True
# 声明全局变量 IS_SPAN，用于操控是否共用坐标轴标签
IS_SPAN = True


class Version:
    """
    用于记录版本信息和一些内容的类
    """

    # 版本信息和有关 py-subplots 的介绍
    def __init__(self):
        # 获取当前文件的绝对路径
        file_path = os.path.abspath(__file__)
        # 获取最后修改时间的时间戳
        timestamp = os.path.getmtime(file_path)
        self.developer = "Kimariyb, Ryan Hsiun"
        self.version = 'v1.0.0'
        self.release_date = str(datetime.fromtimestamp(timestamp).strftime("%b-%d-%Y"))
        self.address = "XiaMen University, School of Electronic Science and Engineering"
        self.website = 'https://github.com/kimariyb/py-subplots'


# 全局的 Version 对象
VERSION = Version()


class SubplotsConfig:
    """
    进入主程序时所使用的配置类
    """

    def __init__(self, font_family, font_size, figure_size, is_serial, sup_layout, dpi, save_format, is_share,
                 is_span):
        """
        初始化 SubplotsConfig 对象
        :param sup_layout: 子图的排版，list 类型
        :param is_serial: 是否显示序号，bool 类型
        :param font_family: 字体，string 类型
        :param font_size: 字号，普通字体、label 字体和 title 字体，例如 [10.5, 12, 14]，list 类型
        :param figure_size: 图纸的大小，例如 (4, 5)，tuple 类型
        :param dpi: 保存文件的分辨率，float 类型
        :param save_format: 保存文件的格式，string 类型
        :param is_share: 是否共用坐标轴，bool 类型
        :param is_span: 是否共用坐标轴刻度，bool 类型
        """
        self.font_family = font_family
        self.font_size = font_size
        self.figure_size = figure_size
        self.is_serial = is_serial
        self.sup_layout = sup_layout
        self.dpi = dpi
        self.save_format = save_format
        self.is_share = is_share
        self.is_span = is_span


class Spectrum:
    """
    用于绘制图像的 Spectrum 类，这个类必须从 toml 文件中读取
    """

    def __init__(self, x_limit, y_limit, title, x_label, y_label, colors,
                 line_style, is_zero, is_legend, legend_text, plot_data):
        """
        初始化 Spectrum 对象
        :param x_limit: X 轴坐标的最小、最大值以及间距，例如 [0, 4000, 500]，list 类型
        :param y_limit: Y 轴坐标的最小、最大值以及间距，例如 [0, 3000, 1000]，list 类型
        :param title: 图片的标题，string 类型
        :param x_label: X 轴标签，string 类型
        :param y_label: Y 轴标签，string 类型
        :param colors: 曲线的颜色，可以是一个有字符串组成的 list 类型，也可以是一个 string 类型
        :param line_style: 曲线的风格，可以是一个有字符串组成的 list 类型，也可以是一个 string 类型
        :param legend_text: 图例的文本，可以是一个有字符串组成的 list 类型，也可以是一个 string 类型
        :param is_zero: 是否开启 zero 轴，bool 类型
        :param is_legend: 是否显示图例，bool 类型
        :param plot_data: 绘图数据，一个 DataFrame 对象
        """
        self.x_limit = x_limit
        self.y_limit = y_limit
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.colors = colors if isinstance(colors, list) else [colors]
        self.line_style = line_style if isinstance(line_style, list) else [line_style]
        self.legend_text = legend_text if isinstance(legend_text, list) else [legend_text]
        self.is_zero = is_zero
        self.is_legend = is_legend
        self.plot_data = plot_data

    def __str__(self):
        return f"Spectrum Object:\n" \
               f"  x_limit: {self.x_limit}\n" \
               f"  y_limit: {self.y_limit}\n" \
               f"  x_label: {self.x_label}\n" \
               f"  y_label: {self.y_label}\n" \
               f"  title: {self.title}\n" \
               f"  line_style: {self.line_style}\n" \
               f"  colors: {self.colors}\n" \
               f"  legend_text: {self.legend_text}\n" \
               f"  is_legend: {self.is_legend}\n" \
               f"  is_zero: {self.is_zero}\n"


def auto_layout(len_list):
    """
    自动排版功能，可以根据数据的多少自动判断，需要如何排版
    排版的算法为，根据一个数据集合的长度，首先对其进行因式分解。例如 9 可以分为 3 和 3，则返回 [3,3]。
    例如 15 可以分解为 5 和 3，则返回 [5,3] 注意，一个数如果能分解为两个数，则较大的一个数在前。
    如果一个数是一个质数，只能分解为 n 和 1，则返回 [n,1]
    :param len_list: 数据集合的长度，如 9
    :return: 返回一个 list 集合，这个list 集合记录了排版的信息，如 [3, 3]
    """
    layout_list = []

    # 辅助函数，判断一个数是否为质数
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    if is_prime(len_list):
        # 如果数据集合长度为质数，则按照 [n, 1] 的排版方式
        layout_list = [len_list, 1]
    else:
        # 因式分解，找到能整除数据集合长度的两个因子
        for i in range(int(math.sqrt(len_list)), 1, -1):
            if len_list % i == 0:
                layout_list = [len_list // i, i]
                break

    return layout_list


def load_toml(toml_file):
    """
    根据 toml 文件得到 spectrum 组成的集合
    :param toml_file: toml 文件
    :return: spectrum list
    """
    # 根据 toml 文件得到 spectrum 对象
    with open(toml_file, 'r', encoding='utf-8') as file:
        spectrum_configs = toml.load(file)
    # 新建一个 list 用来存放 spectrum 对象
    spectrum_list = []
    # 解析文件内容
    for spectrum_config in spectrum_configs['file']:
        # 新建一个 DataFrame 对象
        data = pd.DataFrame()
        # 拿到每一个 file 下的所有参数
        path = spectrum_config['path']
        # 读取 Multiwfn 输出的 txt 文件或者一个记载光谱数据的 excel 文件
        file = Path(path)
        # 根据文件的后缀是否为 txt 或者 xlsx 判断
        if file.suffix == ".txt":
            # 如果是 Multiwfn 输出的 txt 文件，调用 Pandas 的 read_csv 方法读取
            data = pd.read_csv(file, delim_whitespace=True, header=None)
        elif file.suffix == ".xlsx":
            # 读取包含光谱数据的 Excel 文件，假设文件包含一个名为 Sheet1 的表格
            data = pd.read_excel(file, sheet_name=0, dtype={'column_name': float})
        else:
            # 文件格式不支持
            raise ValueError("Unsupported file format.")

        # 解析 toml 文件中的其他参数
        colors = spectrum_config['colors']
        styles = spectrum_config['styles']
        legend = spectrum_config['legend']
        xlim = spectrum_config['xlim']
        ylim = spectrum_config['ylim']
        x_label = spectrum_config['xlabel']
        y_label = spectrum_config['ylabel']
        title = spectrum_config['title']
        is_zero = bool(spectrum_config['iszero'])
        is_legend = bool(spectrum_config['islegend'])

        # 初始化一个 spectrum 对象
        spectrum = Spectrum(x_limit=xlim, y_limit=ylim, x_label=x_label, y_label=y_label, title=title, colors=colors,
                            line_style=styles, legend_text=legend, is_zero=is_zero, is_legend=is_legend, plot_data=data)

        # 在 spectrum 追加每一个 spectrum 对象
        spectrum_list.append(spectrum)

    return spectrum_list


def show_head(version_info: Version):
    """
    展示程序头，显示程序的基本信息、配置信息以及版权信息。
    """
    # 展示程序头
    print(f"pySubplots -- A python script for plotting multiple subplots.")
    print(f"Version: {version_info.version}, release date: {version_info.release_date}")
    print(f"Developer: {version_info.developer}")
    print(f"Address: {version_info.address}")
    print(f"KimariDraw home website: {version_info.website}\n")
    # 获取当前日期和时间
    now = datetime.now().strftime("%b-%d-%Y, 00:45:%S")
    # 程序结束后提示版权信息和问候语
    print(f"(Copyright 2023 Kimariyb. Currently timeline: {now})\n")


def validate(toml_path):
    """
    判断输入的 toml 文件是否符合标准
    :param toml_path: toml 文件的路径
    """
    # 首先判断输入的是否为 toml 文件，如果不是，则抛出异常。并在屏幕上打印不支持该文件
    if not toml_path.endswith(".toml"):
        raise ValueError("Error: Unsupported file format. Only TOML files are supported.\n")

    # 判断输入的 toml 文件是否存在，如果不存在，则抛出异常。并在屏幕上打印未找到该文件
    if not os.path.isfile(toml_path):
        raise FileNotFoundError("Error: File not found.\n")


def select_file():
    """
    和用户交互式的选择需要输入的 toml 文件，并返回 toml 文件的路径
    如果直接写入 toml 文件的绝对路径，则直接返回 toml_path
    如果输入 Enter 则弹出 GUI 界面选择 toml 文件
    如果输入 q 则退出整个程序
    :return: toml_path
    """
    # 创建文件对话框
    dialog = wx.FileDialog(None, "Select toml file", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    while True:
        # 输入的文本
        input_str = input("Input toml file path, for example E:\\Hello\\World.toml\n"
                          "Hint: Press ENTER button directly can select file in a GUI window. "
                          "If you want to exit the program, simply type the letter \"q\" and press Enter.\n")
        # 如果输入为 "q"，则退出主程序
        if input_str.lower() == "q":
            print("The program has exited！")
            exit()
        # 对应与直接输入 Enter，如果输入 ENTER 则显示对话框，不会退出主程序
        if not input_str:
            # 弹出文件选择对话框
            if dialog.ShowModal() == wx.ID_CANCEL:
                # 如果没有选择文件，即选择取消，则打印提示信息，并回到 input_str 输入文本这里
                print("Hint: You did not select a file.\n")
                # 返回 None 表示未选择文件, 继续主循环
                continue
            input_path = dialog.GetPath()
            try:
                validate(input_path)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print("Hint: Selected toml file path:", input_str)
            # 销毁对话框
            dialog.Destroy()
            # 返回 input_path
            return input_path
        # 对应直接填写文件路径
        else:
            # 对于直接输入了路径的情况，执行验证逻辑
            try:
                validate(input_str)
            except (ValueError, FileNotFoundError) as e:
                print(str(e))
                # 继续主循环
                continue
            print("Hint: Selected toml file path:", input_str)
            # 返回 input_str
            return input_str


def save_figure(config: SubplotsConfig, spectrum_list):
    """
    保存图片
    :param config: 一个 SubplotsConfig 对象
    :param spectrum_list: 一个由 Spectrum 对象组成的 list 集合
    :return:
    """
    # 文件名初始值
    file_name = f"figure.{config.save_format}"
    i = 1
    # 首先检查当前路径是否存在以 figure.save_format 为文件名的文件
    while os.path.exists(file_name):
        # 文件名已存在，添加数字后缀
        file_name = f"figure{i}.{SAVE_FORMAT}"
        i += 1
    # 调用 draw_spectrum 方法
    fig, axs = draw_spectrum(config, spectrum_list, False)
    # 保存光谱图
    fig.savefig(file_name, dpi=config.dpi, bbox_inches="tight", pad_inches=0.2)
    print()
    print("The picture is successfully saved!")
    print()


def draw_spectrum(config: SubplotsConfig, spectrum_list, is_show):
    """
    根据 SubplotsConfig 和 Spectrum 对象绘制多子图的光谱
    :param config: 一个 SubplotsConfig 对象
    :param spectrum_list: 一个由 Spectrum 对象组成的 list 集合
    :param is_show: 是否显示图片
    """
    # 设置全局属性
    rc['font.name'] = config.font_family
    rc['title.size'] = config.font_size[2]
    rc['label.size'] = config.font_size[1]
    rc['font.size'] = config.font_size[0]
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.5
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.5
    # 确定子图的排版，如果 sup_layout 为 auto，则调用 auto_layout 方法；如果不是 auto，则直接跳过
    if config.sup_layout == "auto":
        config.sup_layout = auto_layout(len(spectrum_list))
    # 确定图像的大小，如果 figure_size 为 auto，则通过 sup_layout 属性自动生成；如果不是 auto，则直接跳过
    if config.figure_size == "auto":
        config.figure_size = (4 * config.sup_layout[0], 3 * config.sup_layout[1])
    # 创建子图和坐标轴
    fig = pplt.figure(figsize=config.figure_size, dpi=300, span=config.is_span, share=config.is_share)
    axs = fig.subplots(nrows=config.sup_layout[0], ncols=config.sup_layout[1])
    for ax, spectrum in zip(axs, spectrum_list):
        # 第一列作为 x 值，第二列作为 y 值
        x = spectrum.plot_data.iloc[:, 0]
        y = spectrum.plot_data.iloc[:, 1]
        # 绘制单曲线图
        ax.plot(x, y, color=spectrum.colors[0], linestyle=spectrum.line_style[0], label=spectrum.legend_text[0],
                linewidth=1.3)

        ax.format(
            xlabel=spectrum.x_label, ylabel=spectrum.y_label, title=spectrum.title,
            xlim=(spectrum.x_limit[0], spectrum.x_limit[1]), ylim=(spectrum.y_limit[0], spectrum.y_limit[1]),
            xminorlocator=(spectrum.x_limit[2] / 2), yminorlocator=(spectrum.y_limit[2] / 2)
        )

        # 如果开启显示图例，则执行下面的代码
        if spectrum.is_legend:
            # 显示图例
            ax.legend(loc='best', ncols=1, fontweight='bold', fontsize=12.5, frame=False, bbox_to_anchor=(0.95, 0.96))
        # 如果开启显示 Zero 轴，则执行下面的代码
        if spectrum.is_zero:
            # 显示 Zero 轴
            ax.axhline(y=0, color='black', linewidth=1.25)

    # 设置一个标志，根据 config 判断是否开启子图的序号
    if config.is_serial:
        serial_flag = "(a)"
    else:
        serial_flag = False

    axs.format(grid=False, abc=serial_flag, abcloc="ul")

    # 如果 is_show = True，则调用 fig.show()
    if is_show:
        fig.show()

    return fig, axs


def show_menu(config: SubplotsConfig):
    """
    展示主页面菜单，没有实现逻辑
    :return:
    """
    print(" \"q\": Exit program gracefully\t \"r\": Load a new file")
    print("********************************************************")
    print("****************** Main function menu ******************")
    print("********************************************************")
    print(f"-4 Set dpi of saving spectrum, current: {config.dpi}")
    print(f"-3 Showing the serial of subplots, current: {config.is_serial}")
    print(f"-2 Set whether to share axis ticks , current: {config.is_span}")
    print(f"-1 Set whether to share axis labels, current: {config.is_share}")
    print("0 Plot spectrum! But the effect of direct drawing is very poor, please save directly!")
    print("1 Save graphical file of the spectrum in current folder")
    print(f"2 Set font family of the spectrum, current: {config.font_family}")
    print(f"3 Set font size of the spectrum, current: {config.font_size}")
    print(f"4 Set figure size of spectrum file, current: {config.figure_size}")
    print(f"5 Set format of saving spectrum file, current: {config.save_format}")


def set_dpi(config: SubplotsConfig):
    """
    修改全局变量 DPI
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global DPI
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    DPI = input("Please input dpi of saving spectrum, eg. 300\n")
    if DPI.lower() == "r":
        return
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.dpi = float(DPI)
    print("Setting successful!\n")


def set_serial(config: SubplotsConfig):
    """
    修改全局变量 IS_SPAN
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global IS_SERIAL
    # 修改全局变量的值，取反操作
    IS_SERIAL = not IS_SERIAL
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.is_share = IS_SERIAL


def set_span(config: SubplotsConfig):
    """
    修改全局变量 IS_SPAN
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global IS_SPAN
    # 修改全局变量的值，取反操作
    IS_SPAN = not IS_SPAN
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.is_share = IS_SPAN


def set_share(config: SubplotsConfig):
    """
    修改全局变量 IS_SHARE
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global IS_SHARE
    # 修改全局变量的值，取反操作
    IS_SHARE = not IS_SHARE
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.is_share = IS_SHARE


def set_format(config: SubplotsConfig):
    """
    修改全局变量 SAVE_FORMAT，已达到修改保存图片的格式目的
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global SAVE_FORMAT
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    SAVE_FORMAT = input("Please input format of saving spectrum file, eg. png\n")
    if SAVE_FORMAT.lower() == "r":
        return
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.figure_size = SAVE_FORMAT
    print("Setting successful!\n")


def set_figsize(config: SubplotsConfig):
    """
    修改全局变量 FONT_SIZE，已达到修改字号的目的
    :param config: 一个 SubplotsConfig 对象
    """
    global FIGURE_SIZE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    size_choice = input("Please input figure size of spectrum file, eg. 8, 5\n")
    if size_choice.lower() == "r":
        return
    # 将输入的字符串值修改成一个元组对象
    FIGURE_SIZE = tuple(map(float, size_choice.split(',')))
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.figure_size = FIGURE_SIZE
    print("Setting successful!\n")


def set_fontsize(config: SubplotsConfig):
    """
    修改全局变量 FONT_SIZE，已达到修改字号的目的
    :param config: 一个 SubplotsConfig 对象
    """
    # 声明全局变量
    global FONT_SIZE
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_SIZE = input("Please input the font size that you want to set: \n")
    if FONT_SIZE.lower() == "r":
        return
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.font_size = FONT_SIZE
    print("Setting successful!\n")


def set_fontname(config: SubplotsConfig):
    """
    修改全局变量 FONT_NAME，已达到修改字体的目的
    :param config: 一个 SubplotsConfig 对象
    """
    global FONT_NAME
    # 修改全局变量的值
    print("Type \"r\": Return to main menu")
    FONT_NAME = input("Please input the font family that you want to set: \n")
    if FONT_NAME.lower() == "r":
        return
    # 将全局变量的值赋值给 SubplotsConfig 对象
    config.font_family = FONT_NAME
    print("Setting successful!\n")


def menu(config: SubplotsConfig, toml_file):
    """
    展示主程序界面，同时执行相应的逻辑
    :param config: 一个 SubplotsConfig 对象
    :param toml_file: toml 文件的路径
    """
    # 读取 toml 文件，根据 toml 文件得到 spectrum_list
    spectrum_list = load_toml(toml_file)
    while True:
        # 展示主程序页面
        show_menu(config)
        # 接受用户的指令，并根据用户的指令
        choice = input()
        # 如果输入 0，则按照当前参数绘制 Spectrum，调用 draw_spectrum() 方法
        if choice == "0":
            draw_spectrum(config=config, spectrum_list=spectrum_list, is_show=True)
            continue
        # 如果输入 1，按照当前参数绘制的 Spectrum 保存图片，调用 save_figure() 方法
        elif choice == "1":
            save_figure(config=config, spectrum_list=spectrum_list)
        # 如果输入 2，则调用 set_fontname 修改绘制图片的字体
        elif choice == "2":
            set_fontname(config)
        # 如果输入 3，则调用 set_fontsize 修改绘制图片的字号
        elif choice == "3":
            set_fontsize(config)
        # 如果输入 4，则调用 set_figsize 修改绘制图片的大小
        elif choice == "4":
            set_figsize(config)
        # 如果输入 5，则调用 set_format 修改保存图片的格式
        elif choice == "5":
            set_format(config)
        # 如果输入 -1，设置是否启动共用坐标轴标签
        elif choice == "-1":
            set_share(config)
        # 如果输入 -2，设置是否启动共用坐标轴刻度
        elif choice == "-2":
            set_span(config)
        # 如果输入 -3，设置是否显示子图的序号
        elif choice == "-3":
            set_serial(config)
        # 如果输入 -4，则调用 set_dpi 修改保存图片的分辨率
        elif choice == "-4":
            set_dpi(config)
        # 如果输入 q 则退出程序
        elif choice.lower() == "q":
            print()
            print("The program has already terminated!")
            print("Thank you for your using! Have a good time!")
            exit()
        # 如果输入 r 则重新加载一个新的 toml 文件
        elif choice.lower() == "r":
            toml_file = select_file()
            spectrum_list = load_toml(toml_file)
            continue
        # 如果输入的内容不符合要求，提示按下空格重新选择。
        else:
            print()
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")


def main():
    # 初始化一个 SubplotsConfig 对象，之后的操作都是操作这个 SubplotsConfig 对象
    config = SubplotsConfig(font_family=FONT_NAME, font_size=FONT_SIZE, figure_size=FIGURE_SIZE,
                            is_serial=IS_SERIAL,
                            dpi=DPI, sup_layout=LAYOUT, save_format=SAVE_FORMAT, is_share=IS_SHARE, is_span=IS_SPAN)
    # 命令行运行方式
    if len(sys.argv) > 1:
        # 处理命令行参数
        arg = sys.argv[1]
        # 创建 ArgumentParser 对象
        parser = argparse.ArgumentParser(prog='pysub', add_help=False,
                                         description='pySubplots -- A python script for plotting multiple subplots.')
        # 添加 -h 参数
        parser.add_argument('--help', '-h', action='help', help='Show this help message and exit')
        # 添加版权信息和参数
        parser.add_argument('--version', '-v', action='version', help='Show the version information',
                            version=VERSION.version)
        # 添加输入文件参数
        parser.add_argument('input', type=str, help='toml file')

        # 解析参数
        args = parser.parse_args()
        # 处理命令行参数
        input_file = args.input
        # 展示开始界面
        show_head(VERSION)
        # 进入主程序
        menu(config=config, toml_file=input_file)
    # 否则就直接进入主程序
    else:
        # 展示开始界面
        show_head(VERSION)
        # 创建一个 wxPython 应用程序对象
        app = wx.App()
        # 选择需要解析的 toml 文件路径
        selected_file = select_file()
        # 进入主程序
        menu(config=config, toml_file=selected_file)
