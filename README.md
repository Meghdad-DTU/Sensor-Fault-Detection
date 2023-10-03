## Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

## Solution Proposed
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

## Deploymnet
- 1. Login to AWS console
- 2. Create IAM user for deploymnet with specific access
    - EC2 access: It is virtual machine
    - S3 bucket: To store artifacts and model is s3 bucket
    - ECR: Elastic Container Registry to save docker image in aws

## Description about deployment
- 1. Build docker image of the source code
- 2. Push your docker image to ECR
- 3. Launch EC2 instance
- 4. Pull your image from ECR in EC2 instance
- 5. Launch your docker image in EC2 instance


