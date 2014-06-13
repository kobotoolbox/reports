requirements <- c(
    'knitr',
    'rjson',
    'pander',
    'ggplot2',
    'plyr',
    'reshape2'
    )

init <- function() {
    install.list(requirements)
    install.rcharts()
}

install.list <- function(l) {
    for (lib in requirements) {
        install.packages(lib, dependencies=TRUE)
    }
}

install.rcharts <- function() {
    rcharts.deps <- c('RCurl', 'RJSONIO', 'whisker', 'yaml')
    install.list(rcharts.deps)
    url <- 'https://codeload.github.com/ramnathv/rCharts/tar.gz/master'
    path <- 'rCharts.tar.gz'
    system(paste('curl', url, '-o', path))
    install.packages(path, repos=NULL, type='source')
    system(paste('rm', path))
}

init()
