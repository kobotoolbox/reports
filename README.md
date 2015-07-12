# reports

`reporter` makes it easy to compile a large number of dynamic reports. Check out a demo [here](http://dimagi.herokuapp.com/). `reporter` is built with the R package [knitr](http://yihui.name/knitr/), the Python web framework [Django](https://www.djangoproject.com/), and it is deployed with [Heroku](https://www.heroku.com).

Adding a new dynamic report to `reporter` is easy:

1.  Add an R Markdown document to the [templates](https://github.com/amarder/reporter/tree/master/compiler/templates) folder.
2.  Add a corresponding entry in the [config file](https://github.com/amarder/reporter/tree/master/web_portal/portal/reports.json).
