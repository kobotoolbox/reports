requirements <- c(
    'knitr',
    'rjson',
    'pander',
    'ggplot2',
    'plyr',
    'reshape2'
    )

for (lib in requirements) {
    install.packages(lib, dependencies=TRUE)
}
