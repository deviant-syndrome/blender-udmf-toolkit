import bpy
import bmesh


class MeshObjectLifecycle:
    def __init__(self, object_name):
        self.object_name = object_name
        self.mesh_name = object_name + "_Mesh"
        self.mesh = None
        self.bm = None
        self.obj = None
        self.scale = bpy.context.scene.map_scale

    def __enter__(self):
        # Ensure we're in OBJECT mode
        if bpy.context.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")

        # Delete any existing mesh with the given name
        if self.mesh_name in bpy.data.meshes:
            bpy.data.meshes.remove(bpy.data.meshes[self.mesh_name])

        self.mesh = bpy.data.meshes.new(name=self.mesh_name)
        self.bm = bmesh.new()
        return self.bm, self.mesh

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.bm:
            bmesh.ops.scale(
                self.bm, vec=(self.scale, self.scale, self.scale), verts=self.bm.verts
            )
            self.bm.to_mesh(self.mesh)
            self.bm.free()

        if exc_type is None:
            if self.mesh:
                self.mesh.update()
                self.mesh.validate()
            self.obj = bpy.data.objects.new(self.object_name, self.mesh)
            bpy.context.collection.objects.link(self.obj)
            bpy.context.view_layer.objects.active = self.obj
            self.obj.select_set(True)

            # Cleanup
            bpy.context.view_layer.objects.active = self.obj
            bpy.ops.object.mode_set(mode="OBJECT")

        if exc_type is not None:
            # Optionally, if you want to handle/log the exception
            print(f"Exception occurred: {exc_val}")
