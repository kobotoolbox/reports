library(knitr)
library(whisker)

opts_chunk$set(error=FALSE, warning=FALSE)

compile <- function() {
    {% if url %}
    ## 0. download the data
    data <- read.csv('{{ url }}')
    {% endif %}

    ## 1. knit to get calculate value of interest
    md_path <- knit('{{ filename }}', quiet=TRUE)

    ## 2. whisk to include sections of interest
    .context <- list()
    for (k in ls()) {
        .context[[k]] <- get(k)
    }
    template <- paste(readLines('{{ filename }}'), collapse='\n')
    rmd <- whisker.render(template, .context)

    ## 3. write back out to the file and knit again
    writeLines(rmd, '{{ filename }}')
    knit2html('{{ filename }}', quiet=TRUE)
}

compile()
