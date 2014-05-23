library(knitr)

args <- commandArgs(trailingOnly = TRUE)
for (line in args) {
    # expects destination
    eval(parse(text=line))
}

rmd.file <- 'activity.Rmd'
country.code <- gsub('(reports/|.html)', '', destination)
knit2html(rmd.file, quiet=TRUE)
html.file <- gsub('.Rmd', '.html', rmd.file)
dir.create('reports', showWarnings=FALSE)
quietly <- file.rename(from=html.file, to=destination)
