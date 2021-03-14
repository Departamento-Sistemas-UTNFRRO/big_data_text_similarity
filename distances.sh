INPUT_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/_samples_input"
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/distances"

SAMPLE_NAME_PREFIX="question_pairs_subset_100"
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t gtfidf -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/100/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t sem -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/100/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/100/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t ft -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/100/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/100/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 100

SAMPLE_NAME_PREFIX="question_pairs_subset_500"
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t gtfidf -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t sem -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t ft -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 500

SAMPLE_NAME_PREFIX="question_pairs_subset_1000"
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t gtfidf -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t sem -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t ft -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1000

SAMPLE_NAME_PREFIX="question_pairs_subset_1500"
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t gtfidf -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t sem -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t ft -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/1500/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 1500

SAMPLE_NAME_PREFIX="question_pairs_subset_2000"
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t gtfidf -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/2000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 2000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t sem -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/2000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 2000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/2000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 2000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t ft -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/2000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 2000
python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -sample "$INPUT_FOLDER/2000/" -sample_file_name "$SAMPLE_NAME_PREFIX" -k 10 -n 2000

python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique gtfidf -samples_path "$INPUT_FOLDER/100/" -input_path "$RESULTS_FOLDER/gtfidf/100_10" -runs 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique gtfidf -samples_path "$INPUT_FOLDER/500/" -input_path "$RESULTS_FOLDER/gtfidf/500_10" -runs 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique gtfidf -samples_path "$INPUT_FOLDER/1000/" -input_path "$RESULTS_FOLDER/gtfidf/1000_10" -runs 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique gtfidf -samples_path "$INPUT_FOLDER/1500/" -input_path "$RESULTS_FOLDER/gtfidf/1500_10" -runs 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique gtfidf -samples_path "$INPUT_FOLDER/2000/" -input_path "$RESULTS_FOLDER/gtfidf/2000_10" -runs 10 -n 2000

python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique sem -samples_path "$INPUT_FOLDER/100/" -input_path "$RESULTS_FOLDER/sem/100_10" -runs 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique sem -samples_path "$INPUT_FOLDER/500/" -input_path "$RESULTS_FOLDER/sem/500_10" -runs 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique sem -samples_path "$INPUT_FOLDER/1000/" -input_path "$RESULTS_FOLDER/sem/1000_10" -runs 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique sem -samples_path "$INPUT_FOLDER/1500/" -input_path "$RESULTS_FOLDER/sem/1500_10" -runs 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique sem -samples_path "$INPUT_FOLDER/2000/" -input_path "$RESULTS_FOLDER/sem/2000_10" -runs 10 -n 2000

python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$INPUT_FOLDER/100/" -input_path "$RESULTS_FOLDER/bow/100_10" -runs 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$INPUT_FOLDER/500/" -input_path "$RESULTS_FOLDER/bow/500_10" -runs 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$INPUT_FOLDER/1000/" -input_path "$RESULTS_FOLDER/bow/1000_10" -runs 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$INPUT_FOLDER/1500/" -input_path "$RESULTS_FOLDER/bow/1500_10" -runs 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$INPUT_FOLDER/2000/" -input_path "$RESULTS_FOLDER/bow/2000_10" -runs 10 -n 2000

python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique ft -samples_path "$INPUT_FOLDER/100/" -input_path "$RESULTS_FOLDER/ft/100_10" -runs 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique ft -samples_path "$INPUT_FOLDER/500/" -input_path "$RESULTS_FOLDER/ft/500_10" -runs 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique ft -samples_path "$INPUT_FOLDER/1000/" -input_path "$RESULTS_FOLDER/ft/1000_10" -runs 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique ft -samples_path "$INPUT_FOLDER/1500/" -input_path "$RESULTS_FOLDER/ft/1500_10" -runs 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique ft -samples_path "$INPUT_FOLDER/2000/" -input_path "$RESULTS_FOLDER/ft/2000_10" -runs 10 -n 2000

python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$INPUT_FOLDER/100/" -input_path "$RESULTS_FOLDER/w2v/100_10" -runs 10 -n 100
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$INPUT_FOLDER/500/" -input_path "$RESULTS_FOLDER/w2v/500_10" -runs 10 -n 500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$INPUT_FOLDER/1000/" -input_path "$RESULTS_FOLDER/w2v/1000_10" -runs 10 -n 1000
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$INPUT_FOLDER/1500/" -input_path "$RESULTS_FOLDER/w2v/1500_10" -runs 10 -n 1500
python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$INPUT_FOLDER/2000/" -input_path "$RESULTS_FOLDER/w2v/2000_10" -runs 10 -n 2000

