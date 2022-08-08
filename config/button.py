from discord_components import *

async def peginator_button(client,
                    emoji_1 = None,
                    emoji_2 = None,
                    emoji_3 = None,
                    emoji_4 = None,
                    disabled_1 = False,
                    disabled_2 = False,
                    disabled_3 = False,
                    disabled_4 = False
                    ):
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

async def hqshop_button(client, disabled_1 = None,
                                disabled_2 = None,
                                disabled_3 = None,
                                disabled_5 = None,
                                disabled_4 = None,
                                disabled_6 = None,
                                disabled_7 = None,
                                disabled_8 = None,
                                disabled_9 = None):
    life_emoji_1 = client.get_emoji()
    life_emoji_3 = client.get_emoji()
    life_emoji_5 = client.get_emoji()
    eraser_emoji_1 = client.get_emoji()
    eraser_emoji_3 = client.get_emoji()
    eraser_emoji_5 = client.get_emoji()
    spin_emoji_1 = client.get_emoji()
    spin_emoji_3 = client.get_emoji()
    spin_emoji_5 = client.get_emoji()