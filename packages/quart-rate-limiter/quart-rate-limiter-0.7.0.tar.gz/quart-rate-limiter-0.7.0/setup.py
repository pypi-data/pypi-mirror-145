# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quart_rate_limiter']

package_data = \
{'': ['*']}

install_requires = \
['quart>=0.15']

extras_require = \
{'redis': ['aioredis>=2.0']}

setup_kwargs = {
    'name': 'quart-rate-limiter',
    'version': '0.7.0',
    'description': 'A Quart extension to provide rate limiting support',
    'long_description': 'Quart-Rate-Limiter\n==================\n\n|Build Status| |pypi| |python| |license|\n\nQuart-Rate-Limiter is an extension for `Quart\n<https://gitlab.com/pgjones/quart>`_ to allow for rate limits to be\ndefined and enforced on a per route basis. The 429 error response\nincludes a `RFC7231\n<https://tools.ietf.org/html/rfc7231#section-7.1.3>`_ compliant\n``Retry-After`` header and the successful responses contain headers\ncompliant with the `RateLimit Header Fields for HTTP\n<https://tools.ietf.org/html/draft-polli-ratelimit-headers-00>`_ RFC\ndraft.\n\nUsage\n-----\n\nTo add a rate limit first initialise the RateLimiting extension with\nthe application,\n\n.. code-block:: python\n\n    app = Quart(__name__)\n    rate_limiter = RateLimiter(app)\n\nor via the factory pattern,\n\n.. code-block:: python\n\n    rate_limiter = RateLimiter()\n\n    def create_app():\n        app = Quart(__name__)\n        rate_limiter.init_app(app)\n        return app\n\nNow this is done you can apply rate limits to any route by using the\n``rate_limit`` decorator,\n\n.. code-block:: python\n\n    @app.route(\'/\')\n    @rate_limit(1, timedelta(seconds=10))\n    async def handler():\n        ...\n\nOr to apply rate limits to all routes within a blueprint by using the\n``limit_blueprint`` function,\n\n.. code-block:: python\n\n    blueprint = Blueprint("name", __name__)\n    limit_blueprint(blueprint, 1, timedelta(seconds=10))\n\nOr to apply rate limits to all routes in an app, define the default\nlimits when initialising the RateLimiter,\n\n.. code-block:: python\n\n    rate_limiter = RateLimiter(\n        default_limits=[RateLimit(1, timedelta(seconds=10))]\n    )\n\nand then to exempt a route,\n\n.. code-block:: python\n\n    @app.route("/exempt")\n    @rate_exempt\n    async def handler():\n        ...\n\n\nTo alter the identification of remote users you can either supply a\nglobal key function when initialising the extension, or on a per route\nbasis.\n\nBy default rate limiting information (TATs) will be stored in memory,\nwhich will result in unexpected behaviour if multiple workers are\nused. To solve this a redis store can be used by installing the\n``redis`` extra (``pip install quart-rate-limiter[redis]``) and then\nusing as so,\n\n.. code-block:: python\n\n    from quart_rate_limiter.redis_store import RedisStore\n\n    redis_store = RedisStore(address)\n    RateLimiter(app, store=redis_store)\n\nThis store uses `aioredis <https://github.com/aio-libs/aioredis>`_,\nand any extra keyword arguments passed to the ``RedisStore``\nconstructor will be passed to the aioredis ``create_redis`` function.\n\nA custom store is possible, see the ``RateLimiterStoreABC`` for the\nrequired interface.\n\nSimple examples\n~~~~~~~~~~~~~~~\n\nTo limit a route to 1 request per second and a maximum of 20 per minute,\n\n.. code-block:: python\n\n    @app.route(\'/\')\n    @rate_limit(1, timedelta(seconds=1))\n    @rate_limit(20, timedelta(minutes=1))\n    async def handler():\n        ...\n\nAlternatively the ``limits`` argument can be used for multiple limits,\n\n.. code-block:: python\n\n    @app.route(\'/\')\n    @rate_limit(\n        limits=[\n            RateLimit(1, timedelta(seconds=1)),\n            RateLimit(20, timedelta(minutes=1)),\n        ],\n    )\n    async def handler():\n        ...\n\nTo identify remote users based on their authentication ID, rather than\ntheir IP,\n\n.. code-block:: python\n\n    async def key_function():\n        return current_user.id\n\n    RateLimiter(app, key_function=key_function)\n\nThe ``key_function`` is a coroutine function to allow session lookups\nif appropriate.\n\nContributing\n------------\n\nQuart-Rate-Limiter is developed on `GitLab\n<https://gitlab.com/pgjones/quart-rate-limiter>`_. You are very welcome to\nopen `issues <https://gitlab.com/pgjones/quart-rate-limiter/issues>`_ or\npropose `merge requests\n<https://gitlab.com/pgjones/quart-rate-limiter/merge_requests>`_.\n\nTesting\n~~~~~~~\n\nThe best way to test Quart-Rate-Limiter is with Tox,\n\n.. code-block:: console\n\n    $ pip install tox\n    $ tox\n\nthis will check the code style and run the tests.\n\nHelp\n----\n\nThis README is the best place to start, after that try opening an\n`issue <https://gitlab.com/pgjones/quart-rate-limiter/issues>`_.\n\n\n.. |Build Status| image:: https://gitlab.com/pgjones/quart-rate-limiter/badges/main/pipeline.svg\n   :target: https://gitlab.com/pgjones/quart-rate-limiter/commits/main\n\n.. |pypi| image:: https://img.shields.io/pypi/v/quart-rate-limiter.svg\n   :target: https://pypi.python.org/pypi/Quart-Rate-Limiter/\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/quart-rate-limiter.svg\n   :target: https://pypi.python.org/pypi/Quart-Rate-Limiter/\n\n.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://gitlab.com/pgjones/quart-rate-limiter/blob/main/LICENSE\n',
    'author': 'pgjones',
    'author_email': 'philip.graham.jones@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pgjones/quart-rate-limiter/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
