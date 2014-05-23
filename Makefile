data/mortality_rates.csv:
	mkdir data
	curl -o data/worldbank.zip "http://api.worldbank.org/v2/en/indicator/sh.dyn.mort?downloadformat=csv"
	cd data; unzip worldbank.zip
	mv data/sh.dyn.mort_Indicator_en_csv_v2.csv data/mortality_rates.csv
	touch data/mortality_rates.csv

clean:
	rm -rf data reports figure activity.md

reports/ETH.html: compiler.R activity.Rmd data/mortality_rates.csv
	Rscript compiler.R "rmd.file <- 'activity.Rmd'" "country.code <- 'ETH'"
