import uuid


class SiriMetaClass(type):
    def __new__(cls, name, bases, attrs):
        parent_props = []
        for base in bases:
            if hasattr(base, '_properties'):
                parent_props += base._properties
        cls_props = []
        for attr in filter(lambda a: (not a.startswith('_')) or callable(a), attrs.iterkeys()):
            if not attr in parent_props:
                cls_props.append(attr)
        attrs['_properties'] = cls_props
        return super(SiriMetaClass, cls).__new__(cls, name, bases, attrs)


class SiriObject(object):
    __metaclass__ = SiriMetaClass
    cls = ""
    group = "com.apple.ace.assistant"

    def __init__(self, **kwargs):
        self.ref_id = None
        self.ace_id = None
        self.properties = {}
        for key, val in kwargs.iteritems():
            if key in self._properties:
                val = [] if val == [] else val
                self.properties[key] = val

    def to_dict(self):
        d = {
            'class': self.cls,
            'group': self.group,
            'properties': {}
        }
        if self.ref_id:
            d['refId'] = self.ref_id
        if self.ace_id:
            d['aceId'] = self.ace_id
        props = d['properties']
        for key in self._properties:
            val = getattr(self, key)
            if isinstance(val, list):
                props[key] = []
                for el in val:
                    if hasattr(el, 'to_dict'):
                        props[key].append(el.to_dict())
                    else:
                        props[key].append(el)
            else:
                if hasattr(val, 'to_dict'):
                    props[key] = val.to_dict()
                else:
                    props[key] = val
        return d

    def make_root(self, ref_id=None, ace_id=None):
        if not ref_id:
            ref_id = str(uuid.uuid4()).upper()
        if not ace_id:
            ace_id = str(uuid.uuid4())
        self.ref_id = ref_id
        self.ace_id = ace_id


class SiriObjects(object):
    class AddViews(SiriObject):
        cls = "AddViews"
        scroll_to_top = False
        temporary = False
        dialog_phase = "Completion"
        views = []

    class Utterance(SiriObject):
        cls = "AssistantUtteranceView"
        text = ""
        speakable_text = ""
        dialog_identifier = "Misc#ident"
        listen_after_speaking = False

    class Map(SiriObject):
        cls = "MapItemSnippet"
        group = "com.apple.ace.localsearch"
        user_current_location = True
        items = []

    class Wolfram(SiriObject):
        cls = "Snippet"
        group = "com.apple.ace.answer"
        answers = []

    class Button(SiriObject):
        cls = "Button"
        text = ""
        commands = []

    class RequestCompleted(SiriObject):
        cls = "RequestCompleted"
        group = "com.apple.ace.system"


if __name__ == '__main__':
    root = SiriObjects.AddViews()
    root.make_root()
    root.views.append(SiriObjects.Utterance(text='Hello, World'))
    from pprint import pprint
    pprint(root.to_dict())
