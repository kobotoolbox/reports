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
        if (l[[k]] != '') {
            keep <- result[[k]] == l[[k]]
            result <- result[keep, ]
        }
    }
    return(result)
}

set.knitr.defaults <- function() {
    opts_chunk$set(error=FALSE, echo=FALSE)
}

compile <- function(config, destination) {
    compilation.id <- config$id

    set.knitr.defaults()
    rmd.path <- paste0('templates/', config$template, '.Rmd')
    knit2html(rmd.path, quiet=TRUE)

    html.path <- paste0(config$template, '.html')
    system(paste('mv', html.path, destination))

    md.path <- paste0(config$template, '.md')
    system(paste('rm', md.path))
}

get.data <- function(config) {
    return(do.call(extract, config$data))
}

md2pdf <- function() {
    ## Let's also make a pdf using pandoc.
    system('pandoc mortality.md -o mortality.pdf')
    pdf.path <- paste0('reports/', country.code, '.pdf')
    system(paste('mv mortality.pdf', pdf.path))
}

args <- commandArgs(trailingOnly=TRUE)
config <- fromJSON(file=args[1])
compile(config, destination=args[2])
