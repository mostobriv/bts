import binaryninja
from binaryninjaui import UIAction, UIActionHandler, Menu

import random

def resolve_virtual_call(context):
    token_state = action_context.token
    token = token_state.token if token_state.valid else None
    if token is None:
        return False


def is_valid_Test(context):
    if random.choice([1,2]) == 1:
        print('nope')
        return False

    print('yep')
    return True

print('test')

UIAction.registerAction("Resolve virtual call")
UIActionHandler.globalActions().bindAction("Resolve virtual call", UIAction(handle_action, is_valid_test))
Menu.mainMenu("Tools").addAction("Resolve virtual call")
