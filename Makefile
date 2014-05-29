data:
	mkdir data

data/games.csv: data
	curl -o data/games.csv http://www.calvin.edu/~stob/data/bballgames03.csv
	touch data/games.csv

data/mortality_rates.csv: data
	mkdir temp
	curl -o temp/worldbank.zip "http://api.worldbank.org/v2/en/indicator/sh.dyn.mort?downloadformat=csv"
	cd temp; unzip worldbank.zip
	cat temp/sh.dyn.mort_Indicator_en_csv_v2.csv | sed '1,2d' > data/mortality_rates.csv
	rm -r temp

clean:
	rm -rf data reports figure mortality.md

reports: data/games.csv data/mortality_rates.csv
	mkdir reports
	Rscript compiler.R
