# here we take the strings from our engine and pass them to hython so that it can give houdini the hit frame and coordinates
# argparse is the library used to parse strings (ie, understand string as data/commands)

import sys, argparse, os
from pxr import Usd, Sdf
print(Sdf.FileFormat.FindById('usdnc'))
print('usd version: ', Usd.GetVersion())

try:
    import hou 
    print('imported hou')
except ImportError:
    print('make sure to  you are using HYTHON and NOT standard PYTHON interpreter.')
    sys.exit(1) # we tell the subprocess to shut down immediately

def DustSimulationBuildAndExport(export_file_path):
    print('starting building simple test sim')
    
    start_frame = 1 
    life = 45 
    end_frame = start_frame + life
    hou.playbar.setFrameRange(start_frame, end_frame) 

    obj_context = hou.node('/obj')
    dust_node = obj_context.createNode('geo', 'dust_sim_gen')
    # dust_node.clearChildren()
    
    # test_sphere = dust_node.createNode('sphere', 'test_mesh')
    # test_sphere.parm('type').set(1) # Convert to polygon
    
    # test_sphere.parm('scale').setExpression(f'max(0, ($F - {start_frame}) * 0.15)')

    # output_null = dust_node.createNode('null', 'OUT_particles')
    # output_null.setInput(0, test_sphere) 

    emitter_source = dust_node.createNode('sphere', 'emitter_source')
    emitter_source.parm('scale').set(0.1)
    
    # B. Scatter 500 points (our dust particles) onto the emitter
    scatter = dust_node.createNode('scatter', 'emit_points')
    scatter.setInput(0, emitter_source)
    scatter.parm('npts').set(500) 
    
    # C. Apply VEX Math to simulate explosion, drag, and gravity 
    # (Notice the double {{ }} to prevent Python f-string errors!)
    wrangle = dust_node.createNode('attribwrangle', 'particle_kinematics')
    wrangle.setInput(0, scatter)
    vex_code = f"""
    float age = (@Frame - {start_frame}) / 24.0; // Age in seconds
    
    if (age > 0) {{
        // 1. Generate a random outward direction with an upward bias
        vector dir = normalize(set(rand(@ptnum)-0.5, rand(@ptnum+10)*0.8, rand(@ptnum+20)-0.5));
        
        // 2. Randomize speed per particle
        float speed = rand(@ptnum+30) * 8.0 + 2.0; 
        
        // 3. Air Resistance (Drag): Particles explode fast but slow down quickly in the air
        float drag = 4.0; 
        float damped_age = (1.0 - exp(-drag * age)) / drag; 
        
        // Apply velocity over time
        @P += dir * speed * damped_age;
        
        // 4. Light gravity gently pulling them back down
        @P.y -= 0.5 * 1.5 * age * age;
        
        // 5. Floor collision (stops them from falling through the ground)
        if (@P.y < 0.02) @P.y = 0.02;
        
        // 6. Scale them down over time so they shrink into nothing
        @pscale = max(0.0, 0.04 * (1.0 - (age / 1.5)));
    }} else {{
        // Hide particles before the impact frame
        @pscale = 0.0;
    }}
    """
    wrangle.parm('snippet').set(vex_code)
    
    # D. Create actual geometry for the particles to render properly in USD
    particle_mesh = dust_node.createNode('sphere', 'particle_mesh')
    particle_mesh.parm('type').set(1) # Polygon
    particle_mesh.parm('scale').set(1.0) # VEX @pscale will control the final size!
    
    # E. Copy the geometry onto our moving points
    copy_pts = dust_node.createNode('copytopoints', 'copy_to_particles')
    copy_pts.setInput(0, particle_mesh)
    copy_pts.setInput(1, wrangle)

    output_null = dust_node.createNode('null', 'OUT_particles')
    output_null.setInput(0, copy_pts)

    # 5. Export via Solaris/USD
    stage_context = hou.node('/stage') 

    # CREATE LOPNET FIRST!!!
    lop_net=stage_context.createNode('subnet', 'dust_export_net')
    # lop_net.clearChildren()

    # 2. Connect the geometry import underneath it
    sop_import = lop_net.createNode('sopimport', 'import_dust')
    sop_import.parm('soppath').set(output_null.path())
    # sop_import.parm('primpath').set('/dust_asset/mesh') # Local path structure
    sop_import.parm('pathprefix').set('/dust_asset')
    # sop_import.parm('enable_setdefaultprim').set(1)
    # sop_import.parm('setdefaultprim').set(1)
    config_layer = lop_net.createNode('configurelayer', 'set_metadata')
    config_layer.setInput(0, sop_import)
    
    # Toggle the default prim switch to TRUE (1)
    config_layer.parm('setdefaultprim').set(1)
    # Provide the exact matching text path string to the root primitive
    config_layer.parm('defaultprim').set('/dust_asset')

    usd_rop_node = lop_net.createNode('usd_rop', 'export_usd')
    usd_rop_node.setInput(0, config_layer)
    usd_rop_node.parm('lopoutput').set(export_file_path)
    
    # Configure the frame range
    usd_rop_node.parm('trange').set(1) 
    usd_rop_node.parm('f1').set(start_frame) 
    usd_rop_node.parm('f2').set(end_frame)

    usd_rop_node.parm('savestyle').set('flattenstage')

    print('starting simulation baking')
    usd_rop_node.render()
    print('bake complete 🤯')

# to execute the above script
def main():
    parser=argparse.ArgumentParser(description='houdini worker')
    parser.add_argument('--frame', type=int, required=True, help='hit_frame_number')
    parser.add_argument('--x', type=float, required=True, help='x coord of contact point')
    parser.add_argument('--y', type=float, required=True, help='y coord of contact point')
    parser.add_argument('--z', type=float, required=True, help='z coord of contact point')

    args=parser.parse_args() # store the data in the args variable

    print(f'houdini worker received data {args.frame}, ({args.x}, {args.y}, {args.z})')

    export_file_path = '/Users/shreyapahuja/USD_Projects/dust_sim.usdnc'
    DustSimulationBuildAndExport(export_file_path)

    print('sim exported. houdini worker shutting down')

    sys.exit(0) # make sure to shut down the worker so that it doesn't use memory after it has finished its job

if __name__=='__main__':
    main()



