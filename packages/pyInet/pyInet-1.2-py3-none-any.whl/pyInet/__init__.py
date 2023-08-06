import os, sys
path, filename = os.path.split(__file__)
"""
Add Path System and Import file main 
"""
sys.path.insert(0, path)
try:
	from main import ClassA, ClassB, SaveContext, CleanContext
except:
	from pyInet.main import ClassA, ClassB, SaveContext, CleanContext
	#except:
	#	from .main import ClassA, ClassB
	
"""def called():
	del ClassA.__class__
	del ClassB.__class__
called()



Create custom Error output, and check if file path does not exist (Root Mode)

"""

class CustomError(Exception):

    # We can override the constructor of Exception class to accomplish our own __init__.
    def __init__(self, customMessage:str = 'The number should not be more than 1 and less than -1.'):
        self.msg = customMessage
        super(CustomError, self).__init__(self.msg)

    # We can implement our custom __str__ dunder method.
    def __str__(self):
        return '%s' % (self.msg)

def error(num):
    raise CustomError(num)

		
class AcceptTools_programs():
    caller = ""
    def __init__(self):
        self.caller = path
        self.accepts = False
    def accept(self):
    	if sys.platform == "darwin":
    		self.accepts = True
    	if sys.platform.startswith("linux"):
    		if self.caller not in sys.path:
    			self.accepts = False
    		else:
	    		self.accepts = True
    	elif sys.platform.startswith("win"):
	    	if self.caller not in sys.path:
	    		sys.path.append(path)
	    		self.accepts = False
	    	else:
	    		self.accepts = True
    def excute(self):
    	self.accept()
    	if self.accepts==False: return"Path: {} does not exist".format(self.caller)

if AcceptTools_programs().excute() != "":
	pass
else:
	try:
		error("Path: {} does not exist".format(path))
	except CustomError as err:
		print(err.msg)

"Class Imported"
ClassA = ClassA
ClassB = ClassB
