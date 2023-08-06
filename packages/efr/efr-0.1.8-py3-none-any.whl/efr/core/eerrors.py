# -*- coding: utf-8 -*-
class SolutionMissing(Exception):
    def __init__(self, *args, event=None):
        super(SolutionMissing, self).__init__(*args)
        self.event = event

    def __str__(self):
        txt = '\n[SolutionMissing]: ' + "Event refused by all stations.\n"
        if self.event:
            txt += "\tEvent: " + str(self.event)
        if self.args:
            txt += "\tDetails:"
            for info in self.args:
                txt += "\n\t\t" + str(info)
        return txt



if __name__ == '__main__':
    raise SolutionMissing()
