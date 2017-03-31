function alert()
{
    notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$@"
}

for i in $(seq 1 10); do
    python example.py --train --update --model stand_default.h5f
    alert "Major Project" "Iteration $i done. $(( 10 * i ))k steps."
    sleep 60
    cp stand_default_actor.h5f stand_default_actor.h5f.bup
    cp stand_default_critic.h5f stand_default_critic.h5f.bup
    sleep 60
done
