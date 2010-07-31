import re
import sys
#import xsplicer
import logging

class Command:
    def __init__(self, arg, param_def):
        """
        Example parameter definition:
        {
            '<xsplice>': 'Rows to display',
            'cols <xsplice>': 'Columns to display', 
            'where <expr>': 'Filter expression'
        }
        """
        self.VAR_RE = re.compile(r'<.*>')
        self.params = param_def
        if arg:
            self.parse(arg)
    
    def help(self, arg):
        pass
        
    def closest_match(self, word, words):
        """
        :param word: The word to try and match
        :param words: A list of words to try and match against
        :returns: The word in the 'words' list that most closely matches the original 'word'
        :rtype: String
        """
        ch_pos = len(word)
        match = False
        while not match and ch_pos >= 0:
            list = [ (i, i[:min(len(i), ch_pos)]) for i in words ]
            match = [ i[0] for i in list if word[:ch_pos] == i[1] ]
            ch_pos -= 1
        if not match:
            print 'Unrecognized Command... type \'help\' for a list of commands.' 
            return
        if len(match) > 1:
            print 'Incomplete command... use one of the following...'
            print '  '.join(match)
            return
        print 'Found: ', match[0]
        return match[0]    
        
    def match_param_set(self, args, params):
        """
        :param args: user entered arguments
        :param params: list of parameter definitions for a single valid command format
        :returns: percentage of parameters matched for complete &  incomplete commands
        :rtype: Float
        ------------------------------------------------------------------------------
        Incomplete commands match each parameter from left to right, but may not
        contain all parameters.  Incomplete commands are considered a match.
        ------------------------------------------------------------------------------
        Function builds a string of 1's and 0's indicating whether each match was successful.
        Match only occurs when 1's are found consecutively from left to right.
        Examples: '11100' is a match, '10100' is not a match, '01111' is not a match.
        """
        num_args = len(args)
        num_params = len(params)
        if num_args > num_params:
            return
        matches = ''.join([ str(int(j.is_match(params[i]))) for i, j in enumerate(params) ])
        matches = matches.rstrip('0')
        if '0' in matches:
            return 0
        return len(matches)/num_valid_params

    def get_exact_match(self, args):
        match = False
        param_set_idx =0
        num_param_sets = len(self.params)
        num_args = len(args)
        while (not match) and (param_set_idx < num_param_sets):
            if len(self.params[param_set_idx]) == num_args:
                matches = [ self.params[param_set_idx][i].get(arg[i]) for i in num_args ]
                match = [ i for i in matches if (i is not None) ]
        return match        

    def get_literals(self):
        literals = [ i.replace('[', '').replace(']', '') for i in self.params.values() ]
        literals = [ VAR_RE.sub('', i) for i in literals ] 
        return [ i.strip() for i in literals ]
    
    def complete(self, arg):
        logging.basicConfig(filename='completer.log', level=logging.DEBUG,)
        logging.debug('\nARGS: %r' % arg)

        text = []
        args = arg.split()
        num_cmd_args = len(args)
        num_params = len(self.params)
        param_num = 0
        while param_num < num_params:
            logging.debug('PARAM #%d: %r' % (param_num, self.params[param_num]))
            param_args = self.params[param_num][0].split()
            num_param_args = len(param_args)
            #print "COUNT: ", num_cmd_args, num_param_args
            if num_cmd_args <= num_param_args:
                num_args = min(num_cmd_args, num_param_args)
                arg_num = 0
                match = True
                logging.debug('NUM ARGS: %d' % num_args)
                while arg_num < num_args:
                    logging.debug('\tARG #%d: %r' % (arg_num, args[arg_num]))
                    if not param_args[arg_num].startswith(args[arg_num]) and not param_args[arg_num].startswith('<'):
                        logging.debug('\tNO MATCH')
                        match = False
                        break
                    logging.debug('\tFOUND MATCH...')
                    arg_num += 1
                if match and not param_args[arg_num - 1].startswith('<'):
                    text.append(param_args[arg_num - 1]) 
                    #print 'MATCH', text
            param_num += 1
            #print 'PARAM_NUM', param_num
        #print 'TEXT: ', text
        if text:
            #print 'TEXT: ', text
            return text
        return [args[-1]]
    
    def complete_one(self, text, words):
        return [ i for i in words if i.startswith(text) ]        
    
    def parse(self, arg):
        #print self.params
        args = [ i.strip() for i in arg.split() ]
        print 'ARGS: ', arg

"""
    def parse(self, command, args):
        print 'PARSING'
        if args is None:
            # text completion, do not parse
            return
        # is help command?
        if args == '?':
            return
        args = args.split()
        print '%r' % args
        if not args:
            self.help(args)
            return
        if args[-1] == '?' or args[-1][-1] == '?':
            print 'HELP'
            self.help(args)
            return
        match = self.get_exact_match(args)
        if match:
            return match
        # no exact match, try to find closest match
        numered_params = enumerate(self.params)
        valid_params = [ (self.match_param_set(args, j), i) for i, j in numbered_params ]
        best_match_percent, best_match_param_num  = max(valid_params)
        if best_match_percent == 0:
            self.help(args)
        else:
            closest_matches = [ i[1] for i in valid_params if i[0] == best_match_param_num ]
            for param_num in closest_matches:
                self.help(param_num, best_match_percent)
"""        

class Param:
    def __init__(self, type_, help=''):
        valid_types = [None, 'float', 'int', 'splice', 'str', 'splice', 'xsplice']
        if type_ not in valid_types:
            sys.stderr.write('Valid Param() types = %r.\n' % valid_types)
            raise KeyError(type_)
        self.type = type_
        self.help = help
    
    def get_float(self, arg):
        try:
            return float(arg)
        except:
            return    

    def get_int(self, arg):
        try:
            return int(arg)
        except:
            return
        
    """
    def get_splice(self, arg):
        s = xsplicer.Splice()
        return s.get_values(arg)
            
    def get_xplice(self, param):
        x = xsplicer.Xsplice()
        return x.get_values(arg)
    """

    def get_value(self):
        if self.type == 'float':
            return ('float', self.get_float(arg))
        if self.type == 'int':
            return ('int', self.get_int(arg))
        #elif self.type == 'splice':
        #    return ('splice', self.get_splice(arg))
        elif self.type == 'str':
            return ('str', self.get_str(arg))
        #if self.type == 'xsplice':
        #    return ('xplice', self.get_xsplice(arg))
    
    def is_match(self, arg):
        if self.type == 'float':
            f = self.get_float(arg)
            return (f == type(0.0)) or (f == type(0))
        if self.type == 'int':
            return self.get_int(arg) == type(0)
        #elif self.type == 'splice':
        #    return self.get_splice(arg)[0] == type(0)
        elif self.type == 'str':
            return self.get_str(arg) == type('')
        #if self.type == 'xsplice':
        #    return self.get_xsplice(arg)[0] == type(0)
            
    def help(self, param_num, match_percent):
        param_num += 1
        

class Literal:
    def __init__(self, word, help=''):
        self.word = word.lower()
        self.help = help
    
    def get_value(self):
        return word
    
    def is_match(self, arg):
        return arg.lower() == self.word
                
if __name__ == '__main__':    
    cmd = CmdParser()
    user_input = rawinput('Enter Command ? ')

"""
def get_literals(self, text, line, begidx, endidx):
    if self.params is None:
        return
    text = line.split()
    word_num = len(text)
    literals = []
    for param in self.params:
        for param_num, param_item in enumerate(param):
            if param_num <= word_num:
                 
                if begidx in [param_num, None]:
                    if type(param_item) is type(Command):
                        literals.append(para_item.value)
    return [ i for i in literals(begidx) if i.startswith(text) ]
"""