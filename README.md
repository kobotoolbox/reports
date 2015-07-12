# reports

`reports` is a Django project that makes it easy to compile dynamic
reports. It is built on the R package
[knitr](http://yihui.name/knitr/).

# Current Features

Report templates are stored in the database.

Context variables can be passed to the template each time a template
is rendered. This allows us to pass in a URL describing where to pull
data from (read the kobo API).

# TODO

Dockerize this project so it's easy to deploy.

Need support for an if/else template tag. So we can return a warning
message if a deployment has fewer than 150 responses.

# Backburner

On each compilation of a report, it would be nice to save the
corresponding CSV file. That way when the report is recompiled we can
pull only the new / updated data from the API to get the latest
data. I'm not going to worry about setting this up right now, but I'll
keep it in mind in my design decisions.

I am going to ignore different user roles for the moment.  It seems
like there is a large NGO that wants to write reports, and then there
are satellite offices collecting data that will want to view the
reports. For the moment I'm not going to worry too much about
supporting different users and groups.

We will want to share sessions with the other kobo projects on the
server, this will allow users to log in once.
