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

## November 16th, 2021
In this meeting, we showed progress in the code having developed a preprocessing pipeline to execute a job in Compute Canada to extract volumes for all patients. Also, we talked about how I will pick the sample size of each classes (NC, PD). 

For the sampling of data, I am yet to decide. In terms of the COMP691 project, it would be best to match the dataset to the paper we are replicating and keep it simple. 

**Goals for the following week:**
- Execute FreeSurfer volume extraction jobs in Compute Canada
- Start ML pipeline

## November 22nd, 2021
In this meeting, we discussed the progrssions of the Compute Canada job. On this date, all 216 patients scans are being ran in Compute Canada. Once the volumes are extracted, the data will be used to start the machine learning pipeline. Over the last week, I wrote code to start the ML pipeline in a notebook. The pipeline will include conversion from CSV to DF, training models, normalize data and making predictions.

**Goals for the following week:**
- Download metadata from PPMI to get scanner types
- Write methods to normalize data
- Continue ML pipeline

**Additional note:**

I need to use the correct volumes from FreeSurfer. The following lists are a breakdown of what I have, what I need and what is available to me.

ROI's missing
-------------------------------
- Midbrain
- Pons
- Posterior putamen
- SCP
- Insula
- Precentral cortex
- Insular cortex

ROIs present (currently using)
-------------------------------
- Putamen
- Caudate
- Thalamus
- Pallidum
- CerebralWhiteMatterVol
- 3rd and 4th ventricles

ROI's available from FreeSurfer
-------------------------------
- Left-Lateral-Ventricle
- Left-Inf-Lat-Vent
- Left-Cerebellum-White-Matter
- Left-Cerebellum-Cortex
- Left-Thalamus
- Left-Caudate
- Left-Putamen
- Left-Pallidum
- 3rd-Ventricle
- 4th-Ventricle
- Brain-Stem
- Left-Hippocampus
- Left-Amygdala
- CSF
- Left-Accumbens-area
- Left-VentralDC
- Left-vessel
- Left-choroid-plexus
- Right-Lateral-Ventricle
- Right-Inf-Lat-Vent
- Right-Cerebellum-White-Matter
- Right-Cerebellum-Cortex
- Right-Thalamus
- Right-Caudate
- Right-Putamen
- Right-Pallidum
- Right-Hippocampus
- Right-Amygdala
- Right-Accumbens-area
- Right-VentralDC
- Right-vessel
- Right-choroid-plexus
- th-Ventricle
- WM-hypointensities
- Left-WM-hypointensities
- Right-WM-hypointensities
- non-WM-hypointensities
- Left-non-WM-hypointensities
- Right-non-WM-hypointensities
- Optic-Chiasm
- CC_Posterior
- CC_Mid_Posterior
- CC_Central
- CC_Mid_Anterior
- CC_Anterior