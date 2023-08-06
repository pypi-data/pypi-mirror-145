'''
    TColorP.py
    print with color.
    class TColor and TColorP
'''

class TColor:
    '''
        supposed Color and method.
    '''
    method_normal=0
    method_highlight=1
    method_underline=4
    method_reverse=7

    foreground_black=30
    foreground_red=31
    foreground_green=32
    foreground_yellow=33
    foreground_blue=34
    foreground_fuchsia=35
    foreground_cyan=36
    foreground_white=37

    background_black=40
    background_red=41
    background_green=42
    background_yellow=43
    background_blue=44
    background_fuchsia=45
    background_cyan=46
    background_white=47

    def __str__(self):
        return f'''method_normal=0,method_highlight=1,method_underline=4,method_reverse=7
foreground_black=30,foreground_red=31,foreground_green=32,foreground_yellow=33,foreground_blue=34,foreground_fuchsia=35,foreground_cyan=36,foreground_white=37
background_black=40,background_red=41,background_green=42,background_yellow=43,background_blue=44,background_fuchsia=45,background_cyan=46,background_white=47
'''

class TColorP:
    def __init__(self):
        self.normalStyle = [TColor.method_normal]
        self.successStyle = [TColor.method_normal,TColor.foreground_green]
        self.warningStyle = [TColor.method_normal,TColor.foreground_yellow]
        self.errorStyle = [TColor.method_normal,TColor.foreground_red]

    def formatColor(self,style:list) -> None:
        '''
            format color,print after this function will changed as arg style.
        :param style: list of style,use TColor or number
        :return: None
        '''
        if not len(style):
            return

        method = -1
        foreground = -1
        background = -1

        for i in style:
            if i in [0,1,4,7]:
                method = i
            if i >=30 and i <= 37:
                foreground = i
            if i >= 40 and i <= 47:
                background = i

        if method == -1:
            method = 0

        if background >= 0:
            print(f'\033[{method};{foreground};{background}m',end='')
        else:
            if foreground >= 0:
                print(f'\033[{method};{foreground}m',end='')
            else:
                print(f'\033[{method}m',end='')

    def normal(self,txt:str,**args) -> None:
        '''
        print any text with normal style,default style is [method_normal].
        :param txt: text you want to print
        :param args: end arg like print(), style arg for change print style once
        :return: None
        '''
        style = args.get('style',self.normalStyle)
        self.formatColor(style)
        end = args.get('end', '\n')
        print(txt, end=end)

    def success(self,txt:str,**args) -> None:
        '''
        print any text with normal style and foreground is green,change once with style arg.
        :param txt: text you want to print
        :param args: end arg like print(),style arg for change print style once
        :return: None
        '''
        style = args.get('style',[TColor.method_normal,TColor.foreground_green])
        self.formatColor(style)
        end = args.get('end', '\n')
        print(txt, end=end)
        self.formatColor([TColor.method_normal])

    def error(self,txt:str,**args) -> None:
        '''
        print any text with normal style and foreground is red,change once with style arg
        :param txt: text you want to print
        :param args: end arg like print(),style arg for change print style once
        :return: None
        '''
        style = args.get('style',[TColor.method_normal,TColor.foreground_red])
        self.formatColor(style)
        end = args.get('end', '\n')
        print(txt, end=end)
        self.formatColor([TColor.method_normal])

    def warning(self,txt:str,**args) -> None:
        '''
        print any text with normal style and foreground is yellow,change once with style arg
        :param txt: text you want to print
        :param args: end arg like print(),style arg for change print style once
        :return: None
        '''
        style = args.get('style',[TColor.method_normal,TColor.foreground_yellow])
        self.formatColor(style)
        end = args.get('end','\n')
        print(txt,end=end)
        self.formatColor([TColor.method_normal])