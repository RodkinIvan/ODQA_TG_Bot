import re 

from dff.script import labels as lbl
from dff.script import conditions as cnd
from dff.script import GLOBAL, TRANSITIONS, RESPONSE, Context, Message

from load_model import model

def generated_response(ctx: Context, *args, **kwargs) -> Message:

    generated_text = model([ctx.last_request.text])[0]
    return Message(text=generated_text)

def yes_condition(ctx: Context, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(re.search(r'yes|y|of course|ofk', request.text))

def no_condition(ctx: Context, *args, **kwargs) -> bool:
    request = ctx.last_request
    return bool(re.search(r'no|n|don\'t', request.text))

def idk_condition(ctx: Context, *args, **kwargs):
    return not yes_condition(ctx, *args, **kwargs) and not no_condition(ctx, *args, **kwargs)

default_trans = {
    ('greeting_flow',"greeting_node"): cnd.exact_match(Message(text="/start")),
}


script = {
    "greeting_flow": {
        "start_node": {
            TRANSITIONS: {**default_trans},
        },
        "greeting_node": {
            RESPONSE: Message(text="Do you want me to answer your quastions? (y/n)"),
            TRANSITIONS: {
                **default_trans,
                ('generating_flow', 'gen_node'): yes_condition,
                'no_node': no_condition,
                'idk_node': idk_condition
            },
        },
        'no_node': {
            RESPONSE: Message(text='Unfortunately, I\'m too stupid to do anything else...'),
            TRANSITIONS: {
                **default_trans,
                'start_node': cnd.true()
            }
        },
        'idk_node':{
            RESPONSE: Message(text='I haven\'t clearly understood. Repeat please, but as slowly, as you can...'),
            TRANSITIONS: {
                **default_trans,
                ('generating_flow', 'gen_node'): yes_condition,
                'no_node': no_condition,
                'idk_node': idk_condition
            }
        },
        "fallback_node": {
            RESPONSE: Message(text="Please, repeat the request"),
            TRANSITIONS: {**default_trans},
        },
    },
    'generating_flow': {
        'gen_node': {
            RESPONSE: generated_response,
            TRANSITIONS: {
                **default_trans,
                lbl.repeat(): cnd.true()
            }
        }
    }
}
