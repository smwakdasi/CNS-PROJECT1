\# CNS-PROJECT: Ransomware Detection Tool



This project uses real-time monitoring and a machine learning classifier (Random Forest) to detect ransomware behavior on local systems.



\## Features

\- Trains on structured malware feature data

\- Predicts ransomware vs benign behavior

\- Saves trained model (`ransomware\_model.pkl`)

\- (Optional) Real-time CLI monitoring with `watchdog`/`psutil`



\## How to Use

1\. Clone repo

2\. Run `train\_model.py`

3\. Load model in real-time script



\## Tools

\- Python, Pandas, Scikit-learn, Matplotlib



