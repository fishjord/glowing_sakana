#!/bin/bash

sed -i '' 's/<GBSet>/<GBSet xmlns="http:\/\/www.ncbi.nlm.nih.gov\/soap\/eutils\/efetch_seq">/g' $*
