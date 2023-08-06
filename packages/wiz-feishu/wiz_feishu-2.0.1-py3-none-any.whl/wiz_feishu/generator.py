from wiz_message import elements
from wiz_message.bot_client import MessageGenerator
from wiz_message.message import Message, Robot


class FeishuRobotMessageGenerator(MessageGenerator):
    @staticmethod
    def _hr():
        return {"tag": "hr"}

    @staticmethod
    def _markdown(text):
        return {"tag": "div", "text": {"tag": "lark_md", "content": text}}

    @staticmethod
    def _markdown_at(open_id):
        return FeishuRobotMessageGenerator._markdown("<at id=%s></at>" % open_id)

    @staticmethod
    def _confirm(title, content):
        return {"title": {"tag": "plain_text", "content": title}, "text": {"tag": "plain_text", "content": content}}

    @staticmethod
    def _text_and_button(text, button_text, button_type, button_id, confirm=None):
        result = FeishuRobotMessageGenerator._markdown(text)
        result['extra'] = {"tag": "button", "text": {"tag": "lark_md", "content": button_text}, "value": {"button_type": button_type, "button_id": button_id}}
        if confirm is not None:
            result['extra']['confirm'] = FeishuRobotMessageGenerator._confirm(confirm.title, confirm.content)
        return result

    @staticmethod
    def _text_and_date_picker(text, place_holder, picker_type, picker_id, confirm=None):
        result = FeishuRobotMessageGenerator._markdown(text)
        result["extra"] = {"tag": "picker_datetime", "value": {"picker_type": picker_type, "picker_id": picker_id}, "placeholder": {"tag": "plain_text", "content": place_holder}}
        if confirm is not None:
            result['extra']['confirm'] = FeishuRobotMessageGenerator._confirm(confirm.title, confirm.content)
        return result

    @staticmethod
    def _text_and_options(text, place_holder, option_type, option_id, options, confirm=None):
        result = FeishuRobotMessageGenerator._markdown(text)
        result["extra"] = {"tag": "select_static", "placeholder": {"tag": "plain_text", "content": place_holder}, "value": {"select_type": option_type, "select_id": option_id}, "options": []}
        if confirm is not None:
            result['extra']['confirm'] = FeishuRobotMessageGenerator._confirm(confirm.title, confirm.content)
        for option in options:
            result["extra"]['options'].append(option)
        return result

    @staticmethod
    def _option_item(text, value):
        return {"text": {"tag": "plain_text", "content": text}, "value": value}

    @staticmethod
    def _note(text):
        return {"tag": "note", "elements": [{"tag": "plain_text", "content": text}]}

    @staticmethod
    def _null_message(message: Robot):
        return {
            "config": {
                "wide_screen_mode": True,
                "update_multi": True
            },
            "header": {
                "template": message.template,
                "title": {
                    "content": message.title,
                    "tag": "plain_text"
                }
            },
            "elements": []
        }

    @staticmethod
    def to_message(message: Message, **kwargs):
        if not isinstance(message, Robot):
            return None
        msg = FeishuRobotMessageGenerator._null_message(message)
        for element in message.elements:
            if isinstance(element, elements.Markdown):
                msg['elements'].append(FeishuRobotMessageGenerator._markdown(element.text))
            elif isinstance(element, elements.MarkdownAt):
                msg['elements'].append(FeishuRobotMessageGenerator._markdown_at(element.user_id))
            elif isinstance(element, elements.Hr):
                msg['elements'].append(FeishuRobotMessageGenerator._hr())
            elif isinstance(element, elements.TextAndButton):
                button = element.button
                msg['elements'].append(FeishuRobotMessageGenerator._text_and_button(element.text, button.button_text, button.button_type, button.button_id, button.confirm))
            elif isinstance(element, elements.TextAndDatePicker):
                date_picker = element.date_picker
                msg['elements'].append(FeishuRobotMessageGenerator._text_and_date_picker(element.text, date_picker.placeholder, date_picker.picker_type, date_picker.picker_id, date_picker.confirm))
            elif isinstance(element, elements.TextAndOptions):
                options = element.options
                options_list = [FeishuRobotMessageGenerator._option_item(item.text, item.value) for item in options.options]
                msg['elements'].append(FeishuRobotMessageGenerator._text_and_options(element.text, options.place_holder, options.option_type, options.option_id, options_list, options.confirm))
            elif isinstance(element, elements.Note):
                msg['elements'].append(FeishuRobotMessageGenerator._note(element.text))
        return msg


if __name__ == '__main__':
    m = Robot("title", "red")
    m.add_element(elements.Note("hello"))
    m.add_element(elements.Markdown("hello"))
    m.add_element(elements.Hr())
    m.add_element(elements.MarkdownAt("ou_004b55017df575ea6182a8643bb6e53d"))
    m.add_element(elements.TextAndButton("text", elements.Button("button", "type", "id", None)))
    m.add_element(elements.TextAndButton("text", elements.Button("button", "type", "id", elements.Confirm("title", "content"))))
    m.add_element(elements.TextAndOptions("text", elements.Options("placeholder", "type", "id", [elements.OptionItem("text", "value")], elements.Confirm("title", "content"))))
    m.add_element(elements.TextAndDatePicker("text", elements.DatePicker("placeholder", "type", "id", elements.Confirm("title", "content"), )))
    FeishuRobotMessageGenerator.to_message(m, )
