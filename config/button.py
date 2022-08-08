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
    life_emoji_1 = client.get_emoji(1006086382147604490)
    life_emoji_3 = client.get_emoji(1006086589425909870)
    life_emoji_5 = client.get_emoji(1006086677170753576)
    eraser_emoji_1 = client.get_emoji(1006087038384222330)
    eraser_emoji_3 = client.get_emoji(1006087104440303646)
    eraser_emoji_5 = client.get_emoji(1006087158437793874)
    spin_emoji_1 = client.get_emoji(1006087362578763886)
    spin_emoji_3 = client.get_emoji(1006087466870132836)
    spin_emoji_5 = client.get_emoji(1006087510163734589)
    
    button = [
        [
            Button(style = ButtonStyle.blue, emoji = life_emoji_1, disabled = disabled_1, custom_id = "life_1"),
            Button(style = ButtonStyle.blue, emoji = life_emoji_3, disabled = disabled_2, custom_id = "life_3"),
            Button(style = ButtonStyle.blue, emoji = life_emoji_5, disabled = disabled_3, custom_id = "life_5")
        ],
        [
            Button(style = ButtonStyle.blue, emoji = eraser_emoji_1, disabled = disabled_4, custom_id = "eraser_1"),
            Button(style = ButtonStyle.blue, emoji = eraser_emoji_3, disabled = disabled_5, custom_id = "eraser_3"),
            Button(style = ButtonStyle.blue, emoji = eraser_emoji_5, disabled = disabled_6, custom_id = "eraser_5")
        ],
        [
            Button(style = ButtonStyle.blue, emoji = spin_emoji_1, disabled = disabled_7, custom_id = "spin_1"),
            Button(style = ButtonStyle.blue, emoji = spin_emoji_3, disabled = disabled_8, custom_id = "spin_3"),
            Button(style = ButtonStyle.blue, emoji = spin_emoji_5, disabled = disabled_9, custom_id = "spin_5")
        ]
    ]
    return button