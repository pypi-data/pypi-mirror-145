"""
这是“nester-wl.py”模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表，其中有可能包舍(也可能不包含)嵌套列表。
"""


def print_lol(the_list):
    """
    “这个函数取一个位置参数，名为“the_list”, 这可以是任何Python列表(也可以是包舍嵌套列表的列表)。所指定的列表中的每个数据项会(递归地)
    输出到屏幕上，各数据项各占一行。”
    :param the_list:
    :return:
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)


if __name__ == '__main__':
    movies = ["The Holy Grail", 1975, "Terry Jones & rerry Gilliam", 91,
              ["Graham Chapman",
               ["Michael Palin", "John cleese", "Terry Gi1liam", "Eric Idle", "rerry Jones"]]]

    print_lol(movies)
