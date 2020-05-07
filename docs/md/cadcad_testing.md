# Towards cadCAD Unit & Integration Testing
## A vision for how using, wrapping and testing cadCAD could be

This notebooks shows an proposal for wrapping cadCAD objects, and concrete uses of it when it comes to unit testing as well as integration with existing functions.

## cadCAD objects

The key for doing intuitive unit and integration testing on cadCAD simulations is to build objects that represents all objects that are used by it. On this section, I'll propose the callable definitions of their constructors as well as an hypothetical docstrings.

### Simulation objects

#### Simulation

```python
Simulation(timestep_block: TimestepBlock,
           genesis_state: Dict[str, object],
           parameters: Dict[str, List[object]],
           run_count: int=1)
"""

"""
```

### Structural objects


#### TimestepBlock

```python
TimestepBlock(*args: PartialStateUpdateBlock,
              **options: object)
"""
Creates an cadCAD timestep block representing an entire simulation structure.

Args:
    *args: Simulation PSUBs. Order-sensitive.
    **options: (still need to think about it)
"""
```


#### PartialStateUpdateBlock

```python
PartialStateUpdateBlock(*args: Union[Policy, StateUpdate],
                        **options: object)
"""
PSUB representing an set of policies and SUFs.

Args:
    *args: Policies and SUFs that compose the PSUB. Must have at least one SUF. 
           Non Ordering-sensitive.
    **options: (still need to think about it)
"""
```

### Logical objects

#### Policy

**Practical form**
```python
Policy(function: callable,
       *maps: PolicyArgument,
       **options: object
       )
"""
Create an Policy wrapped around an user-function. 
The input callable must return an single value or an tuple,
which will be mapped into the given PolicySignals, order-wise.

Args:
    function: callable for wrapping the policy.
    *maps: Wrappers for the function input and output. 
           Must include at least one PolicySignal.
"""
```

**General form**
```python
Policy(function: callable,
       signals: List[PolicySignal],
       pos_args: List[PolicyArgument]=[],
       kw_args: Dict[str, PolicyArgument]={},
       **options: object
       )
"""
Create an Policy wrapped around an user-function. 
The input callable must return an single value or an tuple,
which will be mapped into the given PolicySignals, order-wise.

Args:
    function: callable for wrapping the policy.
    signals: list containing the output wrappers
    pos_args: list containing positional arguments wrappers
    kw_args: dict containing keyword arguments wrappers
"""
```

#### StateUpdate

**Practical form**
```python
StateUpdate(function: callable,
            updated_variable: Union[str, Variable],
            *maps: SUFArgument,
            **options: object
       )
"""
Create an SUF wrapped around an user-function. 
The input callable must return an single value representing the new variable value.

Args:
    function: callable for wrapping the SUF.
    updated_variable: Variable to update
    *maps: Wrappers for the function input and output.
"""
```

**General form**
```python
StateUpdate(function: callable,
            updated_variable: Variable,
            pos_args: List[SUFArgument]=[],
            kw_args: Dict[str, SUFArgument]={},
            **options: object
       )
"""
Create an SUF wrapped around an user-function. 
The input callable must return an single value representing the new variable value.

Args:
    function: callable for wrapping the SUF.
    updated_variable: Variable to update
    pos_args: list containing positional arguments wrappers
    kw_args: dict containing keyword arguments wrappers
"""
```

### Concrete objects

### Arguments

```python
PolicyArgument = Union[Parameter,
                       Substep,
                       StateHistory,
                       Variable]

SUFArgument = Union[PolicyArgument,
                    PolicySignal]

```
#### Variable

```python
Variable(name: str)
"""
Placeholder for an state variable.
"""
```

#### Parameter

```python
Parameter(name: str)
"""
Placeholder for an simulation parameter.
"""
```

#### PolicySignal

```python
PolicySignal(name: str)
"""
Placeholder for an 'policy input' signal
"""
```

#### StateHistory

```python
StateHistory(name: str, 
             timestep: slice, 
             substep: slice)
"""
Placeholder for the state history

Vars:
    name: Variable name
    timestep: Slice of the timestep (eg: 1, -1, 5:8, ::2)
    substep: Slice of the substep (eg: 1, -1, 5:8, ::2)
"""
```

#### Substep

```python
Substep()
"""
Placeholder for the current substep
"""
```

## Example of object usage

```python
# Logical processes
process_1 = lambda a, x: a * x
process_2 = lambda a, x, y: (a * x * y, -1.0 * a * x * y)
swap_process = lambda x, y: (y - x, x - y)
add_delta = lambda pop, delta: max(round(pop + delta), 0 )

# System pieces
prey_population = StateUpdate(add_delta, 
                              'prey_pop'
                              Variable('prey_count'),
                              PolicySignal('delta_prey'))

predator_population = StateUpdate(add_delta, 
                                  'predator_pop',
                                  Variable('predator_count'),
                                  PolicySignal('delta_predator'))

# System dynamics

## Reproduction
prey_growth = Policy(process_1,
                     PolicySignal('delta_prey'),
                     Parameter['prey_growth_rate'],
                     Variable['prey_count']
                    )

predator_growth = Policy(process_1,
                         PolicySignal('delta_predator'),
                         Parameter['predator_growth_rate'],
                         Variable['predator_count']
                        )

## Interaction
prey_predator_interaction = Policy(process_2,
                                   PolicySignal('delta_prey'),
                                   PolicySignal('delta_predator'),
                                   Parameter['prey_predator_interaction'],
                                   Variable['prey_count'],
                                   Variable['predator_count']
                                  )
## Swapping 
prey_predator_swap = Policy(swap_process,
                            PolicySignal('delta_prey'),
                            PolicySignal('delta_predator'),
                            Variable('prey_count'),
                            Variable('predator_count')
                           )

# System structure
lotka_volterra_dynamic = PartialStateUpdateBlock(prey_population, 
                                                 predator_population,
                                                 prey_predator_interaction,
                                                 prey_growth,
                                                 predator_growth,
                                                 scenarios=['all', 'lotka-volterra'])

swapping_dynamic = PartialStateUpdateBlock(prey_predator_swap,
                                           prey_population,
                                           predator_population
                                           scenarios=['all', 'debug']
                                          )

prey_predator_system = TimestepBlock(lotka_volterra_dynamic,
                                     spontaneous_generation_dynamic)
# Simulation config

simulation = Simulation(prey_predator_system,
                        initial_state,
                        parameters,
                        scenario='all')

simulation.run()

```

## How testing could work

```python

# Logical tests
assert swap_process(5, 4) == (4 - 5, 5 - 4)

# Consistency checks
assert simulation.is_consistent is True

assert check_toy_scenario(simulation, test_scenario) is True
```

## Potential beneficial side-effects

* Would make a lot easier to analyze structural interactions and dependences
    * Including make diagramming and documentation tools
* 


```python

```
