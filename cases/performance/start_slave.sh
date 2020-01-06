for((i=0;i<8;i++))
do
   locust -f $1 --slave --master-host=$2 &
done
