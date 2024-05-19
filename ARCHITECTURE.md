# Architecture
___
## Running
Run the flask server with `python3 core_app.py`

## Test Environment
To run the test environment, use `testwidget.py`.\
Change the widget being tested by editing the `widget=` variable\
Change the script being tested by editing the `script="js/"` variable
___
## templates
* **templates/**
  * `head.html`   application header info
  * `index.html` application main page
  * `WidgetTester.html` widget test environment``
    * **poll/**
      * `PollWidget.html` polling interface widget
* **static**
  * **css**
    * `custom.css` custom css rules
    * `colors.css` define custom css color vars
  * **js**
    * `LoadPolLData.js` loads a poll entry from database
    * `pollVote.js` submits a poll vote from a button input