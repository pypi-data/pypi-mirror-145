class MessageElement(object):
    pass


class Hr(MessageElement):
    pass


class Markdown(MessageElement):
    content: str

    def __init__(self, content: str):
        self.content = content


class Note(MessageElement):
    content: str

    def __init__(self, content: str):
        self.content = content


class MarkdownAt(MessageElement):
    user_id: str

    def __init__(self, user_id: str):
        self.user_id = user_id


class Confirm(MessageElement):
    title: str
    content: str

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class Button(MessageElement):
    button_text: str
    button_type: str
    button_id: str
    confirm: Confirm

    def __init__(self, button_text: str, button_type: str, button_id: str, confirm: Confirm):
        self.button_text = button_text
        self.button_type = button_type
        self.button_id = button_id
        self.confirm = confirm


class TextAndButton(MessageElement):
    text: str
    button: Button

    def __init__(self, text: str, button: Button):
        self.text = text
        self.button = button


class Option(object):
    text: str
    value: str

    def __init__(self, text: str, value: str):
        self.text = text
        self.value = value


class Options(MessageElement):
    place_holder: str
    option_id: str
    option_type: str
    options: list
    confirm: Confirm

    def __init__(self, place_holder: str, option_id: str, option_type: str, options: list, confirm: Confirm):
        self.place_holder = place_holder
        self.option_id = option_id
        self.option_type = option_type
        self.options = options
        self.confirm = confirm


class TextAndOptions(MessageElement):
    text: str
    options: Options

    def __init__(self, text: str, options: Options):
        self.text = text
        self.options = options
