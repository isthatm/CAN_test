- This repo simulate communication abiding by UDS protocol between tester tool and automotive ECUs.
- For demo purposes, serveral services are introduced in `can_test/test_services.py` file.
- The main logic for sending/receiving messages is handled by a simulated ECU in `can_test/can_node.py`.
- Test cases are implemented automatically with RobotFramework in the `test_suite.robot` file.
- This program utilizes [hardbyte/python-can](https://github.com/hardbyte/python-can)
  and [pylessard/python-can-isotp](https://github.com/pylessard/python-can-isotp) libraries.
- The whole program can be sectioned into 3 parts as displayed in the below diagram (from the bottom to top layer):
  + 1st: Handles the incoming/outcoming messages between the application layer and lower can nodes
  + 2nd: Defines supported services by the program, contructs message payloads to be sent to can nodes
  + 3rd: Application layer, testers define services that they wish to get the information from

    
![Picture1](https://github.com/user-attachments/assets/7c21d6fc-b5fc-4ac4-b364-3ffe0fadaf83)
