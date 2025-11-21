# Transmission_vs_congestiondelay_analyzer
🚀 Transmission vs. Congestion Delay Analyzer

A lightweight, interactive tool designed to analyze and visualize the difference between transmission delay and congestion delay in computer networks. This project helps students, researchers, and network engineers understand how packet size, bandwidth, and network load affect total network latency.

📌 Overview

Traditional network monitoring tools often provide only overall latency, making it difficult to identify whether delays are caused by data transmission limitations or network congestion.
This analyzer breaks down latency into:

Transmission Delay – Time required to push packet bits onto the link.

Congestion Delay – Queuing delay caused by traffic, bottlenecks, or overloaded links.

The tool provides an interactive platform to simulate different network scenarios, visualize delay behavior, and perform performance analysis with clarity.

🔍 Features

Simulates network delays based on real-world parameters.

Inputs: packet size, bandwidth, traffic load, link capacity.

Separate computation of transmission & congestion delays.

Generates graphs showing delay trends and bottlenecks.

Real-time updates for parameter changes.

Ideal for networking labs, academic use, or research demonstrations.

🧩 Project Modules

Input & Data Processing Module
Handles user input, validates network parameters, and processes topology data.

Delay Computation Engine
Calculates transmission delay, congestion delay, and total network latency.

Visualization & Output Module
Displays interactive graphs, analytics panels, and downloadable reports.

📈 Use Cases

Network performance study

Teaching networking concepts

Research simulations

Delay comparison and bottleneck identification

🛠️ Tech Stack

Python / JavaScript (depending on your implementation)

Matplotlib / Chart.js for visualization

Flask / Node.js (optional for web interface)

📚 How It Works

Enter network parameters like packet size, bandwidth, and load.

The system calculates transmission & congestion delays separately.

A graphical dashboard visualizes delay changes dynamically.

Users can export delay reports for analysis.

📄 Future Enhancements

Support for real-time network data import

Integration with ML-based delay prediction

Multi-node topology simulation

Advanced congestion modeling
