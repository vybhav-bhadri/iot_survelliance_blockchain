## Pi Face detection - IoT Network
Goal of project is to store detected images in a distributed database. Hyperledger fabric is used to store detected images. This readme file explains how to setup the IoT network which sends detected images to IoT Gateway.

## Note - branch testjson has the working code, changes will be commited to master in future

## Table of contents
* [Technolgies](#technologies)
* [Setup](#setup)
* [Snapshots](#snapshots)

## Technologies and modules
Project is created using:
* Python 3
* Flask
* HTML,CSS for frontend
* python requests to send post data

## Pi camera Setup
In this project Pi acts as a IP camera. Before running code, check if pi camera is working. You can also use a web-cam to run this project.
Open termianl
```
$ sudo raspi-config
```
Selelt Interface, then enable Pi camera and select Finish.
Check that camera is working by running this command in terminal
```
$ raspistill -o imgname.jpg

```
## Project Setup
Clone the project using the following command
```
$git clone git@github.com:vybhav-bhadri/pi-face_detection.git
```
This project is using openCV which creates camera objects, and haar cascade classifier is used for facial detection. Install openCV using the folllowing commnads.
```
$sudo apt update
$sudo pip install python3-opencv
```
Navigate to the repository directory
```
$ cd pi-face_detection
```
Install all the dependencies by running this command
```
$pip install -r requirements.txt
```
## Run the Program
Start server
```
$python3 run.py
```
In code main.py has logic to send JSON Data, camera.py has the logic to detect faces

```
payload = json.dumps({"Face_Id":face_id,"ImageData": im_b64,"Timestamp":timestamp,"Device_Id":device_id},default=str)
```
To send post request to an api end point
```
response = requests.post(api_test, data=payload, headers=headers)
```
Stream can be viewed by entering localhost:5000 in your browser.You can also access the stream locally by entering ip address of the rasberry pi running the server.
To find the local IP address of your Pi, open terminal and run
```
$ifconfig
```
To access stream remotely, use ngrok to expose a local tunnel. Start the local server and run ngrok with this command,
visit [ngrok](https://ngrok.com/) and check documentation for setup.
```
$./ngrok http 5000
```
This will generate a link and use this link to access stream.

### Note : If face is detected, captured image is converted into base64 format and is sent to IoT gateway along with device id,face id and timestamp at which image is captured.

# Snapshots

## Rasberry pi setup
![IMG_20210629_181909](https://user-images.githubusercontent.com/54641149/124130854-d64c2580-da9c-11eb-8f89-3cd8644014a9.jpg)

### Note: If face is detected, data is sent as a JSON object to IoT gateway
