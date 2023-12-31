# Insulin advisor with meal announcement using deep Reinforcement Learning

Project for diabetics management by NL,PB  
This project aims to compare two RL models, one without meal detection and one with meal detection. 
For this purpose the basic implementations the [T1D simulator](https://github.com/jxx123/simglucose) was used. 
The project is based on previous projects [RL-Project](https://github.com/miopp2/diabetes-RL-project/tree/main) and [Meal Detection](https://github.com/bodging/DiabetsTechMeatDetection) which were updated (due to simglucose updates), adapted and combined.

# Installation

To install the repository and all required packages:

```bash
git clone https://github.com/Rbeyan/Diabetics
cd Diabetics

pip install simglucose
pip install gym==0.21
pip install -r requirements2.txt
```
 

# Results

The model is successfully updated and made compatible with new simglucose Simulator environment.   
The meal detection is rewritten into Pytorch to ensure compatibility.    
The fine-tuning of the parameters was not successfull therefore no comparison could be made. The models are located in RL_models. Pre-implementation of model into BB controller and PPO controller was done.



