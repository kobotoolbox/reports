library(knitr)

opts_chunk$set(error=FALSE, warning=FALSE)
knit2html('{{ filename }}', quiet=TRUE)
