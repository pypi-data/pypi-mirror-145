import os
from efr.utils import *
class Trace:
    """
    .caller: Trace的直接调用者
    一般而言，Trace的调用者才是我们关心的对象，暂称其为target
    .initial: target的调用者
    """
    def __init__(self):
        stack:list = traceback.extract_stack()
        self.caller  = stack[-2][2]
        self.initial = stack[-3][2]
        self._errs = []

    @property
    def reason(self):
        return self._errs

    def update(self, err:Exception=None, efr:object=None):
        """
        Update trace.
        :param err: Exception
        :param efr: EventFramework
        :return:
        """
        if err:
            self._errs += [err]
        if efr.log_immediate:
            efr._logger.error(self.strError(err))
        else:
            efr.quit_logs += [err]

    @staticmethod
    def strError(error):
        def _inner_recur(fr, stack):
            if fr.f_back:
                _inner_recur(fr.f_back, stack)

            _sfr = str(fr)
            index = _sfr.find('file')
            if index != -1:
                _sfr = _sfr[index:-1]
            stack += [_sfr]
        if isinstance(error, Exception):
            tr = getattr(error, 'trace', None)
            if tr:
                return tr  # + "\n\t" + str(error)
            tb = error.__traceback__
            if tb:
                fr = tb.tb_frame
                if fr:
                    stack = []
                    _inner_recur(fr, stack)

                    txt = "Exception Traceback: \n"
                    for i in range(len(stack)):
                        str_frame = stack[i]
                        txt += '  ' * (i + 1) + str_frame + "\n"
                    base = "  " * ( len(stack) + 1 )
                    txt += base + ">{} At line:{}:".format(error.__class__.__name__, fr.f_lineno) + '\n'

                    _lis  = str(error).split("\n")
                    for _line in _lis:
                        if _line:
                            txt += base + _line + '\n'

                    return txt

        return str(error)


if __name__ == '__main__':
    def target():
        tr = Trace()
        print(tr)
        print(tr.reason)

    def caller():
        target()

    caller()
