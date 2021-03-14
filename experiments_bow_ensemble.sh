# Bow
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble"

# python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t bow -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -k 10 -n 500
# python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique bow -samples_path "$RESULTS_FOLDER/bow/500_10/" -input_path "$RESULTS_FOLDER/bow/500_10" -runs 10 -n 500

# Ensemble
INPUT_FOLDER="$RESULTS_FOLDER/bow/500_10"
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal"

#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow_1,bow_2,bow_3,bow_4,bow_5 -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k 100 -clustering_runs 100 -in_progress_experiment_path "" -calc_distances_enabled -clustering_enabled -ensemble_enabled
#python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/samples_size_500_count_10_k_100_runs_100_202009261601"

ORIGIN_FOLDER="samples_size_500_count_10_k_100_runs_100_202009261601"
DEST_FOLDER="samples_size_500_count_10_k_50_runs_100_202009261601"
k=50
mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$DEST_FOLDER
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/bow_ensemble/equal/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow_1,bow_2,bow_3,bow_4,bow_5 -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"