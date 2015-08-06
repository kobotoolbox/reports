library(knitr)
library(rmarkdown)
library(whisker)

opts_chunk$set(error=FALSE, warning=FALSE)

compile <- function() {
    {% if url %}
    ## 0. download the data
    data <- read.csv('data.csv')
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

    ## 3. write back out to the file
    writeLines(rmd, '{{ filename }}')

    ## 4. render different formats using rmarkdown
    formats <- list(md_document(), html_document(), word_document(), pdf_document())
    for (of in formats) {
        render('{{ filename }}', output_format=of, quiet=TRUE)
    }
}

compile()
