# app/core/registry.py

class PluginRegistry:
    def __init__(self):
        self.sources = {}
        self.actions = {}

    # ---------- Register ----------
    def register_source(self, plugin_class):
        self.sources[plugin_class.name] = plugin_class()

    def register_action(self, plugin_class):
        self.actions[plugin_class.name] = plugin_class()

    # ---------- Get ----------
    def get_source(self, name):
        return self.sources.get(name)

    def get_action(self, name):
        return self.actions.get(name)
