#!/bin/sh
# 500 pairs. 10 samples.
# python3 /Users/ftesone/dev/big_data_text_similarity/computeDistance.py -t w2v -q data/question_pairs.csv -results_path "/Users/ftesone/Documents/Tesis/experiments/ensembles/inputs" -k 10 -n 500
# python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k 5 -clustering_runs 100 -in_progress_experiment_path "" -calc_distances_enabled -clustering_enabled -ensemble_enabled -start_from_sample_num 9

INPUT_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/inputs/w2v/500_10"
RESULTS_FOLDER="/Users/ftesone/Documents/Tesis/experiments/ensembles/results"
ORIGIN_FOLDER="samples_size_500_count_10_k_5_runs_100_202006071735"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_10_runs_100_202006130001"
k=10
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_15_runs_100_202006130001"
k=15
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_20_runs_100_202006130001"
k=20
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_25_runs_100_202006130001"
k=25
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_30_runs_100_202006130001"
k=30
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_35_runs_100_202006130001"
k=35
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_40_runs_100_202006130001"
k=40
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_45_runs_100_202006130001"
k=45
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################

DEST_FOLDER="samples_size_500_count_10_k_50_runs_100_202006130001"
k=50
rm -rf /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/*
for i in 1 2 3 4 5 6 7 8 9 10
do
  mkdir /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/distances /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
  cp -r /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$ORIGIN_FOLDER/500_$i/pairs /Users/ftesone/Documents/Tesis/experiments/ensembles/results/$DEST_FOLDER/500_$i
done

python3 /Users/ftesone/dev/big_data_text_similarity/clusterEnsemble.py -techniques bow,gtfidf,w2v,ft,sem -questions_path $INPUT_FOLDER -results_path $RESULTS_FOLDER -sample_size 500 -samples_number 10 -k $k -clustering_runs 100 -in_progress_experiment_path $DEST_FOLDER -clustering_enabled -ensemble_enabled
python3 /Users/ftesone/dev/big_data_text_similarity/confusion_matrix_ensembles.py -runs 10 -sample_size 500 -experiment_path "$RESULTS_FOLDER/$DEST_FOLDER"

###################################################################################################################################