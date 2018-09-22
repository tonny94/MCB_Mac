from Abstract.AInputSubclasses.Keyboard import CKeyboard
from Abstract.AOutputSubclasses.Screen import CScreen


class IInteractor(object):

    input = CKeyboard()
    output = CScreen()
