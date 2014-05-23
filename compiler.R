library(knitr)

args <- commandArgs(trailingOnly = TRUE)
for (line in args) {
    # expects rmd.file and country.code
    eval(parse(text=line))
}

knit2html(rmd.file, quiet=TRUE)
html.file <- gsub('.Rmd', '.html', rmd.file)
dir.create('reports', showWarnings=FALSE)
destination <- paste0('reports/', country.code, '.html')
quietly <- file.rename(from=html.file, to=destination)
