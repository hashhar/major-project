function alert()
{
    notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$@"
}

n=10
env='crouch'
[ -n $1 ] && n=$1
[ -n "$2" ] && env=$2
echo $n
echo $env
case "$env" in
    "crouch") envUse='CrouchEnv';;
    "stand")  envUse='StandEnv';;
    "gait")   envUse='GaitEnv';;
    "hop")    envUse='HopEnv';;
esac
folders=( $(find new-"$env"/ -mindepth 1 -type d -printf '%f\n') )
new_folder=${#folders[@]}
for i in $(seq 1 $n); do
    python example.py --train --update --model "$env"_default.h5f --steps 25000 --env "$envUse"
    python example.py --train --update --model "$env"_default.h5f --steps 25000 --env "$envUse"
    python example.py --train --update --model "$env"_default.h5f --steps 25000 --env "$envUse"
    python example.py --train --update --model "$env"_default.h5f --steps 25000 --env "$envUse"
    alert "Major Project" "Iteration $i done. $(( 100 * i ))k steps."
    mkdir new-"$env"/$(( new_folder + i ))00k
    sleep 60
    cp "$env"_default*.h5f new-"$env"/$(( new_folder + i ))00k/
done
