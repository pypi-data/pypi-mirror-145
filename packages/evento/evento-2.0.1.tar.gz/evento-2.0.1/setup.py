# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['evento']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'evento',
    'version': '2.0.1',
    'description': 'Observer pattern made muy facil',
    'long_description': '# pyevento\n\n[![Build Status](https://travis-ci.org/markkorput/pyevento.svg)](https://travis-ci.org/markkorput/pyevento)\n[![PyPI wheel](https://img.shields.io/pypi/wheel/evento?style=flat)](https://pypi.org/project/evento/ "View this project on npm")\n[![Github Tag](https://img.shields.io/github/tag/markkorput/pyevento.svg?label=version)](https://github.com/markkorput/pyevento/releases/latest)\n\nPython evento package, making the Observer pattern estúpida sencillo.\n\n## Install\n\n```shell\npip install evento\n```\n\n## Basic Usage\n\n```python\nfrom evento import Event\n\n# observers are simply methods\ndef observer(value: str):\n\tprint("Received: " + value)\n\n# we need to create an instance for every event we want to fire\ndemo_event: Event[str] = Event()\n\n# subscribe observer to the event\ndemo_event += observer\n\n# trigger notifications for the event (run all observers)\ndemo_event(\'Hello\') # => "Received: Hello"\ndemo_event(\'World\') # => "Received: World"\n```\n\n## Typical usage\n\nThis is how Events are typically used to decouple code into separate classes;\n\n```python\nfrom evento import Event\n\nclass Action:\n\tdef __init__(self, name) -> None:\n\t\tself.name = name\n\t\tself.run_event = Event[Action]()\n\n\tdef run(self) -> None:\n\t\tself.run_event(self)\n\nclass ActionCounter:\n\tdef __init__(self, action: Action) -> None:\n\t\tself.count = 0\n\t\t# Event.add returns an unsubscribe method\n\t\tself._disconnect = action.run_event.add(self._on_action)\n\n\tdef __del__(self) -> None:\n\t\t# observers should make sure to unsubscribe from events when they are done\n\t\tself._disconnect()\n\n\tdef _on_action(self, action: Action) -> None:\n\t\tself.count += 1\n\t\tprint(f"\'{action.name}\' ran {self.count} times")\n\naction = Action(\'Foo action\')\ncounter = ActionCounter(action)\naction.run() # => "\'Foo action\' ran 1 times"\naction.run() # => "\'Foo action\' ran 2 times"\n```\n\n## Unsubscribe\n\n```python\n\n# setup\nevent = Event()\n\ndef handler(value) -> None:\n\tprint(value)\n\ndef setup() -> Callable[[], None]:\n\tunsubscribe = event.add(handler)\n\treturn unsubscribe\n\ncleanup = setup()\n\n# ... do stuff ...\n\n# cleanup; all the following lines do the same\nevent -= handler\nevent.remove(handler)\ncleanup()\n```\n\n## Async Event\n\nWorks the same as `Event` but takes async subscribers and has to be awaited;\n\n```python\nfrom evento import AsyncEvent\nevent = AsyncEvent[float]()\n\nasync def echo_double(value: float) -> None:\n\tprint(f"double: {value * 2}")\n\nevent.append(echo_double)\n# ...\nawait event(5.0) # using __call__\nawait event.fire(10.0) # using fire (same as __call__)\n# ...\nevent.remove(echo_double)\n```\n\n## Signature Event\n\nSince version 2.0.0 `evento` is typed and `Event` and `SyncEvent` are generic classes with a single type; they are \'fired\' using a single argument, and all subscribers are expected to take one argument of that type.\n\nTo support more complex method signatures, the `event` and `async_event` decorator can be used to turn a method into an event;\n\n### Sync\n\n```python\nfrom evento import event\n@event\ndef multi_arg_event(id: int, message: str, price: float, **opts: Any) -> None:\n    ...\n\ndef observer(id: int, message: str, price: float, **opts: Any) -> None:\n    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")\n\nmulti_arg_event += observer\nmulti_arg_event(0, "Hello World!", 9.99, demo=True)\n```\n\n### Async\n\n```python\nfrom evento import async_event\n\nasync def observer(id: int, message: str, price: float, **opts: Any) -> Any:\n    print(f"observer: id={id}, message={message}, price={price}, opts={opts}")\n\n@async_event\nasync def multi_arg_event(id: int, message: str, price: float, **opts: Any) -> str:\n\treturn "Done"\n\n# the original method is still invoked after all event subscribers have executed\nresult = await multi_arg_event(1, "Test-12", 9.99, feature=True)\nprint(f"Result: {result}") # => Done\n```\n',
    'author': 'Mark van de Korput',
    'author_email': 'dr.theman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markkorput/pyevento',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
