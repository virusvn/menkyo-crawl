clang dedict.c -Wall -lz -o dedict
clang strip.c -Wall -o strip
./dedict "Oxford Dictionary of English" | ./strip > dict.xml
egrep -o 'd:title="(.+?)"' dict.xml | awk -F\" '{print $2}' > words