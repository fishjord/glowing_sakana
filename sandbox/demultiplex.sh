#!/bin/bash

SFFFILE=/scratch/fishjord/apps/sff/bin/sfffile
CAFE=/scratch/fishjord/apps/bin/cafe

if [ $# -ne 3 ]; then
	echo "USAGE: demultiplex.sh <forward_primer> <tagfile> <sff_dir>"
	exit 1
fi

if [ `hostname` != "nonpareil" ]; then
	echo "This program must be run on nonpareil"
	exit 1
fi

for_primer=$1
tag_file=$2
sff_dir=$3

mkdir init_proc
mkdir demultiplexed
mkdir ids

echo "    <FILES>" > submission_stub.xml

for f in `ls "$sff_dir"/*.sff`
do
	run=`basename $f | sed 's/.sff//g'`
	echo "Processing run $run, $f"

	$CAFE InitialProcessorMain -f $for_primer -t $tag_file -o init_proc/"$run" -S -s $f > /dev/null

	for seq_file in `ls init_proc/"$run"/result_dir/*/*.fasta`
	do
		tag_name=`basename $seq_file | sed 's/_trimmed.fasta//g'`
		echo "   Processing tag $tag_name"
		stem="$run"-"$tag_name"
		
		id_file=ids/"$stem".ids
		grep '>' $seq_file | sed -r 's/>([^ ]+)[ ].*/\1/g' > $id_file

		echo "   `wc -l $id_file` ids found"

		demultiplex_sff=demultiplexed/"$stem".sff
		echo "   Demultiplexing to $demultiplex_sff"
		$SFFFILE -i $id_file -o $demultiplex_sff $f

		sum=`md5sum $demultiplex_sff | sed -r 's/[ ]+.*//g'`

		echo "        <FILE checksum=\"$sum\" checksum_method=\"MD5\" filename=\"$stem.sff\"/>" >> submission_stub.xml
		echo
	done
done

echo "    </FILES>" >> submission_stub.xml
