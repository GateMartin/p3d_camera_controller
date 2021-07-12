# Panda3D Camera Controller
A simple camera controller for the Panda3D engine.</br>
It allows you to move with ZQDS (that's because I'm french ;)) keys and to look around or move with the mouse.</br></br>
You can easily change the default keys in order to setup a WASD configuration (How to just after the section right below).

## Example of use
```python
from direct.showbase.ShowBase import ShowBase
from camera import CameraControllerBehaviour

class MyApp(ShowBase):
    def __init__(self):
        super.__init__()
        # Load a model
        cube = self.loader.loadModel("models/box.egg")
        cube.reparentTo(self.render)
        
        # Setting up the camera controller
        cam_controller = CameraControllerBehaviour(self.camera) # Apply the behaviour to the showbase camera object
        cam_controller.setVelocity(0.2)
        cam_controller.setMouseSensivity(0.1)
        
        cam_controller.setup()
 
if __name__ in '__main__':
  MyApp().run()
```
## WASD Setup
In order to change the default keyboard controls to a WASD confguration, you need to pass this dictionary inside the setup method of the controller :
```python
cam_controller.setup(keys={
            'w':"forward",
            's':"backward",
            'a':"left",
            'd':"right",
            'space':"up",
            'lshift':"down"
        })
 ```
 Note: You can put whatever key you want as long as they are supported by Panda3D (see <a href="https://docs.panda3d.org/1.10/python/programming/hardware-support/keyboard-support"></a>).
