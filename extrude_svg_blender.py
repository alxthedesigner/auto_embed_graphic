import bpy
import os
import mathutils
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# accessing and printing value
stashbox_path = os.getenv("STASHBOX_PATH")
stashbox_XL_path = os.getenv("STASHBOX_XL_PATH")
hexagon_container_path = os.getenv("HEXAGON_CONTAINER_PATH")
three_d_sticker_path = os.getenv("3D_STICKER_PATH")


def delete_all_in_scene():
    # Ensure we are in Object Mode
    #if bpy.context.object.mode != 'OBJECT':
        #bpy.ops.object.mode_set(mode='OBJECT')

    # Select all objects in the scene
    bpy.ops.object.select_all(action='SELECT')

    # Delete all selected objects
    bpy.ops.object.delete()


def import_svg(filepath):
    # Ensure we are in Object Mode
    #if bpy.context.object.mode != 'OBJECT':
        #bpy.ops.object.mode_set(mode='OBJECT')
    
    # Import the SVG file
    bpy.ops.import_curve.svg(filepath=filepath)


def convert_curves_to_mesh():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Iterate over all objects in the scene
    for obj in bpy.context.scene.objects:
        # Check if the object is a curve
        if obj.type == 'CURVE':
            # Select the curve object
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            # Convert the curve to mesh
            bpy.ops.object.convert(target='MESH')
        else:
            obj.select_set(False)
    

def extrude_and_move():
     #Move object up
    bpy.ops.transform.translate(value=(-0.0194, 0.0, 0.005))

    # Switch to Edit Mode to select all geometry
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices, edges, and faces
    bpy.ops.mesh.select_all(action='SELECT')

    # Extrude the selection along the Z-axis by 5mm (0.005 units in Blender)
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0.0049)})

    # Select all vertices, edges, and faces
    bpy.ops.mesh.select_all(action='SELECT')

    # Remove doubles (merge by distance)
    bpy.ops.mesh.remove_doubles()


def export_stl(output_filepath):
    # Switch to Object Mode to export the final mesh
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Select all objects (just in case)
    bpy.ops.object.select_all(action='SELECT')

    # Export the selected objects as an STL file
    bpy.ops.export_mesh.stl(filepath=output_filepath)

def process_svg(filepath):

    delete_all_in_scene()

    # Import SVG file (selects all)
    import_svg(filepath)
    
    # Convert all imported curves to meshes
    convert_curves_to_mesh()
    
    # Select and extrude all geometry
    extrude_and_move()
    
    # Export the final mesh as an STL file
    export_stl("gpt_extrusion.stl")


# Example usage
svg_filepath = "./too_t3rpd_logo_1.svg"  # Replace with your SVG file path
process_svg(svg_filepath)
