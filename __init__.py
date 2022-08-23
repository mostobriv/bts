
from binaryninjaui import UIContext

import binaryninja
from binaryninja.architecture import InstructionTextTokenType
from binaryninja.plugin import PluginCommand

import re

from binaryninja import log

VTABLE_NAME_PATTERN = re.compile(r"Vtable_[0-9A-Fa-f]{4,16}")

def is_valid_vtable_name(name):
    return VTABLE_NAME_PATTERN.match(name) is not None


class Logger:
    def __init__(self, session_id, name):
        if type(name) is not str:
            name = name.__class__.__name__

        self._logger = log.Logger(session_id, name)

    def debug(self, message):
        self._logger.log_debug(message)

    def info(self, message):
        self._logger.log_info(message)

    def warning(self, message):
        self._logger.log_warning(message)

    def error(self, message, exception: Exception=None):
        self._logger.log_error(message)
        if exception is not None:
            self._logger.exception(exception)

    def alert(self, message):
        self._logger.log_alert(message)


class VirtualJumpResolver:
    def __init__(self):
        pass

    def delayed_constructor(self, binary_view, hlil_instruction):
        pass

    def __call__(self, bv, hlil_instruction) -> None:
        self.logger = Logger(bv.file.session_id, self)

        context = UIContext.activeContext()
        action_handler = context.getCurrentActionHandler()
        view = context.getCurrentView()
        action_context = view.actionContext() if view is not None else action_handler.actionContext()
        token_state = action_context.token
        token = token_state.token if token_state.valid else None

        self.logger.info(f"Token: {token}")

        if token is None:
            return

        if token.type is not InstructionTextTokenType.FieldNameToken:
            return

        vtable_name = token.typeNames[0] # typeNames -> [type_name, field_name]
        virtual_function_offset = token.value


        if not is_valid_vtable_name(vtable_name):
            return

        self.logger.info(f"Detected call to {vtable_name}->{virtual_function_offset:x}")

        try:
            vtable_funcs = bv.query_metadata(vtable_name)
            self.logger.info(f"Vtable functions object: {vtable_funcs}")
            function_address = vtable_funcs.get(str(virtual_function_offset), None)
            self.logger.info(f"Retrieved address: {function_address:x}")
            if function_address is not None:
                bv.navigate(bv.view, function_address)
        except KeyError:
            pass




PluginCommand.register_for_high_level_il_instruction("BTS\\test", "Extract virtual call in HLIL from virtual table structure", VirtualJumpResolver())
# UIAction.registerAction("Resolve virtual call")
# UIActionHandler.globalActions().bindAction("Resolve virtual call", UIAction(resolve_virtual_call))
# Menu.mainMenu("Tools").addAction("Resolve virtual call", "BTS")
