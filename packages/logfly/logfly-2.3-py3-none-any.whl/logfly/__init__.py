#####################
# Author: Yuki Sui
# Date: 2022-4-1
#####################

import time
import shutil
import os
from pathlib import Path
try:
    from colorama import init
    __colorama_init__ = True
except Exception:
    __colorama_init__ = False
    pass

if __colorama_init__ == True:
    init(autoreset=True)
else:
    pass

__version__ = '2.3'


def create_or_check_file(pathorfile, name, warning='yes'):
    try:
        if pathorfile == 'file':
            if not os.path.exists(name):
                with open(name, 'w', encoding='utf-8') as f:
                    f.write('')
                    f.close()
                    write_log('logfly-log', 'CLI', 'info', 'File ' + name + ' created!')
        elif pathorfile == 'path':
            if not os.path.exists(name):
                os.makedirs(name)
                write_log('logfly-log', 'CLI', 'info', 'Path ' + name + ' created!')
        else:
            raise ParameterERROR('function create_or_check_file Parameter error! pathorfile must be "file" or "path"! ')
        if warning == 'yes':
            write_log('logfly-log', 'CLI', 'warning', 'File(path) ' + name + ' already exists!')
        elif warning == 'no':
            pass
        else:
            raise ParameterERROR('function create_or_check_file Parameter error! warning must be "yes" or "no"! ')
    except Exception as e:
        linenum = e.__traceback__.tb_lineno
        error(e, linenum)


def create_log_folder(folder_name, hidden='no'):
    dirs = '.\\logs\\'
    dirs2 = '.\\logs\\' + folder_name + '\\' + get_time('date') + '\\'
    dirs3 = str(Path.home()) + '\\.1o9f1y\\' + folder_name + '\\' + get_time('date') + '\\'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    else:
        pass
    if not os.path.exists(dirs2):
        os.makedirs(dirs2)
    if hidden == 'yes':
        if not os.path.exists(dirs3):
            os.makedirs(dirs3)
        else:
            pass
    else:
        pass


def get_time(flag):
    try:
        if flag == 'datetime':
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elif flag == 'date':
            return time.strftime("%Y-%m-%d", time.localtime())
        elif flag == 'times':
            return time.strftime("%H:%M:%S", time.localtime())
        elif flag == 'datetimefile':
            return time.strftime("%Y%m%d%H%M%S", time.localtime())
        elif flag == 'timestamp':
            return time.time()
        else:
            raise ParameterERROR('function get_time Parameter error! flag must be "datetime", "date", "times", '
                                 '"datetimefile","timestamp"! ')
    except Exception as e:
        linenum = e.__traceback__.tb_lineno
        error(e, linenum)


def time_transfer(time_stamp, flag='timestamp2datetime'):
    try:
        if flag == 'timestamp2datetime':
            if len(str(time_stamp)) == 10:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
            elif len(str(time_stamp)) == 13:
                return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp / 1000))
            else:
                raise ParameterERROR('function time_transfer Parameter error! time_stamp must be 10 bits or 13 bits! ')
        elif flag == 'datetime2timestamp':
            return time.mktime(time.strptime(time_stamp, "%Y-%m-%d %H:%M:%S"))
        else:
            raise ParameterERROR('function time_transfer Parameter error! flag must be "timestamp2datetime" or '
                                 '"datetime2timestamp"! ')
    except Exception as e:
        linenum = e.__traceback__.tb_lineno
        error(e, linenum)


# noinspection PyTypeChecker
def write_log(name, position, level, message, mode='add',
              folder_name='default-log', hidden='no', color='yes', str_message='yes'):
    global LOGFILE, LOGFILE2, logfolder, logfolder_hidden, LOGFILE_hidden
    try:
        create_log_folder(folder_name)
        if str_message == 'yes':
            message = str(message)
        elif str_message == 'no':
            pass
        else:
            mesg = str(message) + '\r\n\r\n'
            print(mesg)
            raise ParameterERROR('function write_log Parameter error! str_message must be "yes" or "no"! ')
        if hidden == "no":
            logfolder = '.\\logs\\' + folder_name + '\\' + get_time('date') + '\\'
        elif hidden == 'yes':
            logfolder = '.\\logs\\' + folder_name + '\\' + get_time('date') + '\\'
            logfolder_hidden = str(Path.home()) + '\\.1o9f1y\\' + folder_name + '\\' + get_time('date') + '\\'
            create_log_folder(folder_name, hidden)
        else:
            mesg = str(message) + '\r\n\r\n'
            print(mesg)
            raise ParameterERROR('function write_log Parameter error! hidden must be "no" or "yes"! ')
        if mode == 'add':
            LOGFILE_hidden = name + '-' + get_time('date') + '.log'
            LOGFILE = logfolder + name + '-' + get_time('date') + '.log'
        elif mode == 'new':
            LOGFILE_hidden = name + '-' + get_time('datetimefile') + '.log'
            LOGFILE = logfolder + name + '-' + get_time('datetimefile') + '.log'
        else:
            mesg = str(message) + '\r\n\r\n'
            print(mesg)
            raise ParameterERROR('function write_log Parameter error! mode must be "add" or "new"! ')
        if position == 'CLI':
            if color == 'no':
                print(name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            elif color == 'yes':
                LogFlyMessage = name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + \
                                '\r\n '
                if __colorama_init__ == True:
                    if str.upper(level) == 'INFO':
                        print(f'\033[0;34m{LogFlyMessage}\033[0m')
                    elif str.upper(level) == 'WARNING':
                        print(f'\033[0;33m{LogFlyMessage}\033[0m')
                    elif str.upper(level) == 'ERROR':
                        print(f'\033[0;31m{LogFlyMessage}\033[0m')
                    else:
                        print(f'\033[0;37m{LogFlyMessage}\033[0m')
                else:
                    print(LogFlyMessage)
            else:
                mesg = str(message) + '\r\n\r\n'
                print(mesg)
                raise ParameterERROR('function write_log Parameter error! color must be "yes" or "no"! ')
        elif position == 'file':
            if mode == 'add':
                File = open(LOGFILE, 'a', newline='', encoding='utf-8')
                File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                File.close()
                if hidden == 'yes':
                    LOGFILE2 = logfolder_hidden + LOGFILE_hidden
                    File = open(LOGFILE2, 'a', newline='', encoding='utf-8')
                    File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                    File.close()
                else:
                    mesg = str(message) + '\r\n\r\n'
                    print(mesg)
                    raise ParameterERROR('function write_log Parameter error! hidden must be "no" or "yes"! ')
            elif mode == 'new':
                File = open(LOGFILE, 'w', newline='', encoding='utf-8')
                File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                File.close()
                if hidden == 'yes':
                    LOGFILE2 = logfolder_hidden + LOGFILE_hidden
                    File = open(LOGFILE2, 'a', newline='', encoding='utf-8')
                    File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                    File.close()
                elif hidden == 'no':
                    pass
                else:
                    mesg = str(message) + '\r\n\r\n'
                    print(mesg)
                    raise ParameterERROR('function write_log Parameter error! hidden must be "no" or "yes"! ')
        elif position == 'fileCLI':
            if color == 'no':
                print(name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
            elif color == 'yes':
                LogFlyMessage = name + ' ' + get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + \
                                '\r\n '
                if __colorama_init__ == True:
                    if str.upper(level) == 'INFO':
                        print(f'\033[0;34m{LogFlyMessage}\033[0m')
                    elif str.upper(level) == 'WARNING':
                        print(f'\033[0;33m{LogFlyMessage}\033[0m')
                    elif str.upper(level) == 'ERROR':
                        print(f'\033[0;31m{LogFlyMessage}\033[0m')
                    else:
                        print(f'\033[0;37m{LogFlyMessage}\033[0m')
                else:
                    print(LogFlyMessage)
            else:
                mesg = str(message) + '\r\n\r\n'
                print(mesg)
                raise ParameterERROR('function write_log Parameter error! color must be "yes" or "no"! ')
            if mode == 'add':
                File = open(LOGFILE, 'a', newline='', encoding='utf-8')
                File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                File.close()
                if hidden == 'yes':
                    LOGFILE2 = logfolder_hidden + LOGFILE_hidden
                    File = open(LOGFILE2, 'a', newline='', encoding='utf-8')
                    File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                    File.close()
                elif hidden == 'no':
                    pass
                else:
                    mesg = str(message) + '\r\n\r\n'
                    print(mesg)
                    raise ParameterERROR('function write_log Parameter error! hidden must be "no" or "yes"! ')
            elif mode == 'new':
                File = open(LOGFILE, 'w', newline='', encoding='utf-8')
                File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                File.close()
                if hidden == 'yes':
                    LOGFILE2 = logfolder_hidden + LOGFILE_hidden
                    File = open(LOGFILE2, 'a', newline='', encoding='utf-8')
                    File.write(get_time('datetime') + ' ' + '[' + str.upper(level) + ']' + ' ' + message + '\r\n')
                    File.close()
                elif hidden == 'no':
                    pass
            else:
                mesg = str(message) + '\r\n\r\n'
                print(mesg)
                raise ParameterERROR('function write_log Parameter error! mode must be "add" or "new"! ')
        else:
            mesg = str(message) + '\r\n\r\n'
            print(mesg)
            raise ParameterERROR('function write_log Parameter error! position must be "file" or "fileCLI"! ')
    except Exception as e:
        linenum = e.__traceback__.tb_lineno
        error(e, linenum, 'only print')


def mv_file(original_file_name, new_file_name, folder_name='mv_file'):
    shutil.move(original_file_name, new_file_name)
    message = 'File ' + original_file_name + ' moved to ' + new_file_name
    write_log('logfly-log', 'CLI', 'error', message, folder_name=folder_name)


def error(exp,linenum, mode='logfly'):
    if mode == 'logfly':
        logflyErrorMessage = 'ERROR occurred! at row ' + str(linenum) + '\r\n\r\n' + str(
            exp) + "\r\n\r\nplease re-check it! \r\nAnd you can see the " \
                   "manual at " \
                   "https://github.com/tinqlo/logfly "
        write_log('logfly-log', 'CLI', 'error', logflyErrorMessage)
    elif mode == 'only print':
        print('ERROR occurred!\r\n\r\n' + str(exp) + "\r\n\r\nplease re-check it! \r\nAnd you can see the "
                                                     "manual at " \
                                                     "https://github.com/tinqlo/logfly ")


class ParameterERROR(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    write_log('logfly-log', 'CLI', 'error', 'test', hidden='yes')
