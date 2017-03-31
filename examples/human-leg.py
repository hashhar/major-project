import opensim as osim

# Define global model where the leg lives.
leg = osim.Model()
leg.setUseVisualizer(True)

# Create two links, each with a mass of 1 kg, centre of mass at the body's
# origin, and moments and products of inertia of zero.
upper = osim.Body("upper",
                  1.0,
                  osim.Vec3(0, 0, 0),
                  osim.Inertia(0, 0, 0))
lower = osim.Body("lower",
                  1.0,
                  osim.Vec3(0, 0, 0),
                  osim.Inertia(0, 0, 0))

# Connect the bodies with pin joints. Assume each body is 1m long.
hip = osim.PinJoint("hip",
                    leg.getGround(), # PhysicalFrame
                    osim.Vec3(0, 0, 0),
                    osim.Vec3(0, 0, 0),
                    upper, # PhysicalFrame
                    osim.Vec3(0, 1, 0),
                    osim.Vec3(0, 0, 0))

knee = osim.PinJoint("knee",
                     upper, # PhysicalFrame
                     osim.Vec3(0, 0, 0),
                     osim.Vec3(0, 0, 0),
                     lower, # PhysicalFrame
                     osim.Vec3(0, 1, 0),
                     osim.Vec3(0, 0, 0))

# Add a muscle that flexes the knee (actuator for robotics people).
calf = osim.Millard2012EquilibriumMuscle("calf",  # Muscle name
                                         200.0,  # Max isometric force
                                         0.6,  # Optimal fibre length
                                         0.55,  # Tendon slack length
                                         0.0)  # Pennation angle
calf.addNewPathPoint("origin",
                     upper,
                     osim.Vec3(0, 0.8, 0))

calf.addNewPathPoint("insertion",
                     lower,
                     osim.Vec3(0, 0.7, 0))

# Add a controller that specifies the excitation of the muscle.
brain = osim.PrescribedController()
brain.addActuator(calf)
brain.prescribeControlForActuator("calf",
                                  osim.StepFunction(0.5, 3.0, 0.3, 1.0))

# Build model with components created above.
leg.addBody(upper)
leg.addBody(lower)
leg.addJoint(hip)
leg.addJoint(knee)
leg.addForce(calf)
leg.addController(brain)

# Add a console reporter to print the muscle fibre force and knee angle.
reporter = osim.ConsoleReporter()
reporter.set_report_time_interval(1.0)
reporter.addToReport(calf.getOutput("fiber_force"))
knee_coord = knee.getCoordinate().getOutput("value")
reporter.addToReport(knee_coord, "knee_angle")
leg.addComponent(reporter)

# Add display geometry.
bodyGeometry = osim.Ellipsoid(0.1, 0.5, 0.1)
bodyGeometry.setColor(osim.Gray)
upperCenter = osim.PhysicalOffsetFrame()
upperCenter.setName("upperCenter")
upperCenter.setParentFrame(upper)
upperCenter.setOffsetTransform(osim.Transform(osim.Vec3(0, 0.5, 0)))
upper.addComponent(upperCenter)
upperCenter.attachGeometry(bodyGeometry.clone())

lowerCenter = osim.PhysicalOffsetFrame()
lowerCenter.setName("lowerCenter")
lowerCenter.setParentFrame(lower)
lowerCenter.setOffsetTransform(osim.Transform(osim.Vec3(0, 0.5, 0)))
lower.addComponent(lowerCenter)
lowerCenter.attachGeometry(bodyGeometry.clone())

# Configure the model.
state = leg.initSystem()
# Fix the hip at its default angle and begin with the knee flexed.
hip.getCoordinate().setLocked(state, True)
knee.getCoordinate().setValue(state, 0.5 * osim.SimTK_PI)
leg.equilibrateMuscles(state)

# Simulate.
manager = osim.Manager(leg)
manager.setInitialTime(0)
manager.setFinalTime(10.0)
manager.integrate(state)

# Print/save model file
leg.printToXML("Simpleleg.osim")

