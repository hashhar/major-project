#!/usr/bin/python2

from opensim import *

# Create an OpenSim model and set its name
osimModel = Model()
osimModel.setName("tugOfWar")

print "OpenSim example completed successfully.\n"

# Get a reference to the model's ground body
ground = osimModel.getGroundBody()

# Add display geometry to the ground to visualize in the GUI
ground.addDisplayGeometry("ground.vtp")
ground.addDisplayGeometry("anchor1.vtp")
ground.addDisplayGeometry("anchor2.vtp")

# Save the model to a file
osimModel.printToXML("tugOfWar_model.osim")

# Specify properties of a 20 kg, 0.1 m^3 block body
blockMass = 20.0
blockSideLength = 0.1
blockMassCenter = Vec3(0)
blockInertia = Inertia(blockMass*blockSideLength**2./6.)

# Create a new block body with specified properties
block = Body("block", blockMass, blockMassCenter, blockInertia)

# Add display geometry to the block to visualize in the GUI
block.addDisplayGeometry("block.vtp")

# Create a new free joint with 6 degrees-of-freedom (coordinates) between the block and ground bodies
locationInParent = Vec3(0, blockSideLength/2, 0)
orientationInParent = Vec3(0)
locationInBody = Vec3(0)
orientationInBody = Vec3(0)
blockToGround = FreeJoint("blockToGround", ground, locationInParent, orientationInParent, block, locationInBody, orientationInBody)

# Get a reference to the coordinate set (6 degrees-of-freedom) between the block and ground bodies
jointCoordinateSet = blockToGround.upd_CoordinateSet()

# Set the angle and position ranges for the coordinate set
angleRange = [-SimTK_PI/2, SimTK_PI/2]
positionRange = [-1, 1]

jointCoordinateSet.get(0).setRangeMin(angleRange[0])
jointCoordinateSet.get(0).setRangeMax(angleRange[1])
jointCoordinateSet.get(1).setRangeMax(angleRange[0])
jointCoordinateSet.get(1).setRangeMax(angleRange[1])
jointCoordinateSet.get(2).setRangeMax(angleRange[0])
jointCoordinateSet.get(2).setRangeMax(angleRange[1])
jointCoordinateSet.get(3).setRangeMax(positionRange[0])
jointCoordinateSet.get(3).setRangeMax(positionRange[1])
jointCoordinateSet.get(4).setRangeMax(positionRange[0])
jointCoordinateSet.get(4).setRangeMax(positionRange[1])
jointCoordinateSet.get(5).setRangeMax(positionRange[0])
jointCoordinateSet.get(5).setRangeMax(positionRange[1])

# Add the block body to the model
osimModel.addBody(block)

# Define the acceleration of gravity
osimModel.setGravity(Vec3(0,-9.80665,0))

# Initialize the system
si = osimModel.initSystem()

# Define non-zero (defaults are 0) states for the free joint
modelCoordinateSet = osimModel.updCoordinateSet()

# set x-translation value
modelCoordinateSet.get(3).setValue(si, blockSideLength)

# set x-speed value
modelCoordinateSet.get(3).setSpeedValue(si, 0.1)

# set y-translation value
modelCoordinateSet.get(4).setValue(si, blockSideLength/2+0.01)

# Create the integrator and manager for the simulation.
#integrator = RungeKuttaMersonIntegrator(osimModel.getMultibodySystem()) # TODO Can't create an integrator
#integrator.setAccuracy(1.0e-4)
#manager = Manager(osimModel, integrator)
manager = Manager(osimModel) # Manager without specifying the integrator


### TODO Modification test of an Analysis class (doesn't work so far)
class MyForceReporter(ForceReporter):
    def step(self, *args):
        print "test message"
        return _opensim.ForceReporter_step(self, *args)
reporter = MyForceReporter(osimModel)
osimModel.addAnalysis(reporter)

######################################################################

# (From Part 3)
reporter = ForceReporter(osimModel)
osimModel.addAnalysis(reporter)

# Define the initial and final simulation times
initialTime = 0.0
finalTime = 4.0
# Integrate from initial time to final time
manager.setInitialTime(initialTime)
manager.setFinalTime(finalTime)
print "\n\nIntegrating from",initialTime,"to",finalTime
manager.integrate(si)

# Save the simulation results
statesDegrees = Storage(manager.getStateStorage())
statesDegrees.printToFile("tugOfWar_states.sto")
osimModel.updSimbodyEngine().convertRadiansToDegrees(statesDegrees)
statesDegrees.setWriteSIMMHeader(True)
statesDegrees.printToFile("tugOfWar_states_degrees.mot")

# Save the model to a file
osimModel.printToXML("tugOfWar_model.osim")
