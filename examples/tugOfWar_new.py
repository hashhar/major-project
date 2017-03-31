import opensim as osim

m = osim.Model()
m.setUseVisualizer(True)

anchor1 = osim.Body("anchor1",
    1.0,
    osim.Vec3(0, 0, 0),
    osim.Inertia(0, 0, 0))

anchor2 = osim.Body("anchor2",
    1.0,
    osim.Vec3(0, 0, 0),
    osim.Inertia(0, 0, 0))

block = osim.Body("block",
    1.0,
    osim.Vec3(0, 0, 0),
    osim.Inertia(0, 0, 0))

groundJoint1 = osim.PinJoint("anchor1toGround",
    m.getGround(),
    osim.Vec3(0),
    osim.Vec3(0),
    anchor1,
    osim.Vec3(-2, 0, 0),
    osim.Vec3(0))

groundJoint2 = osim.PinJoint("anchor2toGround",
    m.getGround(),
    osim.Vec3(0),
    osim.Vec3(0),
    anchor2,
    osim.Vec3(4, 0, 0),
    osim.Vec3(0))

blockToGround = osim.PinJoint("blockToGround",
    m.getGround(),
    osim.Vec3(0),
    osim.Vec3(0),
    block,
    osim.Vec3(1, 0, 0),
    osim.Vec3(0))

# blockToAnchor1 = osim.PinJoint("blockToAnchor1",
    # block,
    # osim.Vec3(0),
    # osim.Vec3(0),
    # anchor1,
    # osim.Vec3(0),
    # osim.Vec3(0))

# blockToAnchor2 = osim.PinJoint("blockToAnchor2",
    # block,
    # osim.Vec3(0),
    # osim.Vec3(0),
    # anchor2,
    # osim.Vec3(0),
    # osim.Vec3(0))

blockToAnchor1 = osim.Millard2012EquilibriumMuscle("blockToAnchor1",
    10.0,
    6.1,
    6.0,
    0)

# blockToAnchor2 = osim.Millard2012EquilibriumMuscle("blockToAnchor2",
    # 300.0,
    # 1.6,
    # 2.55,
    # 0)

blockToAnchor1.addNewPathPoint("anchor1",
    anchor1,
    osim.Vec3(-2, 0, 0))
blockToAnchor1.addNewPathPoint("blockanchor1",
    anchor2,
    osim.Vec3(4, 0, 0))

# blockToAnchor2.addNewPathPoint("anchor2",
    # anchor2,
    # osim.Vec3(3, 0.5, 0))
# blockToAnchor2.addNewPathPoint("blockanchor2",
    # block,
    # osim.Vec3(1, 0.5, 0))

brain = osim.PrescribedController()
brain.addActuator(blockToAnchor1)
# brain.addActuator(blockToAnchor2)
brain.prescribeControlForActuator("blockToAnchor1",
    osim.StepFunction(0.5, 3.0, 0.3, 1.0))
# brain.prescribeControlForActuator("blockToAnchor2",
    # osim.StepFunction(0.5, 3.0, 0.3, 1.0))

m.addBody(anchor1)
m.addBody(anchor2)
m.addBody(block)
m.addJoint(groundJoint1)
m.addJoint(groundJoint2)
m.addJoint(blockToGround)
m.addForce(blockToAnchor1)
# m.addForce(blockToAnchor2)
m.addController(brain)
# m.addJoint(blockToAnchor1)
# m.addJoint(blockToAnchor2)

anchorGeometry = osim.Brick()
anchorGeometry.setColor(osim.Gray)

anchor1Center = osim.PhysicalOffsetFrame()
anchor1Center.setName("anchor1Center")
anchor1Center.setParentFrame(anchor1)
anchor1Center.setOffsetTransform(osim.Transform(osim.Vec3(0, 0.5, 0)))
anchor1.addComponent(anchor1Center)
anchor1Center.attachGeometry(anchorGeometry.clone())

anchor2Center = osim.PhysicalOffsetFrame()
anchor2Center.setName("anchor2Center")
anchor2Center.setParentFrame(anchor2)
anchor2Center.setOffsetTransform(osim.Transform(osim.Vec3(0, 0.5, 0)))
anchor2.addComponent(anchor2Center)
anchor2Center.attachGeometry(anchorGeometry.clone())

blockGeometry = osim.Sphere(0.2)
blockGeometry.setColor(osim.Gray)

blockCenter = osim.PhysicalOffsetFrame()
blockCenter.setName("blockCenter")
blockCenter.setParentFrame(block)
blockCenter.setOffsetTransform(osim.Transform(osim.Vec3(0, 0.5, 0)))
block.addComponent(blockCenter)
blockCenter.attachGeometry(blockGeometry.clone())

state = m.initSystem()
groundJoint1.getCoordinate().setLocked(state, True)
groundJoint2.getCoordinate().setLocked(state, True)
# blockToAnchor1.getCoordinate().setLocked(state, False)
# blockToAnchor2.getCoordinate().setLocked(state, True)
blockToGround.getCoordinate().setLocked(state, False)

manager = osim.Manager(m)
manager.setInitialTime(0)
manager.setFinalTime(5)
manager.integrate(state)

m.printToXML("block.osim")
