# Patchy-san
Implementation of Patchy-san in Chainer

# Preprocess
Each graph needs to be preprocessed according to the following procedures:
- load a graph
- calculate centrality
- make a node sequence
- make a receptive field
- canonize labels
- make x
- save x whose shape is (batch_size, in_channels, rf_size, node_size)

Use `run_preprocess_data` in order to do those ones.

# Collection of Small Dataset
Datasets were downloaded from [this site](https://www.bsse.ethz.ch/mlcb/research/machine-learning/graph-kernels/halting-in-random-walk-kernels.html).
The datasets contain the following directories:
- DD
- NCI1
- NCI109: unused
- ENZYMES: Avg = 32.63
- MUTAG

Those directories are placed under the following directories:
- local machine: /Volumes/Untitled/mac/Data/graphml/data_graphml

Preprocessed datasets are located under the following directories:
- local machine: /Volumes/Untitled/mac/Data/graphml/data_graphml/preprocessed
- EC2: /home/ubuntu/data/patchy_san/preprocessed

# Collection of Big Dataset
Datasets were downloaded from [this site](http://www.mit.edu/~pinary/).
An original paper is in [this site](https://users.soe.ucsc.edu/~vishy/pubs/YanVis15.pdf).
The datasets contain the following files:
- collab.graph (big) Avg: 74.4948, Graphs: 5000, Classes: 3
- enzymes.graph (already shown above)
- imdb_action_romance.graph (big)
- imdb_comedy_romance_scifi.graph (big)
- mutag.graph(already shown above)
- nci1.graph (already shown above)
- nci109.graph(already shown above)
- proteins.graph
- ptc.graph
- reddit_iama_askreddit_atheism_trollx.graph (big)
- reddit_multi_5K.graph (big)
- reddit_subreddit_10K.graph (big)

Those directories are placed under the following directories:
- local machine: /Volumes/Untitled/mac/Data/patchy-san/datasets  

These datasets do not have the format of graphml.
Use `run_preprocess_data_2` to make them have the form available for graph_tool library.
Preprocessed datasets are located under the following directories:
- local machine: /Volumes/Untitled/mac/Data/patchy-san/datasets/for_graph_tool 
- EC2: 

After running the above procredure, run `run_preprocess_data` with a new option kind=1.

# Execution of CNN
- Training is executed by `run_train`.
- Optimal parameters are selected by `run_hyperopt`.
- A network structure is fixed except for an epoch and a batch size.
