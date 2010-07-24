import sys
from cmd import Cmd
USING_READLINE = True
try:
    # For platforms without readline (i.e. Mac) use ...
    # http://pypi.python.org/pypi/readline/
    import readline
except:
    try:
        # For Windows readline support use
        # https://launchpad.net/pyreadline
        import pyreadline
    except:
        USING_READLINE = False


class CmdLine(Cmd):
    """
    Help may be requested at any point in a command by entering
    a question mark '?'.  If nothing matches, the help list will
    be empty and you must backup until entering a '?' shows the
    available options.
    Two styles of help are provided:
    1. Full help is available when you are ready to enter a
       command argument (e.g. 'show ?') and describes each possible
       argument.
    2. Partial help is provided when an abbreviated argument is entered
       and you want to know what arguments match the input
       (e.g. 'show pr?'.)
    """  
    def __init__(self):
        Cmd.__init__(self)
        if not USING_READLINE:
            self.completekey = None
        self.prompt = "#"
        self.intro  = "Python IOS-style command-line demonstration."
        
    def completecmd(self, line):
        cmd, arg, line = self.parseline(line)
        cmds = self.completenames(cmd)
        if not cmds:
            return (0, None, arg)
        return (len(cmds), cmds[0], arg)

    def completedefault(self, text, line, begidx, endidx):
        num_cmds, cmd, arg = self.completecmd(line)
        if num_cmds != 1:
            return [text]
        getattr(self, 'do_' + cmd)(False)
        return self.params.complete(arg)

    def default(self, line):
        num_cmds, cmd, arg = self.completecmd(line)
        if num_cmds == 1:
            getattr(self, 'do_' + cmd)(arg)
        elif num_cmds > 1:
            print('%% Ambiguous command:\t"{0}"'.format(cmd))
        else:
            print('% Unrecognized command\n')

    def emptyline(self):
        pass
    
    def do_help(self, arg):
        doc_strings = [ (i[3:], getattr(self, i).__doc__) 
            for i in dir(self) if i.startswith('do_') ]
        doc_strings = [ '  {0}\t{1}\n'.format(i, j) 
            for i, j in doc_strings if j is not None ]
        print('Commands:\n{0}'.format(''.join(doc_strings)))

    def do_exit(self, arg):
        return True

    def precmd(self, line):
        if line.strip() == 'help':
            print(self.__doc__)
            return ''
        cmd, arg, line = self.parseline(line)
        if arg == '?':
            cmds = self.completenames(cmd)
            if cmds:
                self.columnize(cmds)
                sys.stdout.write('\n')
            return ''
        return line


class IOSCmdLine(CmdLine):

    def __init__(self):
        CmdLine.__init__(self)

    def do_show(self, arg):
        " Show running system information "
        print('Executing Show Command\n')
        print('ARGS:{0}\n'.format(arg))

if __name__ == '__main__':
    cmdLine = IOSCmdLine()
    cmdLine.cmdloop()