import os
print("PYTHONPATH:", os.environ.get("PYTHONPATH"))
print("PXR_PLUGINPATH_NAME:", os.environ.get("PXR_PLUGINPATH_NAME"))
print("DYLD_LIBRARY_PATH:", os.environ.get("DYLD_LIBRARY_PATH"))
from pxr import Usd, UsdGeom, Gf, Vt
import random

def CreateStage(file_path):
    # Initializes the stage and sets base metadata
    if os.path.exists(file_path):
        os.remove(file_path)

    stage = Usd.Stage.CreateNew(file_path)
    
    # define default root prim
    root_prim = UsdGeom.Xform.Define(stage, '/Root')
    stage.SetDefaultPrim(root_prim.GetPrim())
    
    # Sst stage metadata
    # set up axis to +z
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
    # setting start and end time codes
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(192)
    stage.SetMetadata('comment', 'Start and end time codes initialized')
    
    return stage

def CreateGround(stage, prim_path):
    # creates a ground plane (will be used to detect sphere hits)
    ground=UsdGeom.Plane.Define(stage, prim_path)
    # we need to author this manually in order to use bbox_cache later
    ground.CreateExtentAttr([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])

    xform=UsdGeom.Xformable(ground)
    xform.ClearXformOpOrder()
    translate_op=xform.AddTranslateOp()
    translate_op.Set(Gf.Vec3d(0,0,0))
    ground.GetPrim().SetMetadata('comment', 'created ground plane')

# we give this prim node a path where it lives
def CreateSphere(stage, prim_path):
    # Creates a sphere prim on the provided stage
    sphere = UsdGeom.Sphere.Define(stage, prim_path)
    # we need to author this manually in order to use bbox_cache later
    sphere.CreateExtentAttr([Gf.Vec3f(-1, -1, -1), Gf.Vec3f(1, 1, 1)])
    xform=UsdGeom.Xformable(sphere)
    scale_op=xform.AddScaleOp()
    scale_op.Set(Gf.Vec3d(0.5,0.5,0.5))
    sphere.GetPrim().SetMetadata('comment', 'created sphere geom')
    
    return sphere

def AnimateSphere(sphere_prim):
    # animating the sphere
    # transformation for sphere
    xform = UsdGeom.Xformable(sphere_prim)
    # clearing any previous transformations
    # xform.ClearXformOpOrder()
    # adding a transformation operation
    translate_op = xform.AddTranslateOp()
    
    # interval set to 8 seconds
    start_frame=1
    end_frame=192
    # speed to implement a time step (increase for slower movement)
    speed=8
    # by default uses linear interpolation
    for frame in range (start_frame, end_frame):
        x=random.uniform(-1.0,1.0)
        y=random.uniform(-1.0,1.0)
        # to make sure we have hits
        z=random.uniform(2.5,10.0)
        time_code=Usd.TimeCode(frame)
        # author opinions at specific timecodes
        # Gf.Vec3d is used to pass precise 3D vector coordinates (x,y,z)
        translate_op.Set(Gf.Vec3d(x,y,z),time_code)
        
    sphere_prim.GetPrim().SetMetadata('comment', 'animated sphere')

def main():
    # 1. Initialize the dataset in memory
    file_name = 'stage1.usda'
    stage = CreateStage(file_name)

    # 2. pass the memory object (stage usda) through created functions
    # we need to create the ground too
    ground = CreateGround(stage, '/Root/ground')
    sphere = CreateSphere(stage, '/Root/sphere')
    AnimateSphere(sphere)
    
    # commit the final scenegraph to memory
    stage.GetRootLayer().Save()
    print(f"Successfully generated {file_name}")

if __name__ == '__main__':
    main()
