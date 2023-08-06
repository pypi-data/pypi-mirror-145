# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_handleref', 'django_handleref.rest']

package_data = \
{'': ['*'],
 'django_handleref': ['templates/handleref/*',
                      'templates/handleref/grappelli/*']}

entry_points = \
{'markdown.extensions': ['pymdgen = pymdgen.md:Extension']}

setup_kwargs = {
    'name': 'django-handleref',
    'version': '1.0.2',
    'description': 'django object tracking',
    'long_description': '\n# django-handleref\n\n[![PyPI](https://img.shields.io/pypi/v/django-handleref.svg?maxAge=3600)](https://pypi.python.org/pypi/django-handleref)\n[![PyPI](https://img.shields.io/pypi/pyversions/django-handleref.svg?maxAge=600)](https://pypi.python.org/pypi/django-handleref)\n[![Tests](https://github.com/20c/django-handleref/workflows/tests/badge.svg)](https://github.com/20c/django-handleref)\n[![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/20c/django-handleref)](https://lgtm.com/projects/g/20c/django-handleref/alerts/)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/django-handleref/master.svg?maxAge=3600)](https://codecov.io/github/20c/django-handleref)\n\ntrack when an object was created or changed and allow querying based on time and versioning (w/ django-reversion support)\n\n## HandleRefModel as a base for all your models\n\n    from django.db import models\n    from django_handleref.models import HandleRefModel\n\n    class Test(HandleRefModel):\n        name = models.CharField(max_length=255)\n\n## Querying for modification since\n\nIt is now possible for you to see which instances of a model have been created or modified\nsince a specific time or version\n\n    import time\n\n    # create instance\n    test = Test.objects.create(name="This is a test")\n\n    # keep track of time, we need this later\n    t = time.time()\n\n    # modifying and saving it\n    test.name = "Changed my mind"\n    test.save()\n\n    # now we can use the handleref manager to retrieve it\n    Test.handleref.since(timestamp=t).count() # 1\n    Test.handleref.since(timestamp=time.time().count() #0\n\n\n## Soft delete\n\nBy default all models extending HandleRefModel will softdelete when their delete() method is called.\nNote that this currently wont work for batch deletes - as this does not call the delete() method.\n\n    test = Test.objects.get(id=1)\n    test.delete()\n\n    # querying handleref undeleted will not contain the deleted object\n    Test.handleref.undeleted().filter(id=1).count() #0\n\n    # querying handleref since will not contain the deleted object\n    Test.handleref.since(timestamp=t).filter(id=1).count() #0\n\n    # passing deleted=True to handleref since will contain the deleted object\n    Test.handleref.since(timestamp=t, deleted=True).filter(id=1).count() #1\n\n    # querying using the standard objects manager will contain the deleted object\n    Test.objects.filter(id=1).count() #1\n\n    # You may also still hard-delete by passing hard=True to delete\n    test.delete(hard=True)\n    Test.objects.filter(id=1).count() #0\n\n## Versioning (with django-reversion)\n\nRequires\n\n    django-reversion==1.8.7\n\nWhen django-reversion is installed all your HandleRefModels will be valid for versioning.\n\n    import reversion\n\n    with reversion.create_revision():\n        obj = Test.objects.create(name="This is a test")\n        obj.save()\n\n        obj.version #1\n\n        obj.name = "Changed my mind"\n        obj.save()\n\n        obj.version #2\n\n    Test.handleref.since(version=1).count() #1\n\n\n### License\n\nCopyright 2015-2021 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this softare except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/django-handleref',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
