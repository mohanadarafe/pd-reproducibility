# Meeting Notes
The following log is dedicated to keep track of meetings & discussions from the authors of this project.

## November 3rd, 2021
In this meeting, we discussed that we will be reproducing a mixture of two papers, namely:

1 - [Automated Categorization of Parkinsonian Syndromes Using Magnetic Resonance Imaging in a Clinical Setting](https://pubmed.ncbi.nlm.nih.gov/33137232/)

2 - [Predicting the progression of Parkinson's disease using conventional MRI and machine learning: An application of radiomic biomarkers in whole-brain white matter.](https://onlinelibrary.wiley.com/doi/abs/10.1002/mrm.28522)

Paper 1 will be used as the main pipeline we will be reproducing and paper 2 will be used to build the dataset. The output will be stable (low-risk) vs progressive (high-risk) PD. 

Additionally, we spoke to Dr.Yimimg Xiao who will collaboratw with us and provide us a ready PPMI dataset. The data transfer will occur November 8th.

**Goals for the following week:**
- Start GitHub repository
- Build initial pipeline to extract volumes from PPMI data


## November 9th, 2021
In this meeting, we went over the progress made in the code to extract volumes from brain data. We discussed the following issues I need to address:

- Compute Canada registration
- Use Boutiques to get FreeSurfer recon-all
- Normalization of data

After acquiring Yiming's data, there is no metadata. This means that I might have to manually get the metadata from PPMI manually which might take some time (tedious task!).

**Goals for the following week:**
- Convert data to one dataframe for each class (PD, NC)
- Register to compute canada