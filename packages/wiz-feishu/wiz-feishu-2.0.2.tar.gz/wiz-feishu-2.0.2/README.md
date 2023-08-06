# wiz_feishu

```python
from wiz_message.message import Robot
from wiz_message import elements
from wiz_feishu.generator import FeishuRobotMessageGenerator
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
```