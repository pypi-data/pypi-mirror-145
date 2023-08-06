class LogMachine:
    __log_list = []

    class __LOG:

        def __init__(self, current_time, result_time, result):
            self.current_time = current_time
            self.result_time = result_time
            self.result = result

        def __str__(self):
            return "[%s]\nrunning time: %.16f\nresult: %s\n" % (
                self.current_time,
                self.result_time,
                str(self.result)
            )

    @classmethod
    def add_log(cls, current_time, result_time, result):
        LogMachine.__log_list.append(LogMachine.__LOG(current_time, result_time, result))

    @classmethod
    def get_log_list(cls):
        return LogMachine.__log_list


def save_log(filename=None, directory='./'):
    from time import ctime

    if filename is None:
        filename = "-".join(ctime().split()) + ".log"

    if directory[-1] != '/':
        directory += '/'

    with open(directory + filename, mode='wt') as file:
        for log in LogMachine.get_log_list():
            file.write(str(log))
