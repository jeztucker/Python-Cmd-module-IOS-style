from cmd_arg_parser import *
from cmd_ios_style import *

class IOSCmdLine(CmdLine):

    def __init__(self):
        CmdLine.__init__(self)

    def do_show(self, arg):
        " Show running system information "
        print('Executing Show Command\n')
        self.params = Command(arg, [
            ('inventory', 'show inventory'),
            ('inventory raw', 'Show every entity in the container hierarchy'),
        ])
        print('ARGS:{0}\n'.format(arg))

if __name__ == '__main__':
    cmdLine = IOSCmdLine()
    cmdLine.cmdloop()