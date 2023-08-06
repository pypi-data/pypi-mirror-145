# coding=utf-8
import shutil
from lettuce import world
from  optparse import  OptionParser
import os
import sys


world.fail_flag = False
world.skip_flag = False
world.re_flag = str()
world.case = list()
world.task_path = str()
world.task_name = str()
world.cache_path = str()


def wrapped():
    parser = OptionParser()
    parser.add_option("--lf", "--last-failed", dest="last_failed", action="store_true",
                      help="仅执行上次失败的测试案例")
    parser.add_option("--ff", "--failed-first", dest="failed_first", action="store_true",
                      help="优先执行上次失败的测试案例")
    parser.add_option("--cc", "--clear-cache", dest="clear_cache", action="store_true",
                      help="清除当前的执行缓存")
    # parser.add_option("--etn", "--error-task-name", dest="error_task_name",
    #                   help="指定需要运行的任务名称")
    parser.add_option("--tn", "--task-name", dest="task_name",
                      help="指定需要运行的任务名称")

    (options, args) = parser.parse_args()
    if options.clear_cache:
        if options.task_name:
            for i in os.listdir('./case_cache'):
                if options.task_name in i:
                    clear_cache(f'./case_cache/{i}')
        else:
            clear_cache('./case_cache')
    if options.task_name:
        world.task_name = options.task_name
    if options.last_failed:
        world.re_flag = 'lf'
    if options.failed_first:
        world.re_flag = 'ff'


def run_task(task_name: str) ->str:
    mkdir_cache()
    name = task_name.split('/')[-1]
    if world.task_name:
        task_name =  world.task_name
    else:
        task_name = name
    if world.re_flag:
        dir_path = 'case_cache'
        if world.re_flag == 'lf':
            # 清除上一次的执行缓存
            clear_cache(f'./case_cache/{task_name}_lf_cache')
            # 根据类型复制案例文件
            shutil.copyfile(f'./case_cache/{task_name}_cache/error_case.feature',
                            f'./case_cache/{task_name}/task.feature')
            world.cache_path = f'./case_cache/{task_name}_lf_cache'
        if world.re_flag == 'ff':
            # 清除上一次的执行缓存
            clear_cache(f'./case_cache/{task_name}_ff_cache')
            # 根据类型复制案例文件
            shutil.copyfile(f'./case_cache/{task_name}_cache/failed_first_case.feature',
                            f'./case_cache/{task_name}/task.feature')
            world.cache_path = f'./case_cache/{task_name}_ff_cache'
    else:
        # 清除上一次的执行缓存
        for i in [f'{task_name}', f'{task_name}_cache']:
            path = f'./case_cache/{i}'
            clear_cache(path)
        dir_path = 'features'
        world.cache_path = f'./case_cache/{task_name}_cache'
    if not os.path.exists(world.cache_path):
        os.mkdir(world.cache_path)
    return f'{dir_path}/{task_name}'


def mkdir_cache():
    if not os.path.exists('./case_cache'):
        os.mkdir('./case_cache')


def get_case_py_file(path):
    task_name = world.task_path.split('/')[-1]
    shutil.copytree(path, f'./case_cache/{task_name}', symlinks=False, ignore=None)
    for root, dirs, files in os.walk(f'./case_cache/{task_name}'):
        for i in files:
            if '.feature' in i:
                os.remove(f'./case_cache/{task_name}/{i}')
    


def clear_cache(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=False, onerror=None)


# def build_case():

    # _case = world.case[:]
    # temp_list = list()
    # for i in _case:
    #     a = i.replace("\033[1;37m", '')
    #     a = a.replace("\033[1;32m", '')
    #     a = a.replace("\033[1;30m", '')
    #     a = a.replace("\033[0m", '')
    #     a = a.replace("\033[A", '')
    #     a = a.replace("\033[0;36m", '')
    #     if a in temp_list:
    #         pass
    #     else:
    #         temp_list.append(a)
    #         if world.fail_flag or world.skip_flag:
    #             # 收集错误信息，保存在结果文件
    #             with open('res.txt', 'a+', encoding='utf8') as f:
    #                 f.write(f'{a}\n')
    #             # 收集错误案例详情，支持-lf指令执行上次失败的案例
    #             with open('./case_cache/error_case.feature', 'a+', encoding='utf8') as c:
    #                 for j in temp_list:
    #                     if "\033[0;31m" not in j and "\033[1;31m" not in j:
    #                         if "#" in j:
    #                             c.write(j.split('#')[0].rstrip() + '\n')
    #                         elif "|" in j:
    #                             c.write(j)
    #             world.fail_flag = False
    #             world.skip_flag = False
    #         else:
    #             # 创建临时文件，此处存放执行通过的案例，如果存在执行失败的案例此处临时文件会与错误案例文件合并，生成新案例文件,支持-ff指令优先执行上次执行失败的案例
    #             with open('./case_cache/temp_case.feature', 'a+', encoding='utf8') as t:
    #                 t.write(f'{a}\n')
    # world.case = []


def build_case():

    with open(f'{world.cache_path}/res.txt', 'a+', encoding='utf8') as f:
        with open(f'{world.cache_path}/error_case.feature', 'a+', encoding='utf8') as c:
            with open(f'{world.cache_path}/temp_case.feature', 'a+', encoding='utf8') as t:
                _case = world.case[:]
                temp_list = list()
                for i in _case:
                    a = i.replace("\033[1;37m", '')
                    a = a.replace("\033[1;32m", '')
                    a = a.replace("\033[1;30m", '')
                    a = a.replace("\033[0m", '')
                    a = a.replace("\033[A", '')
                    a = a.replace("\033[0;36m", '')
                    if not a.startswith("Feature"):
                        if a in temp_list:
                            pass
                        else:
                            temp_list.append(a)
                            if world.fail_flag is True or world.skip_flag is True:
                                # 收集错误信息，保存在结果文件
                                f.write(f'{a}\n')
                                # 收集错误案例详情，支持-lf指令执行上次失败的案例
                                if "\033[0;31m" not in a and "\033[1;31m" not in a:
                                    if "#" in a:
                                        c.write(a.split('#')[0].rstrip() + '\n')
                                    elif "|" in a:
                                        c.write(a)
                            else:
                                # 创建临时文件，此处存放执行通过的案例，如果存在执行失败的案例此处临时文件会与错误案例文件合并，
                                # 生成新案例文件,支持-ff指令优先执行上次执行失败的案例
                                if "#" in a:
                                    t.write(a.split('#')[0].rstrip() + '\n')
                                elif "|" in a:
                                    t.write(a)

    world.fail_flag = False
    world.skip_flag = False
    world.case = []


def build_failed_first_case():
    # 合并失败文件与通过文件
    if os.path.exists(f'{world.cache_path}/error_case.feature'):
        with open(f'{world.cache_path}/failed_first_case.feature', 'a+', encoding='utf8') as f:
            with open(f'{world.cache_path}/error_case.feature', 'r+', encoding='utf8') as c:
                with open(f'{world.cache_path}/temp_case.feature', 'r+', encoding='utf8') as t:
                    temp = c.readlines()
                    temp_b = t.readlines()
                    f.write("Feature: failed-first-case\n")
                    f.writelines(temp + temp_b)
        with open(f'{world.cache_path}/error_case.feature', 'w+', encoding='utf8') as u:
            u.write("Feature: error-case\n")
            u.writelines(temp)
    if not world.re_flag:
        get_case_py_file(world.task_path)
    os.remove(f'{world.cache_path}/temp_case.feature')
    
    
wrapped()
mkdir_cache()
