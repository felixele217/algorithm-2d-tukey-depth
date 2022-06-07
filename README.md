# algorithm-2d-tukey-depth

The implementation of this algorithm has been developed under WSL with Ubuntu. To run the code, you need to clone the repository for example via https with
```
git clone https://github.com/felixele217/algorithm-2d-tukey-depth.git
```

Then, you need to install python3, pip (a package manager for python packages) and the library matplotlib, which is needed for plotting the graph. In WSL, you can do this with the following commands:
```
sudo apt update && upgrade
sudo apt install python3 python3-pip ipython3
pip install matplotlib
```

The command 
```
python --version
```
tells you, if you have successfully installed python.

To run the program, please navigate to the folder of the project in a terminal of your choice and execute the command
```
python3 main.py
``` 
to run the program.  

For example, I am using Visual Studio Code and therefore I could run the program in my integrated terminal like this:  
![image](https://user-images.githubusercontent.com/50794814/172377711-07f6223b-aaa1-4b59-8704-d959dcdfe40b.png)

The images will be saved in the plots/ directory, which is included in the project folder. Feel free to experimentate with the input size in main.py
![image](https://user-images.githubusercontent.com/50794814/172378099-49e100dc-9e05-4253-a24d-a0b64edceb40.png)  
and the range in which the random points are generated in algorithm.py
![image](https://user-images.githubusercontent.com/50794814/172378431-eb54f85e-460d-4378-afef-d53a6318e4c2.png)  
The second argument takes the range for the x-coordinate in [-xrange, xrange] and the third argument takes the range for the y-coordinate analog.







