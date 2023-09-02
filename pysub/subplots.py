# -*- coding: utf-8 -*-
"""
subplots.py
Briefly describe the functionality and purpose of the file.

This is a Main function file!

This file is part of pySubplots.
pySubplots is a python script for plotting multiple subplots.

@author:
Kimariyb (kimariyb@163.com)

@license:
Licensed under the MIT License.
For details, see the LICENSE file.

@Data:
2023-09-02
"""
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

# 获取当前文件被修改的最后一次时间
time_last = os.path.getmtime(os.path.abspath(__file__))
# 全局的静态变量
__version__ = "1.2.0"
__developer__ = "Kimariyb, Ryan Hsiun"
__address__ = "XiaMen University, School of Electronic Science and Engineering"
__website__ = "https://github.com/kimariyb/py-subplots"
__release__ = str(datetime.fromtimestamp(time_last).strftime("%b-%d-%Y"))


class SubConfig:
    """
    绘制多子图时所需要的配置类

    Attributes:
        sub_num(int): The number of subplots.
        font_family (str): Font family.
        font_size (list): Font sizes for normal, label, and title fonts.
        figure_size (tuple): Size of the figure.
        sup_layout (list): Layout of subplots.
        save_dpi (float): Resolution for saved files.
        save_format (str): Format for saved files.
        is_serial (bool): Whether to display serial numbers.
        is_share (bool): Whether to share axes.
        is_span (bool): Whether to share axis scales.
    """

    def __init__(self, **kwargs):
        # 构造函数逻辑

        # 子图的数量，必须为 int
        self.sub_num = kwargs.get('sub_num')

        # 全局的字体 string，默认为 Arial
        self.font_family = kwargs.get('font_family', 'Arial')

        # 字体字号；分为常规字号以及标签字号，必须为 list[float, float]，默认为 [10.5, 12]
        self.font_size = kwargs.get('font_size', [10.5, 12])
        if self.font_size is not None and (not isinstance(self.font_size, list) or len(self.font_size) != 2):
            raise ValueError("font_size must be a list of three floats [regular_size, label_size]")

        # 图像大小，必须为 tuple(float, float)，默认为 (10, 10)
        self.figure_size = kwargs.get('figure_size', (10, 10))
        if self.figure_size is not None and (not isinstance(self.figure_size, tuple) or len(self.figure_size) != 2):
            raise ValueError("figure_size must be a tuple of two floats (width, height)")

        # 子图的排版，必须为 list[int, int]，默认调用 auto_layout() 方法
        if 'sup_layout' in kwargs:
            self.sup_layout = kwargs.get('sup_layout')
            if self.sup_layout is not None and (not isinstance(self.sup_layout, list) or len(self.sup_layout) != 2):
                raise ValueError("sup_layout must be a list of two ints (columns, rows)")
        else:
            self.sup_layout = self.auto_layout()

        # 保存图片的 dpi，默认为 400
        self.save_dpi = kwargs.get('save_dpi', 400)
        # 保存图片的格式，默认为 PNG
        self.save_format = kwargs.get('save_format', 'png')
        # 是否显示序号，默认为 True
        self.is_serial = kwargs.get('is_serial', True)
        # 是否共享，默认为 True
        self.is_share = kwargs.get('is_share', True)
        self.is_span = kwargs.get('is_span', True)

    def __str__(self):
        """
        返回 SubConfig 对象的字符串表示形式
        """
        attributes = [
            f"sub_num={self.sub_num}",
            f"font_family='{self.font_family}'",
            f"font_size={self.font_size}",
            f"figure_size={self.figure_size}",
            f"sup_layout={self.sup_layout}",
            f"save_dpi={self.save_dpi}",
            f"save_format='{self.save_format}'",
            f"is_serial={self.is_serial}",
            f"is_share={self.is_share}",
            f"is_span={self.is_span}"
        ]
        return "SubConfig(\n  " + ",\n  ".join(attributes) + "\n)"

    def auto_layout(self):
        """
        Automatic layout function that determines the arrangement based on the number of data points.
        The layout algorithm factors the length of a data collection. For example, if the length is 9, it can be factored into 3 and 3, so it returns [3, 3].

        Examples:
            If the length is 15, it can be factored into 5 and 3, so it returns [5, 3].
            Note that if a number can only be factored into two numbers, the larger number comes first.
            If a number is a prime number and can only be factored into n and 1, it returns [n, 1].

        Args:
            self.sub_num (int): The length of the data collection.

        Returns:
            list[int, int]: A list that represents the layout information, such as [3, 3].
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

        if is_prime(self.sub_num):
            # 如果数据集合长度为质数，则按照 [n, 1] 的排版方式
            layout_list = [self.sub_num, 1]
        else:
            # 因式分解，找到能整除数据集合长度的两个因子
            for i in range(int(math.sqrt(self.sub_num)), 1, -1):
                if self.sub_num % i == 0:
                    layout_list = [self.sub_num // i, i]
                    break

        return layout_list

    def set_save_dpi(self):
        """
       设置 SubConfig 的 save_dpi 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input dpi of saving subplots, eg. 300\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 save_dpi
        self.save_dpi = float(your_input)
        print("Setting successful!\n")

    def toggle_serial(self):
        """
       设置 SubConfig 的 is_serial 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off drawing of the serial")
        print("1 Turn on drawing of the serial")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_serial = False
        elif your_input == "1":
            self.is_serial = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def toggle_span(self):
        """
       设置 SubConfig 的 is_span 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off sharing axis ticks")
        print("1 Turn on sharing axis ticks")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_span = False
        elif your_input == "1":
            self.is_span = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def toggle_share(self):
        """
       设置 SubConfig 的 is_share 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        print("0 Turn off sharing axis labels")
        print("1 Turn on sharing axis labels")
        your_input = input("Please enter the option of your choice:\n")
        if your_input.lower() == "r":
            return
        elif your_input == "0":
            self.is_share = False
        elif your_input == "1":
            self.is_share = True
        else:
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")
        print("Setting successful!\n")

    def set_format(self):
        """
       设置 SubConfig 的 save_format 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input format of saving subplots file, eg. png\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 save_format
        self.save_format = your_input
        print("Setting successful!\n")

    def set_figure_size(self):
        """
       设置 SubConfig 的 figure_size 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input figure size of subplots file, eg. 8,5\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 figure_size
        self.figure_size = tuple(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_font_size(self):
        """
        设置 SubConfig 的 font_size 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input the font size that you want to set, eg. 10.5,12\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 font_family
        self.font_size = list(map(float, your_input.split(',')))
        print("Setting successful!\n")

    def set_font_family(self):
        """
        设置 SubConfig 的 font_family 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input the font family that you want to set: \n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 font_family
        self.font_family = your_input
        print("Setting successful!\n")

    def set_layout(self):
        """
       设置 SubConfig 的 sup_layout 属性

        Returns:
            None
        """
        print("Type \"r\": Return to main menu")
        your_input = input("Please input layout of subplots, eg. 3,3\n")
        if your_input.lower() == "r":
            return
        # 将输入的内容赋值给 sup_layout
        self.sup_layout = list(map(int, your_input.split(',')))
        print("Setting successful!\n")


class Spectrum:
    """
    用于绘制图像的 Spectrum 类，这个类必须从 toml 文件中读取

    Attributes:
        x_limit (list): X轴坐标的最小值、最大值和间隔，例如 [0, 4000, 500]，列表类型。
        y_limit (list): Y轴坐标的最小值、最大值和间隔，例如 [0, 3000, 1000]，列表类型。
        x_label (str): X轴标签，字符串类型。
        y_label (str): Y轴标签，字符串类型。
        colors (list or str): 曲线的颜色，可以是由字符串组成的列表类型，也可以是字符串类型。
        line_style (list or str): 曲线的风格，可以是由字符串组成的列表类型，也可以是字符串类型。
        legend_text (list or str): 图例的文本，可以是由字符串组成的列表类型，也可以是字符串类型。
        is_zero (bool): 是否启用零轴，布尔类型。
        is_legend (bool): 是否显示图例，布尔类型。
        plot_data (DataFrame): 绘图数据，一个DataFrame对象。
    """

    def __init__(self, **kwargs):
        """
        初始化 Spectrum 对象。

        Args:
            **kwargs: 关键字参数，包含 x_limit、y_limit、x_label、y_label、colors、line_style、legend_text、is_zero、is_legend 和 plot_data。
        """
        # 构造函数逻辑
        # 如果未提供 x_limit，默认为 [0, 1, 0.1]
        self.x_limit = kwargs.get('x_limit', [0, 1, 0.1])
        # 如果未提供 y_limit，默认为 [0, 1, 0.1]
        self.y_limit = kwargs.get('y_limit', [0, 1, 0.1])
        # 如果未提供 x_label，默认为 'X'
        self.x_label = kwargs.get('x_label', 'X')
        # 如果未提供 y_label，默认为 'Y'
        self.y_label = kwargs.get('y_label', 'Y')
        # 如果未提供 colors，默认为 'blue'
        self.colors = kwargs.get('colors', 'blue')
        # 如果未提供 line_style，默认为 '-'
        self.line_style = kwargs.get('line_style', '-')
        # 如果未提供 legend_text，默认为 'Curve'
        self.legend_text = kwargs.get('legend_text', 'Curve')
        # 如果未提供 is_zero，默认为 False
        self.is_zero = kwargs.get('is_zero', False)
        # 如果未提供 is_legend，默认为 True
        self.is_legend = kwargs.get('is_legend', True)
        # 不提供默认值，如果未提供 plot_data，则为 None
        self.plot_data = kwargs.get('plot_data')

    def __str__(self):
        return f"Spectrum Object:\n" \
               f"  x_limit: {self.x_limit}\n" \
               f"  y_limit: {self.y_limit}\n" \
               f"  x_label: {self.x_label}\n" \
               f"  y_label: {self.y_label}\n" \
               f"  line_style: {self.line_style}\n" \
               f"  colors: {self.colors}\n" \
               f"  legend_text: {self.legend_text}\n" \
               f"  is_legend: {self.is_legend}\n" \
               f"  is_zero: {self.is_zero}\n"


def read_path(file_path):
    """
    读取 toml 文件中 path 所指向的 txt 或 xlxs 文件的内容

    Args:
        file_path: toml 文件中 path 所表示的路径

    Returns:
        data(DataFrame): 返回一个 Pandas DataFrame 对象

    """
    file = Path(file_path)
    # 根据文件的后缀是否为 txt 或者 xlsx 判断
    if file.suffix == ".txt":
        # 如果是 Multiwfn 输出的 txt 文件，调用 Pandas 的 read_csv 方法读取
        data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    elif file.suffix == ".xlsx":
        # 读取包含光谱数据的 Excel 文件，假设文件包含一个名为 Sheet1 的表格
        data = pd.read_excel(file_path, sheet_name=0, dtype={'column_name': float})
    else:
        # 文件格式不支持
        raise ValueError("Unsupported file format.")

    return data


def read_toml(toml_file):
    """
    根据 toml 文件得到 spectrum 组成的集合

    Args:
        toml_file(str): toml 文件

    Returns:
        spectrum_list(list): 由 Spectrum 对象组成的 list 集合
    """
    # 根据 toml 文件得到 spectrum 对象
    with open(toml_file, 'r', encoding='utf-8') as file:
        spectrums = toml.load(file)

    # 获取 toml 文件的当前文件夹
    current_folder = os.path.dirname(os.path.abspath(toml_file))
    # 新建一个 list 用来存放 spectrum 对象
    spectrum_list = []
    # 解析文件内容
    for spectrum in spectrums['file']:
        # 拿到每一个 file 下的所有参数
        path = spectrum['path']
        if os.path.isabs(path):
            # 如果是绝对路径，则直接使用该路径
            data_source = path
        else:
            # 如果是相对路径，则与当前文件夹拼接
            data_source = os.path.join(current_folder, path)
        # 根据 data_source 得到数据
        plot_data = read_path(data_source)

        # 解析 toml 文件中的其他参数
        colors = spectrum['colors']
        styles = spectrum['styles']
        legend = spectrum['legend']
        xlim = spectrum['xlim']
        ylim = spectrum['ylim']
        x_label = spectrum['xlabel']
        y_label = spectrum['ylabel']
        is_zero = bool(spectrum['iszero'])
        is_legend = bool(spectrum['islegend'])

        # 初始化一个 spectrum 对象
        spectrum = Spectrum(x_limit=xlim, y_limit=ylim, x_label=x_label, y_label=y_label, colors=colors,
                            line_style=styles, legend_text=legend, is_zero=is_zero, is_legend=is_legend,
                            plot_data=plot_data)

        # 在 spectrum 追加每一个 spectrum 对象
        spectrum_list.append(spectrum)

    return spectrum_list


def validate(file):
    """
    判断输入的文件是否为 toml 文件

    Args:
        file(str): toml 文件的路径
    """
    # 首先判断输入的是否为 toml 文件，如果不是，则抛出异常。并在屏幕上打印不支持该文件
    if not file.endswith(".toml"):
        raise ValueError("Error: Unsupported file format. Only TOML files are supported.\n")

    # 判断输入的 toml 文件是否存在，如果不存在，则抛出异常。并在屏幕上打印未找到该文件
    if not os.path.isfile(file):
        raise FileNotFoundError("Error: File not found.\n")


def welcome_view():
    """显示程序的基本信息、配置信息以及版权信息。

    Returns:
        None
    """
    # 程序最后输出版本和基础信息
    print(f"pySubplots -- A python script for plotting multiple subplots.")
    print(f"Version: {__version__}, release date: {__release__}")
    print(f"Developer: {__developer__}")
    print(f"Address: {__address__}")
    print(f"pySubplots home website: {__website__}\n")
    # 获取当前日期和时间
    now = datetime.now().strftime("%b-%d-%Y, 00:45:%S")
    # 程序结束后提示版权信息和问候语
    print(f"(Copyright (c) 2023 Kimariyb. Currently timeline: {now})\n")


def select_file():
    """通过命令行或者 GUI 界面选择一个文件，这个文件必须是 toml 文件，并且满足程序所指定的 toml 文件内容

    Notes:
        1. 如果直接写入 toml 文件的绝对路径，则直接返回 toml_path
        2. 如果输入 Enter 则弹出 GUI 界面选择 toml 文件
        3. 如果输入 q 则退出整个程序

    Returns:
        toml_path(str): 返回一个 toml 文件路径
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
            print("Hint: Selected toml file path:", input_path)
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


def draw_spectrum(config: SubConfig, spectrum_list):
    """
    根据 SubConfig 对象和 Spectrum 对象组成的集合绘制多子图的图片

    Args:
        config(SubConfig): 一个 SubConfig 对象
        spectrum_list(list[Spectrum...]): 一个由 Spectrum 对象组成的 list 集合
    """
    # 设置全局属性
    rc['font.family'] = config.font_family
    rc['label.size'] = config.font_size[1]
    rc['font.size'] = config.font_size[0]
    rc['tick.width'] = 1.3
    rc['meta.width'] = 1.3
    rc['label.weight'] = 'bold'
    rc['axes.labelpad'] = 8.0
    rc['tick.labelweight'] = 'bold'
    rc['ytick.major.size'] = 4.6
    rc['ytick.minor.size'] = 2.5
    rc['xtick.major.size'] = 4.6
    rc['xtick.minor.size'] = 2.5

    # 创建子图和坐标轴
    fig = pplt.figure(figsize=config.figure_size, dpi=300, span=config.is_span, share=config.is_share)
    axs = fig.subplots(nrows=config.sup_layout[0], ncols=config.sup_layout[1])

    for ax, spectrum in zip(axs, spectrum_list):
        # 第一列作为 x 值，第二列作为 y 值
        x = spectrum.plot_data.iloc[:, 0]
        y = spectrum.plot_data.iloc[:, 1]
        # 绘制单曲线图
        ax.plot(x, y, color=spectrum.colors, linestyle=spectrum.line_style, label=spectrum.legend_text,
                linewidth=1.3)

        ax.format(
            xlabel=spectrum.x_label, ylabel=spectrum.y_label,
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

    # 文件名初始值
    save_name = f"figure.{config.save_format}"
    i = 1
    # 首先检查当前路径是否存在以 figure.save_type 为文件名的文件
    while os.path.exists(save_name):
        # 文件名已存在，添加数字后缀
        save_name = f"figure{i}.{config.save_format}"
        i += 1
    # 保存图像，保存图像的名字为 figure + save_format
    fig.savefig(save_name, dpi=300, bbox_inches="tight", pad_inches=0.2)
    # 输出保存成功的信息
    print("Saving successful!\n")


def main_view(input_file):
    """
    pySubplots 的主程序界面，这个界面是一个交互式的界面。用户可以输入指令自定义的绘制用户想要绘制的 subplots

    Args:
        input_file(str): toml 文件路径

    Returns:
        None
    """
    # 读取 toml 文件，根据 toml 文件得到 spectrum_list
    spectrum_list = read_toml(input_file)
    # 初始化一个 SubConfig 对象，之后的操作都是操作这个 SubConfig 对象
    config = SubConfig(sub_num=len(spectrum_list))

    while True:
        print(" \"q\": Exit program gracefully\t \"r\": Load a new file")
        print("********************************************************")
        print("****************** Main function menu ******************")
        print("********************************************************")
        print(f"-4 Set figure layout of subplots, current: {config.sup_layout}")
        print(f"-3 Showing the serial of subplots, current: {config.is_serial}")
        print(f"-2 Set whether to share axis ticks , current: {config.is_span}")
        print(f"-1 Set whether to share axis labels, current: {config.is_share}")
        print("0 Save graphical file of the spectrum in current folder")
        print(f"1 Set font family of the spectrum, current: {config.font_family}")
        print(f"2 Set font size of the spectrum, current: {config.font_size}")
        print(f"3 Set figure size of spectrum file, current: {config.figure_size}")
        print(f"4 Set format of saving spectrum file, current: {config.save_format}")
        print(f"5 Set dpi of saving spectrum, current: {config.save_dpi}")

        # 接受用户的指令，并根据用户的指令
        choice = input()
        # 如果输入 0，则按照当前参数绘制 Spectrum，调用 draw_spectrum() 方法
        if choice == "0":
            draw_spectrum(config=config, spectrum_list=spectrum_list)
            continue
        # 如果输入 1，调用 set_font_family() 修改字体
        elif choice == "1":
            config.set_font_family()
            continue
        # 如果输入 2，则调用 set_font_size() 修改字号
        elif choice == "2":
            config.set_font_size()
            continue
        # 如果输入 3，则调用 set_figure_size() 修改图片大小
        elif choice == "3":
            config.set_figure_size()
            continue
        # 如果输入 4，则调用 set_format() 修改保存图片格式
        elif choice == "4":
            config.set_format()
            continue
        # 如果输入 5，则调用 set_save_dpi() 修改保存图片 dpi
        elif choice == "5":
            config.set_save_dpi()
            continue
        # 如果输入 -1，设置是否启动共用坐标轴标签
        elif choice == "-1":
            config.toggle_share()
            continue
        # 如果输入 -2，设置是否启动共用坐标轴刻度
        elif choice == "-2":
            config.toggle_span()
            continue
        # 如果输入 -3，设置是否显示子图的序号
        elif choice == "-3":
            config.toggle_serial()
            continue
        # 如果输入 -4，则调用 set_layout() 修改排版
        elif choice == "-4":
            config.set_layout()
            continue
        # 如果输入 q 则退出程序
        elif choice.lower() == "q":
            print()
            print("The program has already terminated!")
            print("Thank you for your using! Have a good time!")
            sys.exit()
        # 如果输入 r 则重新加载一个新的 toml 文件
        elif choice.lower() == "r":
            toml_file = select_file()
            spectrum_list = read_toml(toml_file)
            continue
        # 如果输入的内容不符合要求，提示按下空格重新选择。
        else:
            print()
            print("Invalid input. Please press the Enter button and make a valid selection.")
            input("Press Enter to continue...\n")


def main():
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
                            version=__version__)
        # 添加输入文件参数
        parser.add_argument('input', type=str, help='toml file')

        # 解析参数
        args = parser.parse_args()
        # 处理命令行参数
        input_file = args.input
        # 展示开始界面
        welcome_view()
        # 进入主程序
        main_view(input_file=input_file)
    # 否则就直接进入主程序
    else:
        # 展示开始界面
        welcome_view()
        # 创建一个 wxPython 应用程序对象
        app = wx.App()
        # 选择需要解析的 toml 文件路径
        selected_file = select_file()
        # 进入主程序
        main_view(input_file=selected_file)


main()
