import string

class Translator:
    allchars = string.maketrans('','')
    def __init__(self, frm='', to='', delete='', keep=None):
        if len(to) == 1:
            to = to * len(frm)
        self.trans = string.maketrans(frm, to)
        if keep is None:
            self.delete = delete
        else:
            self.delete = self.allchars.translate(self.allchars, keep.translate(self.allchars, delete))
    
    def translateAction(self, s):
        # return s.translate(self.trans, self.delete)
        return s.translate(self.trans)

'''
USAGE 


1) Keeping only a given set of characters.

>>> trans = Translator(keep=string.digits)
>>> trans('Chris Perkins : 224-7992')
'2247992'
2) Deleting a given set of characters.

>>> trans = Translator(delete=string.digits)
>>> trans('Chris Perkins : 224-7992')
'Chris Perkins : -'
3) Replacing a set of characters with a single character.

>>> trans = Translator(string.digits, '#')
>>> trans('Chris Perkins : 224-7992')
'Chris Perkins : ###-####'

'''