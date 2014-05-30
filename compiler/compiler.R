library(knitr)
library(rjson)
library(pander)
library(ggplot2)
library(plyr)

# TODO: It would be good to tap into a good SQL library here.
extract <- function(path, ...) {
    options(stringsAsFactors=FALSE)
    result <- read.csv(path)
    l <- list(...)
    for (k in names(l)) {
        keep <- result[[k]] %in% l[[k]]
        result <- result[keep, ]
    }
    return(result)
}

set.knitr.defaults <- function() {
    opts_chunk$set(error=FALSE, echo=FALSE)
}

compile <- function(config) {
    compilation.id <- config$id

    set.knitr.defaults()
    rmd.path <- paste0('templates/', config$template, '.Rmd')
    knit2html(rmd.path, quiet=TRUE)

    html.path <- paste0(config$template, '.html')
    destination <- paste0('reports/', compilation.id, '.html')
    system(paste('mv', html.path, destination))

    md.path <- paste0(config$template, '.md')
    system(paste('rm', md.path))
}

get.data <- function(config) {
    return(do.call(extract, config$data))
}

## TODO: This JSON parser doesn't throw errors when it should.
compilations <- fromJSON(file='compilations.json')
for (config in compilations) {
    compile(config)
}

md2pdf <- function() {
    ## Let's also make a pdf using pandoc.
    system('pandoc mortality.md -o mortality.pdf')
    pdf.path <- paste0('reports/', country.code, '.pdf')
    system(paste('mv mortality.pdf', pdf.path))
}
