# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robocorp_dialog']

package_data = \
{'': ['*'],
 'robocorp_dialog': ['Dialog.app/Contents/*',
                     'Dialog.app/Contents/MacOS/*',
                     'Dialog.app/Contents/MacOS/AppKit/*',
                     'Dialog.app/Contents/MacOS/CoreFoundation/*',
                     'Dialog.app/Contents/MacOS/Foundation/*',
                     'Dialog.app/Contents/MacOS/WebKit/*',
                     'Dialog.app/Contents/MacOS/lib-dynload/*',
                     'Dialog.app/Contents/MacOS/objc/*',
                     'Dialog.app/Contents/MacOS/robocorp_dialog/static/*',
                     'Dialog.app/Contents/Resources/*',
                     'Dialog.app/Contents/Resources/robocorp_dialog/static/*',
                     'Dialog.app/Contents/_CodeSignature/*',
                     'Dialog/*',
                     'Dialog/robocorp_dialog/static/*',
                     'Dialog/webview/lib/*',
                     'Dialog/webview/lib/x64/*',
                     'Dialog/webview/lib/x86/*',
                     'static/*']}

extras_require = \
{':sys_platform == "linux"': ['pywebview>=3.5,<4.0',
                              'PyQt5>=5.15.2,<6.0.0',
                              'PyQtWebEngine>=5.15.2,<6.0.0']}

entry_points = \
{'console_scripts': ['robocorp-dialog = robocorp_dialog.main:main']}

setup_kwargs = {
    'name': 'robocorp-dialog',
    'version': '0.5.1',
    'description': 'Dialog for querying user input',
    'long_description': '# Robocorp Dialog\n\nA separate executable which opens a dialog window for querying user input.\nContent created dynamically based on JSON spec.\n\nUsed in [Dialogs](https://github.com/robocorp/rpaframework/tree/master/packages/dialogs) library.\n\n## How to build\n\nThe Python project uses pywebview to render the files in the `static/` folder.\nIn order to install the Python and JS dependencies you can use:\n`poetry run inv install`\nand then to build the static files once use:\n`poetry run inv build-js`\n\nIt is recommended that for development you use the watch command so that the front-end is continously built after each change:\n`poetry run inv watch-js`\n\n## How to test\n\nUse: `poetry run inv test`\n\n## How to run\n\nYou will also need a JSON formatted input that will contain the elements to be rendered in the dialog.\nAn example of such a JSON would be: [form_with_steps.json](./tests/assets/form_with_steps.json)\n\nThen the command you use to call the `main.py` file will have to contain this JSON alongside the window title and sizes.\nA basic example to start a dialog with a heading would be:\n\n```cmd\npython robocorp_dialog/main.py --title Dialog --width 480 --height 100 --auto_height \'[{"type":"heading","value":"Send feedback","size":"medium"}]\'\n```\n',
    'author': 'Ossi Rajuvaara',
    'author_email': 'ossi@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
