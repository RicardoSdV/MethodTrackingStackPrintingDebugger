class Trak(object):
    # Class control
    trackOnlyClss = ()  # If empty track all if not track only those classes here named
    printStack = True
    printPath, printLine, printMeth, printCode, printLocals = True, True, False, False, True

    # Imports
    import inspect as ins

    # Strings to exclude
    localsExcl = (
        'frame',
        'stack_info',
        '__builtins__',
        '__file__',
        'Trak',
        '__package__',
    )

    methNames = (
        '__getattribute__',
        '__classNameThatDefinedMethod',
        '__callStackStr',
    )

    # Formatting
    divLine = '-------------------------------------------------------------------------------------'
    bigSpace = '\n\n\n'
    stackFormat = (', localVars: ', '', ', ln ', ', ', ', code:',)
    stackOrder = (1, 2, 3, 4, 0)

    def __getattribute__(self, methodName):
        attr = object.__getattribute__(self, methodName)
        if callable(attr):
            className = Trak.__classNameThatDefinedMethod(attr)
            if not Trak.trackOnlyClss or className in Trak.trackOnlyClss:
                print str(className) + '.' + methodName
                if Trak.printStack:
                    print Trak.__callStackStr() + Trak.bigSpace + Trak.divLine
        return attr

    @classmethod
    def __classNameThatDefinedMethod(cls, meth):
        if hasattr(meth, 'im_class'):
            for obj in cls.ins.getmro(meth.im_class):
                if meth.__name__ in obj.__dict__:
                    return obj.__name__

    @classmethod
    def __callStackStr(cls):
        stackList = []
        for frame in cls.ins.stack():
            frameObj, filePath, lineNum, methName, codeList = frame[0], frame[1], frame[2], frame[3], frame[4]
            if methName not in cls.methNames:
                locals = str({k: str(v).split(' at 0x')[0] for k, v in frameObj.f_locals.items() if k not in Trak.localsExcl and v})
                codeStr = ' '.join(line.lstrip().rstrip('\n') for line in codeList) if codeList else ''
                stackList.append(
                    '{}{}{}{}{}\n'.format(
                        filePath if cls.printPath else '',
                        ', ln ' + str(lineNum) if cls.printLine else '',
                        ', ' + methName if cls.printMeth else '',
                        ', ' + codeStr if cls.printCode and codeStr else '',
                        ', ' + locals if cls.printLocals else ''
                    ).lstrip(', ')
                )
        return ''.join(stackList)

class MyParent(object):
    j = 640

    def __init__(self):
        self.x = 69
        self.y = 32

    def parentInstanceMethod(self):
        i = self.x + self.y
        return i

    @classmethod
    def parentClassMethod(cls):
        k = cls.j**2
        return k + 210 * 2

    @staticmethod
    def parentStaticMethod():
        l = MyParent.j//10
        return l + 420


class MySon(MyParent, Trak):
    f = 32
    g = 64

    def __init__(self):
        super(MySon, self).__init__()

        self.m = 254
        self.n = 465456

    def testMeth(self, a, b):
        c = 3
        d = b + 1 + a * self.m
        e = self.compute_sum(c, d)
        parentInstanceMethodRes = self.parentInstanceMethod()
        h = self.classMethExample()
        return e + h

    @staticmethod
    def compute_sum(x, y):
        return x + y

    @classmethod
    def classMethExample(cls):
        return cls.f + cls.g


mySonInstance = MySon()
result = mySonInstance.testMeth(453, 79)
