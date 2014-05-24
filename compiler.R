library(knitr)

args <- commandArgs(trailingOnly = TRUE)
for (line in args) {
    # expects destination
    eval(parse(text=line))
}

# Create an HTML report using knitr.
country.code <- gsub('(reports/|.html)', '', destination)
knit2html('mortality.Rmd', quiet=TRUE)
system('mkdir -p reports')
system(paste('mv mortality.html', destination))

# Let's also make a pdf using pandoc.
system('pandoc mortality.md -o mortality.pdf')
pdf.path <- paste0('reports/', country.code, '.pdf')
system(paste('mv mortality.pdf', pdf.path))
