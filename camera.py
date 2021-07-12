# coding:utf-8
from direct.showbase.DirectObject import DirectObject
from direct.controls.InputState import InputState
from direct.task import Task

from panda3d.core import WindowProperties


class CameraControllerBehaviour(DirectObject):
    _instances = 0
    
    def __init__(self, camera, velocity=0.1, mouse_sensivity=0.2, showbase=None):
        """
        Create a camera controller behaviour for a specified camera.        
        """
        self._camera = camera
        self._velocity = velocity
        self._mouse_sensivity = mouse_sensivity
        self._keys = None
        self._input_state = InputState()
        self._showbase = base if showbase is None else showbase

        # Variables for camera rotation
        self._heading = 0.0
        self._pitch = 0.0

        self._instance = CameraControllerBehaviour._instances
        CameraControllerBehaviour._instances += 1

    def setup(self, keys={
        'z':"forward",
        's':"backward",
        'q':"left",
        'd':"right",
        'space':"up",
        'lshift':"down"
    }):
        """
        Setup the camera behaviour.
        """
        # Disable default mouse controls
        self._showbase.disableMouse()

        # Hide the mouse
        props = WindowProperties()
        props.setCursorHidden(True)

        self._showbase.win.requestProperties(props)

        # Setting up key bindings
        self._keys = keys
        for key in self._keys:
            self._input_state.watchWithModifiers(self._keys[key], key)

        # Add camera task to the showbase task manager
        self._showbase.taskMgr.add(self.update, "UpdateCameraTask" + str(self._instance))
    
    def destroy(self):
        """
        Destroy the camera behaviour (it won't be usable anymore)
        """
        self.disable()
        self._input_state.delete()

        del self

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity

    def setVelocity(self, velocity):
        """
        Set camera velocity while moving.
        """
        self._velocity = velocity

    @property
    def mouse_sensivity(self):
        return self._mouse_sensivity

    @mouse_sensivity.setter
    def mouse_sensivity(self, sensivity):
        self._mouse_sensivity = sensivity

    def setMouseSensivity(self, sensivity=0.2):
        """
        Set camera sensivity while looking around (default is 0.2).
        """
        self._mouse_sensivity = sensivity

    def disable(self):
        """
        Disable the camera behaviour.
        Note: the behaviour is still usable, you can use setup() in order to activate it again.
        """
        # Remove camera task from the showbase task manager
        self._showbase.taskMgr.remove("UpdateCameraTask" + str(self._instance))

        # Show the mouse
        props = WindowProperties()
        props.setCursorHidden(False)

        self._showbase.win.requestProperties(props)            
        
    def update(self, task):
        """
        Task to update camera's position and rotation based on inputs.
        """
        dt = globalClock.getDt()

        # Getting mouse position
        md = self._showbase.win.getPointer(0)
	 
        x = md.getX()
        y = md.getY()
        center_x = self._showbase.win.getXSize() // 2
        center_y = self._showbase.win.getYSize() // 2
        
        if self._showbase.win.movePointer(0, center_x, center_y):
            self._heading = self._heading - (x - center_x) * self._mouse_sensivity
            self._pitch = self._pitch - (y - center_y) * self._mouse_sensivity
        
        # Set camera rotation based on mouse position
        self._showbase.camera.setHpr(self._heading, self._pitch, 0)

        pos_increment = dt * self._velocity * 60.0

        # Setting camera position based on inputs        
        if  self._input_state.isSet('forward'):
            self._showbase.camera.setY(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('backward'):
            self._showbase.camera.setY(self._showbase.camera, -pos_increment)

        if  self._input_state.isSet('left'):
            self._showbase.camera.setX(self._showbase.camera, -pos_increment)

        if  self._input_state.isSet('right'):
            self._showbase.camera.setX(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('up'):
            self._showbase.camera.setZ(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('down'):
            self._showbase.camera.setZ(self._showbase.camera, -pos_increment)        
    
        return Task.cont


# Tests
if __name__ in '__main__':
    from direct.showbase.ShowBase import ShowBase
    
    showbase = ShowBase()

    box = showbase.loader.loadModel("models/box.egg")
    box.reparentTo(showbase.render)

    cam_controller = CameraControllerBehaviour(showbase.camera)
    cam_controller.setVelocity(0.2)
    cam_controller.setMouseSensivity(0.9)
    cam_controller.setup()

    showbase.run()