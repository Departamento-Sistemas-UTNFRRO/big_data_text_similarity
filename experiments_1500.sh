###!/bin/sh
### 1500 pairs. 10 samples.
#python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "/Users/ftesone/Documents/Tesis/experiments/ensembles/inputs" -k 10 -n 1500

INPUT_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/inputs/w2v/1500_10"
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/results"
ORIGIN_FOLDER="samples_size_1500_count_10_k_50_runs_100_202007191143" # STARTING FROM k = 50!

#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k 50 -clustering_runs 50 -in_progress_experiment_path $ORIGIN_FOLDER -calc_distances_enabled -clustering_enabled -ensemble_enabled -start_from_sample_num 2
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$ORIGIN_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_5_runs_100_202007121800"
#k=5
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques w2v,bow,gtfidf,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"
#
####################################################################################################################################
#
DEST_FOLDER="samples_size_1500_count_10_k_10_runs_100_202007121800"
#k=10
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

##################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_15_runs_100_202007121800"
#k=15
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done

#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled -start_from_sample_num 3
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

##################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_20_runs_100_202007121800"
#k=20
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

##################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_25_runs_100_202007121800"
k=25
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

##################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_30_runs_100_202007121800"
#k=30
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"
#
###################################################################################################################################
#
DEST_FOLDER="samples_size_1500_count_10_k_35_runs_100_202007121800"
#k=35
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"
#
####################################################################################################################################
#
DEST_FOLDER="samples_size_1500_count_10_k_40_runs_100_202007121800"
#k=40
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_1500_count_10_k_45_runs_100_202007121800"
#k=45
#mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER
#for i in 1 2 3 4 5
#do
#  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/1500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/1500_$i
#done
#
#python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 1500 -samples_number 5 -k $k -clustering_runs 50 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 5 -sample_size 1500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################