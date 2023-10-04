#this script can be used to submit all the jobs that were made by make_jobs.py

#list jobs
jobs=($(ls /work/pi_dongw_umass_edu/RNAseq/pipeline/jobs))

echo ${#jobs[@]}

i="0"

while [ $i -lt ${#jobs[@]} ]
do
echo $i
while [ $(squeue --me | wc -l) -lt 20000 ]
do
echo "submitting job..."
sbatch /work/pi_dongw_umass_edu/RNAseq/pipeline/jobs/${jobs[i]}
i=$[$i+1]


done
sleep 1
done
