.PHONY: clear-data

clear-data:
	find ./data -type f -exec rm -f {} \;
