---
layout: default
title: Project Stage 3
nav_order: 4
---

# Project Stage 3
{: .no_toc }

Entity matching
{: .fs-5 .fw-300 }

---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## Matching Fodors and Zagats
+ **user ID**: group11    
+ **project ID**: try  

![result screenshot](https://raw.githubusercontent.com/chen-xanadu/cs839-website/master/stage3/result.png)


---

## Blocking Results

+ **user ID**: group11    
+ **project ID**: stage3


![blocking screenshot](https://raw.githubusercontent.com/chen-xanadu/cs839-website/master/stage3/blocking.PNG)

---

## Matching Results

+ **user ID**: group11    
+ **project ID**: stage3

![matching screenshot](https://raw.githubusercontent.com/chen-xanadu/cs839-website/master/stage3/matching.PNG)

--- 

## Estimating Accuracy

Data downloaded from CloudMatcher:
- [**Prediction list**](https://github.com/chen-xanadu/cs839-website/blob/master/stage3/prediction_list)  
- [**Candidate set**](https://github.com/chen-xanadu/cs839-website/blob/master/stage3/candidate_set)  
- [**Table A**](https://github.com/chen-xanadu/cs839-website/blob/master/stage3/tableA_meta)  
- [**Table B**](https://github.com/chen-xanadu/cs839-website/blob/master/stage3/tableB_imdb)  

The size of our candidate set C is **2098**.  
- In [**this PDF**](https://chen-xanadu.github.io/cs839-website/reports/stage3.pdf), we discussed the density computation.
- Since no new blocking rules is added, the final candidate set remains unchanged.
- Link to the set of 400 tuple pairs that are sampled and manually labeled: [**sample400.csv**](https://github.com/chen-xanadu/cs839-website/blob/master/stage3/sample400.csv)
- Using [**the Jupyter notebook**](https://nbviewer.jupyter.org/github/chen-xanadu/cs839-website/blob/master/stage3/estimating_precision_recall.ipynb), the accuracy we obtained is
```
Recall = [1.0 - 1.0]   
Precision = [0.98 - 1.00]     
```
