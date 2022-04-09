



class ComponentManager:
    def __init__(self, name=None):
        self._name = name
        self._components_dict = dict()

    def add_component(self, component):
        self._components_dict[component.__name__] = component
        return component

    def __getitem__(self, item):
        if item not in self._components_dict.keys():
            raise KeyError("{} does not exist in availabel {}".format(
                item, self))
        return self._components_dict[item]

    @property
    def components_dict(self):
        return self._components_dict

    @property
    def name(self):
        return self._name

TM_MODELS = ComponentManager('TM_MODELS')