# Panda3D Camera Controller
A simple camera controller for the Panda3D engine.</br>
It allows you to move with WASD keys and to look around or move with the mouse.

## Example of use
'''python
from direct.showbase.ShowBase import ShowBase
from camera import CameraControllerBehaviour

class MyApp(ShowBase):
  def __init__(self):
    super.__init__()
    # Load a model
    cube = self.loader.loadModel("models/box.egg")
    cube.reparentTo(self.render)
    
    # Setting up the camera controller
    cam_controller = CameraControllerBehaviour
    cam_controller.setVelocity(0.2)
    cam_controller.setMouseSensivity(0.1)
    
    cam_controller.setup()
 
if __name__ in '__main__':
  MyApp().run()

'''
