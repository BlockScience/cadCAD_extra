"""
Policy(f,
       Signal('delta'),
       Signal('output'),
       args=(State('x'), 
             Parameter('alpha')),
       kwargs={"t": StateHistory[0, 1, 'x']})
       )

Policy(f,
       Signal('delta'),
       x=State('x'),
       y=Parameter('alpha'))

StateUpdate(f,
            'y',
            args=(),
            kwargs=())


PartialStateUpdateBlock(policy_1,
                        policy_2,
                        suf_1,
                        suf_2)

TimestepBlock(psub1,
              psub2,
              psub3)

Simulation(t_block,
           params,
           initial_state)


simple_run(config)
"""


from typing import NamedTuple, Dict, List, Tuple
import doctest

class ConcreteMap(NamedTuple):
    name: str
    target: str
    options: list
    order: int

Parameter = lambda name: ConcreteMap(name,
                                     'params',
                                     ['policy', 'state_update'],
                                     0)

Timestep = lambda name: ConcreteMap(name,
                                    'timestep',
                                    ['policy', 'state_update'],
                                    1)

StateHistory = lambda name: ConcreteMap(name,
                                        'state_history',
                                        ['policy', 'state_update'],
                                        2)

State = lambda name: ConcreteMap(name,
                                 'prev_state',
                                 ['policy', 'state_update'],
                                 3)

Signal = lambda name: ConcreteMap(name,
                                  'policy_input',
                                  ['state_update'],
                                  4)


def check_args(*args, option=None, target=None):
    arg_types = [(type(arg) is ConcreteMap
                 for arg in args]
    arg_options = []
       (False in arg_types)
    else:


def make_policy(function: callable, 
                *signals: Tuple[ConcreteMap],
                pos_args: Tuple[ConcreteMap]=(), 
                kw_args: Dict[str, ConcreteMap]={},
                **kwargs: Dict[str, ConcreteMap]):

    args_are_valid = check_args(*pos_args, *kwargs.values(),
                          *kwargs.values(), option='policy')
    args_are_valid &= check_args(*signals, target='policy_input')

    if not args_are_valid:
        raise Exception('') 

    def wrapped_function(*args):
        arg_map = [args[arg.order][arg.name] for arg in pos_args]
        kwarg_map = [args[arg.order][arg.name] for arg in kw_args]
        signal_map = None
        output = function(*arg_map, **kwarg_map)
        return {}
    return wrapped_function



    

    return is_valid
