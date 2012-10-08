FILE_DIR=/Users/gerickson/Downloads/
#Empty redis
redis-cli FLUSHALL
#Load files
python train.py $FILE_DIR/spam.txt $FILE_DIR/spam2.txt | python load.py --spam
python train.py $FILE_DIR/easy_ham.txt $FILE_DIR/hard_ham.txt | python load.py 