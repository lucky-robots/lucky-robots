# Lucky Robots
## Robotics AI Training in Hyperrealistic Game Environments

Lucky Robots: Where robots come for a boot camp, like going to a spa day! 🤖💆‍♂️ We use the fancy Unreal Engine 5.2, Open3D and YoloV8 to create a lavish, virtual 5-star resort experience for our metal buddies so they're absolutely pumped before they meet the real world. Our training framework? More like a robotic paradise with zero robot mishaps. "Gentle" methods? We're practically the robot whisperers here, you won't see humans with metal sticks around. That's why it's "Lucky Robots" because every robot leaves our sessions feeling like they just won the jackpot – all without a scratch! 🎰🤣

Joking aside, whether you're an AI/ML Developer, aspiring to design the next Roomba, or interested in delving into robotics, there's no need to invest thousands of dollars in a physical robot and attempt to train it in your living space. With Lucky, you can master the art of training your robot, simulate its behavior with up to 90% accuracy, and then reach out to the robot's manufacturer to launch your new company.

Remember, no robots were emotionally or physically harmed in our ultra-luxurious training process. Thus, Lucky Robots!

Cheers to happy, and more importantly, unbruised robots! 🍀🤖🎉



https://github.com/lucky-robots/lucky-robots/assets/203507/6c29b881-2ff6-4734-ad33-71c09ad75b62



(Note for the repository: since it's almost impossible to develop a large game like this on github due to file size and bandwidth limitations (our repo is currently +250gb, we've moved our unreal source code to a local Perforce server, we'll find a way to share that with the public soon. if you need access please leave reach out, I will give you FTP access)

### ** WHAT WE ARE WORKING ON NEXT **

*   Camera Poses coming from Unreal (to have faster AI training)
*   Depth map provided by Unreal (We tried [MiDAS](https://github.com/isl-org/MiDaS) and [DepthAnything](https://github.com/LiheYoung/Depth-Anything) they work great but not 100%. We're certain this problem will be solved soon and we will simulate this in the meanwhile)
*   Fully integrate with [ConceptGraphs](https://concept-graphs.github.io/) [Ali](https://github.com/alik-git) Welcome to our team! 🚀🚀🚀

** UPDATE 3/6 **

We have designed [Stretch 3 Robot](https://hello-robot.com/stretch-3-product) and working on adding this robot to our world

<img width="504" alt="image" src="https://github.com/lucky-robots/lucky-robots/assets/203507/54b1bbbc-67e0-4add-a58f-84b08d14e680">


** UPDATE 1/6 **

WE GOT OUR FIRST TEST LINUX BUILD (NOT THE ACTUAL WORLD, THAT'S BEING BUILT) (TESTED ON UBUNTU 22.04)

https://drive.google.com/file/d/1_OCMwn8awKZHBfCfc9op00y6TvetI18U/view?usp=sharing


** UPDATE 2/15 **

[Luck-e World second release is out (Windows only - we're working on Linux build next)!](https://drive.google.com/drive/folders/10sVx5eCcx7d9ZR6tn0zqeQCaOF84MIQt)


** UPDATE 2/8 **

We are now writing prompts against the 3d environment we have reconstructed using point clouds...


https://github.com/lucky-robots/lucky-robots/assets/203507/a93c9f19-2891-40e1-8598-717ad13efba6




** UPDATE 2/6 **

Lucky first release: https://drive.google.com/file/d/1qIbkez1VGU1WcIpqk8UuXTbSTMV7VC3R/view?amp;usp=embed_facebook

Now you can run the simulation on your Windows Machine, and run your AI models against it. If you run into issues, please submit an issue.

** UPDATE 1/15 **

Luck-e is starting to understand the world around us and navigate accordingly!

https://github.com/lucky-robots/lucky-robots/assets/203507/4e56bbc5-92da-4754-92f4-989b9cb86b6f


** UPDATE 1/13 **

We are able to construct a 3d world using single camera @niconielsen32

https://github.com/lucky-robots/lucky-robots/assets/203507/f2fd19ee-b40a-4fef-bd30-72c56d0f9ead



** UPDATE 12/29 **
We are now flying! Look at these environments, can you tell they're not real?

![Screenshot_18](https://github.com/lucky-robots/lucky-robots/assets/203507/f988a18e-9dc3-484e-9d9f-eb7ad57180b2)
![Screenshot_17](https://github.com/lucky-robots/lucky-robots/assets/203507/f423d73f-d336-47b6-abf0-6f1b174bd740)
![Screenshot_19](https://github.com/lucky-robots/lucky-robots/assets/203507/7f2b9ae2-f84f-41a1-8511-959e2586b809)
![Screenshot_15](https://github.com/lucky-robots/lucky-robots/assets/203507/d65a0fb4-3a4d-4207-9181-2de0e2ce63ce)
![Screenshot_11](https://github.com/lucky-robots/lucky-robots/assets/203507/cf328e8d-fc40-4be3-81ac-a900d0505fd8)
![Screenshot_14](https://github.com/lucky-robots/lucky-robots/assets/203507/5ae9bf2d-246b-437f-ba1b-901a7f10b1fa)
![Screenshot_12](https://github.com/lucky-robots/lucky-robots/assets/203507/e2f0684e-ca18-40b0-8680-76ccec918171)
![Screenshot_8](https://github.com/lucky-robots/lucky-robots/assets/203507/26904b69-c8b8-467d-8355-595cc62ead3f)
![Screenshot_7](https://github.com/lucky-robots/lucky-robots/assets/203507/e43e25b0-b68d-4c1e-9a7d-800b9cf5312b)


** UPDATE 12/27 **

Lucky now has a drone  - like the Mars Rover! When it's activated camera feed switches to it automatically!



https://github.com/lucky-robots/lucky-robots/assets/203507/29103a5a-a209-4d49-acd1-adad88e5b590



** UPDATE 5/12 **

Completed our first depth map using Midas monocular depth estimation model


https://github.com/lucky-robots/lucky-robots/assets/203507/647a5c32-297a-4157-b72b-afeacdaae48a



https://user-images.githubusercontent.com/203507/276747207-b4db8da0-a14e-4f41-a6a0-ef3e2ea7a31c.mp4

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)
- [Join Our Team](#join-our-team)
- [License](#license)

## Features

1. **Realistic Training Environments**: Train your robots in various scenarios and terrains crafted meticulously in Unreal Engine.
2. **Python Integration**: The framework integrates seamlessly with Python 3.10, enabling developers to write training algorithms and robot control scripts in Python.
3. **Safety First**: No physical wear and tear on robots during training. Virtual training ensures that our robotic friends remain in tip-top condition.
4. **Modular Design**: Easily extend and modify the framework to suit your specific requirements or add new training environments.

## Requirements

- Unreal Engine 5.2
- Python 3.10
- Modern GPU and CPU for optimal performance

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/lucky-robots/lucky-robots.git
   cd lucky-robots
   ```

2. **Setup Python Environment**

   Ensure you have Python 3.10 installed. Set up a virtual environment:

   ```
   # Windows Powershell
   python -m venv lr_venv
   .\lr_venv\Scripts\activate.ps1
   pip install -r requirements.txt
   ```

3. **Setup PixelStreaming**

   - Run `setup.bat` located in `Resources\SignalingWebServer\platform_scripts\cmd`

4. **Launch Unreal Project**

   Open the provided `controllable_pawn.uproject` file in Unreal Engine 5.2 and let it compile the necessary assets and plugins.


## Usage

1. **Start Unreal Simulation**

   - Run `.\run_pixel_streaming_server.ps1`
   - Inside Unreal Editor you have a big green Play button. before you click that, there is a three dot icon next to it that says "Change Play Mode and Play Settings"
   - Click that and then tick "Standalone Game" 
   - Launch the game by clicking that Play button and play the simulation scenario you wish to train your robot in.
   - Then you can browse to http://127.0.0.1/?StreamerId=LeftCamera and to http://127.0.0.1/?StreamerId=RightCamera to see what your robot is seeing (optional).

2. **Run Python Training Script**

   With the simulation running, execute your Python script to interface with the Unreal simulation and start training your robot.

   ```bash
   python main.py
   ```

## Support

For any queries, issues, or feature requests, please refer to our [issues page](https://github.com/LuckyRobots/LuckyRobotsTrainingFramework/issues).

## Contributing

We welcome contributions! Please read our [contributing guide](CONTRIBUTING.md) to learn about our development process, how to propose bugfixes and improvements, and how to build and test your changes to Lucky Robots.

## Join our team?

Absolutely! Ideally contribute a few PRs and let us know!

## License

Lucky Robots Training Framework is released under the [MIT License](LICENSE.md).

---

Happy training! Remember, be kind to robots. 🤖💚
