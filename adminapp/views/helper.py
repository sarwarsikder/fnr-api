from django.views import generic
import logging
from django.conf import settings
import os, sys, time
import inspect


class LogHelper(generic.DetailView):
    def elog(e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log = "----------- Error: " + str(exc_obj) + ", File: " + fname + ", Line: " + str(exc_tb.tb_lineno) + " ------------"
        print(log)
        logger = logging.getLogger(__name__)
        logger.debug(log)

    def efail(e):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        log = "----------- Error: " + str(exc_obj) + ", File: " + fname + ", Line: " + str(
            exc_tb.tb_lineno) + " ------------"
        print(log)

    def warn(e):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        print("\r" + "[" + str(
            os.path.split(filename)[
                1] + ", " + function_name + "()" + ", Line:" + str(
                line_number) + "]"))
        print()

    def ex_time_init(msg=""):
        settings.EX_TIME = time.time()
        settings.EX_MSG = msg
        if msg != "":
            print("{} ==> {}".format(msg, str(time.time() - settings.EX_TIME)))

    def ex_time(*args, **kwargs):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        print("{} ==> {}".format(settings.EX_MSG, str(time.time() - settings.EX_TIME) + "\t" + os.path.split(filename)[1] + " " + function_name + " " + str(line_number)))



