新增指令 --lf, --ff, --cc, --tn
--lf: 仅执行上次未通过的测试案例
--ff: 优先执行未通过的测试案例，通过的测试案例滞后执行
--cc: 清除case_cache
--tn: 在不与其他三个命令一起使用时指的是指定任务目录即 festures文件夹下的目录
      在与lf 或 ff 指令一起使用时，指定重跑任务文件夹（case_cache下）
      在与cc 命令一起使用时，删除包含指定名称的文件夹（case_cache下）

在before_after中引入build_case函数后执行案例就会生成本次执行案例的记录
在根目录下生成case_cache目录
目录结构如下：（以本次执行案例文件夹为features/fee_test举例）
case_cache
   fee_test(保存本次执行的py文件，用于后续的--ff, --lf执行)
   fee_test_cache(保存执行结果)
   		res.txt(保存错误或跳过的测试案例原始信息包含报错详情)
   		error_case.feature（保存出错或跳过的案例原文）
   		failed_first_case.feature(保存全部案例，但是出错的测试案例在前面)
   fee_test_lf_cache(保存lf执行后结果，不执行lf命令不生成)
   		res.txt
   		error_case.feature
   		failed_first_case.feature
   fee_test_ff_cache(保存ff执行后结果，不执行ff命令不生成)
   		res.txt
   		error_case.feature
   		failed_first_case.feature
   
   
使用方法：
将cacheprovider.py放在lettuce库中
修改lettuce：__init__.py 引用：from lettuce.cacheprovider import build_case, build_failed_first_case, run_task；并将其暴露出来
修改lettuce/plugins/colored_shell_output.py 文件获取案例信息
def wp(l):
    if l.startswith("\033[1;32m"):
        l = l.replace(" |", "\033[1;37m |\033[1;32m")
    if l.startswith("\033[1;36m"):
        world.skip_flag = True
        l = l.replace(" |", "\033[1;37m |\033[1;36m")
    if l.startswith("\033[0;36m"):
        world.skip_flag = True
        l = l.replace(" |", "\033[1;37m |\033[0;36m")
    if l.startswith("\033[0;31m"):
        world.fail_flag = True
        l = l.replace(" |", "\033[1;37m |\033[0;31m")
    if l.startswith("\033[1;30m"):
        l = l.replace(" |", "\033[1;37m |\033[1;30m")
    if l.startswith("\033[1;31m"):
        world.fail_flag = True
        l = l.replace(" |", "\033[1;37m |\033[0;31m")  
  
    return l
    
    
def wrt(what):
    if six.PY2:
        if isinstance(what, unicode):
            what = what.encode('utf-8')
    if six.PY3:
        if isinstance(what, bytes):
            print(what)
            what = what.decode('utf-8')
    world.case.append(what)
    sys.stdout.write(what)
    
修改run.py:  from lettuce import run_task
def add_time():
    # run_task如果没有指定--tn --task_name 时，执行输入的，如果有执行指定的
    run_path = lettuce.run_task('features/C_fee_guanghaoguojiyouhua')
    base_path = os.path.join(os.path.dirname(os.curdir),
                             run_path)  # the path of .py and .feature
    lettuce.world.task_path = base_path
    tests_runner = HtmlRunner(base_path,
                              enable_html=True,
                              tags=("run",),

                              enable_xunit=True,
                              verbosity=4)
    tests_runner.run()