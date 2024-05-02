from array import array

import moderngl

SHADER_PATH = "data/shaders/"
SHADER_EXTENSION = ".glsl"


class Renderer:
    def __init__(self, display):
        self.display = display

        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # Position (X, Y),  uv cords (x, y)
            -1.0, 1.0, 0.0, 0.0,   # Top Left
            1.0, 1.0, 1.0, 0.0,    # Top Right
            -1.0, -1.0, 0.0, 1.0,  # Bottom Left
            1.0, -1.0, 1.0, 1.0,   # Bottom Right
        ]))

        self.shaders = {

        }
        self.load_all_shaders()

        self.program = self.ctx.program(vertex_shader=self.shaders["default"]["vertex"],
                                        fragment_shader=self.shaders["default"]["fragment"])
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def change_shader(self, new_shader):
        self.program = self.ctx.program(vertex_shader=self.shaders[new_shader]["vertex"],
                                        fragment_shader=self.shaders[new_shader]["fragment"])
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = "BGRA"
        tex.write(surf.get_view('1'))
        return tex

    def load_all_shaders(self):
        for shader in ["default", "red_tint"]:
            self.load_shader(shader, shader)

    def load_shader(self, shader_slot, shader):
        loaded_shader = {"fragment": None, "vertex": None}
        with open(f"{SHADER_PATH}{shader}{SHADER_EXTENSION}", "r") as file:
            shader_type = None
            shader_code = {"vertex": "", "fragment": ""}
            for line in file:
                if line.strip().startswith("//type"):
                    shader_type = line.strip().split()[1]
                else:
                    shader_code[shader_type] += line

        loaded_shader["vertex"] = shader_code["vertex"]
        loaded_shader["fragment"] = shader_code["fragment"]

        self.shaders[shader_slot] = loaded_shader
