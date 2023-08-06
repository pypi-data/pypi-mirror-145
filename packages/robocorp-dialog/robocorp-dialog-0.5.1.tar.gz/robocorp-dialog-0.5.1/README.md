# Robocorp Dialog

A separate executable which opens a dialog window for querying user input.
Content created dynamically based on JSON spec.

Used in [Dialogs](https://github.com/robocorp/rpaframework/tree/master/packages/dialogs) library.

## How to build

The Python project uses pywebview to render the files in the `static/` folder.
In order to install the Python and JS dependencies you can use:
`poetry run inv install`
and then to build the static files once use:
`poetry run inv build-js`

It is recommended that for development you use the watch command so that the front-end is continously built after each change:
`poetry run inv watch-js`

## How to test

Use: `poetry run inv test`

## How to run

You will also need a JSON formatted input that will contain the elements to be rendered in the dialog.
An example of such a JSON would be: [form_with_steps.json](./tests/assets/form_with_steps.json)

Then the command you use to call the `main.py` file will have to contain this JSON alongside the window title and sizes.
A basic example to start a dialog with a heading would be:

```cmd
python robocorp_dialog/main.py --title Dialog --width 480 --height 100 --auto_height '[{"type":"heading","value":"Send feedback","size":"medium"}]'
```
