jobs=($(ls /work/pi_dongw_umass_edu/RNAseq/jobs))

echo ${#jobs[@]}

i="0"

while [ $i -lt ${#jobs[@]} ]
do
echo $i
while [ $(squeue --me | wc -l) -lt 20000 ]
do
echo "submitting job..."
sbatch /work/pi_dongw_umass_edu/RNAseq/jobs/${jobs[i]}
i=$[$i+1]


done
sleep 1
done

#for job in ${jobs[@]}; do

#    sleep 10
#    sbatch ./jobs/$job

#done
