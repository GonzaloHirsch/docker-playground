#!/bin/sh -e

# Help users with usage and get out
# https://stackoverflow.com/questions/16483119/an-example-of-how-to-use-getopts-in-bash
usage() {
    echo "Usage: $0 [-f <positive integer>] [-s <positive integer>] [-p <string, path>]" 1>&2
    exit 1
}

# Ensure we get the correct options
while getopts ":s:f:p:" o; do
    case "${o}" in
    s)
        FILE_SIZE=${OPTARG}
        case $FILE_SIZE in
        '' | *[!0-9]*)
            echo "Error: Argument for -f must be an integer ($FILE_SIZE)."
            usage
            ;;
        *) ;;
        esac
        ;;
    f)
        FILE_COUNT=${OPTARG}
        case $FILE_COUNT in
        '' | *[!0-9]*)
            echo "Error: Argument for -f must be an integer ($FILE_COUNT)."
            usage
            ;;
        *) ;;
        esac
        ;;
    p)
        FILE_PATH=${OPTARG}
        ;;
    *)
        usage
        ;;
    esac
done
shift $((OPTIND - 1))

# Validate the options
if [ -z "${FILE_SIZE}" ] || [ -z "${FILE_COUNT}" ] || [ -z "${FILE_PATH}" ]; then
    usage
fi

echo "[INFO] This will generate $FILE_COUNT files of up to $FILE_SIZE bytes each on $FILE_PATH"

TOTAL_SIZE=0

# https://gist.github.com/earthgecko/3089509
# Generate a random file with the amount of characters in question from the character set
for i in $(seq 1 $FILE_COUNT); do
    SIZE=$(shuf -i 0-$FILE_SIZE -n 1)
    cat /dev/urandom | env LC_ALL=C tr -dc 'a-zA-Z0-9 ' | head -c $SIZE | head -n 1 | tr -d '\n' >$FILE_PATH/$i
    TOTAL_SIZE=$((TOTAL_SIZE + SIZE))
done

# Inform the total size for debugging purposes
echo "[INFO] Total file size is: $TOTAL_SIZE bytes"
echo "[INFO] Total file count is: $FILE_COUNT files"
