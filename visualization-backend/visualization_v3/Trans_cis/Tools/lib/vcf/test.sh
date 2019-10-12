str="HD15QZAA00752-1-I22"
array=(${str//-/ })
echo ${array[0]}

for i in "${!array[@]}"; do
    echo "$i=>${array[i]}"
done
