from discord_components import *

async def peginator_button(client, disabled_1 = False, disabled_2 = False, disabled_3 = False, disabled_4 = False):
    emoji_2 = left_arrow = client.get_emoji(956817766176940062)
    emoji_3 = right_arrow = client.get_emoji(956817878957584404)
    emoji_1 = first_left_arrow = client.get_emoji(956817439117697024)
    emoji_4 = last_right_arrow = client.get_emoji(956817169813995530)
    button = [
        [
            Button(style=ButtonStyle.blue, emoji=emoji_1, disabled=disabled_1, custom_id="button1"),
            Button(style=ButtonStyle.blue, emoji=emoji_2, disabled=disabled_2, custom_id="button2"),
            Button(style=ButtonStyle.blue, emoji=emoji_3, disabled=disabled_3, custom_id="button3"),
            Button(style=ButtonStyle.blue, emoji=emoji_4, disabled=disabled_4, custom_id="button4")
        ]
    ]
    return button