#!/bin/bash
iiss_info=`curl -X POST https://ctz.solidwallet.io/api/v3 --data '{ "jsonrpc": "2.0", "method": "icx_call", "params": { "to": "cx0000000000000000000000000000000000000000", "dataType": "call", "data": { "method": "getIISSInfo" } }, "id": 1 }'`

current_height=$((`echo ${iiss_info} | jq ".result.blockHeight" | tr -d '"'`))
target_height=$((`echo ${iiss_info} | jq ".result.nextPRepTerm" | tr -d '"'`))
height_left=$((target_height - current_height))

#TZ="Asia/Seoul"
required_sec=$((${height_left} * 2))
curr_time=`date +%s` # Epoch time
est_time=$((curr_time + required_sec))
t_diff=$((est_time - curr_time))


# ----- Results
echo "======RESULT======"
echo ">>> Current height: ${current_height}"
echo ">>> Target height : ${target_height}"
echo ">>> Heights left  : ${height_left}"
echo
TZ="Asia/Seoul"
echo "... Current Time  : `TZ=${TZ} date`"
echo "... Estimated Time: `TZ=${TZ} date --date @${est_time}`"
echo "... $((t_diff % (3600*24) / 3600)) hours $((t_diff % 3600 / 60)) minutes $((t_diff % 60)) seconds left."
