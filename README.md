# reporteR

I want to make it easy to compile a large number of dynamic reports using R. [knitr](http://yihui.name/knitr/) has solved the dynamic report generation problem, I want to build some infrastructure around `knitr` to help with the automation process. In my ideal world, we would build a web application that allows a user to login and compile specific reports for some focal subset of the data. As a first step, I want to make it easy for R developers to compile a large numbers of reports. Features of `reporteR` include:

1.  Each time a report is compiled we can specify:
    1.  What data should be included in the analysis.
    2.  Pass in parameters that will affect the behavior of the report.
2.  Maintain a list of report compilations so a developer can quickly re-compile all reports.

## Tour the code

Compiling all reports requires one command:

    make reports

This will download and clean all required data sets, and then run the compiler. The compiler looks in the configuration file compilations.json, which contains a list of all report compilations to generate. The compile function is inspired by Django's render function. Instead of render(template, dictionary) we use compile(config), where the template/report name is contained in the config. Feel free to check out the config file (compilations.json) and the corresponding compiled reports in the reports folder.
