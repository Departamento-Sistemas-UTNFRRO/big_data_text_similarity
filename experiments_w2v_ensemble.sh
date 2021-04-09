# w2v
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble"

#python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "$RESULTS_FOLDER" -k 10 -n 500
#python3 /Users/ftesone/dev/big_data_text_similarity/confusionMatrix.py -technique w2v -samples_path "$RESULTS_FOLDER/w2v/500_10/" -input_path "$RESULTS_FOLDER/w2v/500_10" -runs 10 -n 500

# Ensemble
INPUT_FOLDER="$RESULTS_FOLDER/w2v/500_10"
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal"

#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques w2v -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k 50 -clustering_runs 500 -in_progress_experiment_path "" -calc_distances_enabled -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/samples_size_500_count_10_k_50_runs_500_202009261929"

#ORIGIN_FOLDER="samples_size_500_count_10_k_100_runs_100_202009261601"
#DEST_FOLDER="samples_size_500_count_10_k_50_runs_100_202009261601"
#k=50
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$DEST_FOLDER
#for i in 1 2 3 4 5 6 7 8 9 10
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$DEST_FOLDER/500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$DEST_FOLDER/500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/w2v_ensemble/equal/$DEST_FOLDER/500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques w2v_1,w2v_2,w2v_3,w2v_4,w2v_5 -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
#python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"