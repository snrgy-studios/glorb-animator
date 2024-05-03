import asyncio
import sys
import traceback

from js import THREE, Float32Array, Math, Object, performance
from pyodide.ffi import to_js
from pyscript import document, window

renderer = THREE.WebGLRenderer.new({"antialias": True})
renderer.setSize(1000, 1000)
renderer.shadowMap.enabled = False
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.shadowMap.needsUpdate = True
renderer.setPixelRatio(window.devicePixelRatio)

document.body.appendChild(renderer.domElement)

camera = THREE.PerspectiveCamera.new(35, window.innerWidth / window.innerHeight, 1, 500)
scene = THREE.Scene.new()
cameraRange = 3

camera.aspect = window.innerWidth / window.innerHeight
camera.updateProjectionMatrix()
renderer.setSize(window.innerWidth, window.innerHeight)

orbit = THREE.OrbitControls.new(camera, renderer.domElement)
orbit.enableZoom = False


setcolor = "#111111"

scene.background = THREE.Color.new(setcolor)
scene.fog = THREE.Fog.new(setcolor, 2.5, 3.5)

modularGroup = THREE.Object3D.new()

perms = {
    "flatShading": True,
    "color": "#111111",
    "transparent": False,
    "opacity": 1,
    "wireframe": False,
    "vertexColors": True,
}
perms = Object.fromEntries(to_js(perms))


def create_cubes(modularGroup):
    geometry = THREE.IcosahedronGeometry.new(0.5, 1)
    material = THREE.MeshStandardMaterial.new(perms)
    cube = THREE.Mesh.new(geometry, material)
    cube.speedRotation = Math.random() * 0.1
    cube.positionX = 0
    cube.positionY = 0
    cube.positionZ = 0
    cube.castShadow = True
    cube.receiveShadow = True
    cube.scale.set(1, 1, 1)
    cube.position.set(cube.positionX, cube.positionY, cube.positionZ)
    modularGroup.add(cube)
    count = geometry.attributes.position.count

    geometry.setAttribute(
        "color", THREE.BufferAttribute.new(Float32Array.new(count * 3), 3)
    )

    def set_colors_local(colors: list[list[int]]):
        color = THREE.Color.new()
        colors1 = geometry.attributes.color
        count = geometry.attributes.position.count
        for i in range(int(count / 3)):
            color.setRGB(colors[i][0], colors[i][1], colors[i][2])
            colors1.setXYZ(i * 3 + 0, color.r, color.g, color.b)
            colors1.setXYZ(i * 3 + 1, color.r, color.g, color.b)
            colors1.setXYZ(i * 3 + 2, color.r, color.g, color.b)
        colors1.needsUpdate = True

    return set_colors_local


set_colors = create_cubes(modularGroup)


scene.add(modularGroup)

camera.position.set(0, 0, cameraRange)
cameraValue = False

ambientLight = THREE.AmbientLight.new(0xFFFFFF, 0.1)

light = THREE.SpotLight.new(0xFFFFFF, 3)
light.position.set(5, 5, 2)
light.castShadow = True
light.shadow.mapSize.width = 10000
light.shadow.mapSize.height = light.shadow.mapSize.width
light.penumbra = 0.5

lightBack = THREE.PointLight.new(0x0FFFFF, 1)
lightBack.position.set(0, -3, -1)

scene.add(light)


light2 = THREE.DirectionalLight.new(0xFFFFFF, 1)
light2.position.set(-1, 2, 4)
scene.add(light2)

scene.add(lightBack)

light_ambient = THREE.AmbientLight.new(0x404040)  # soft white light
scene.add(light_ambient)

rectSize = 2
intensity = 14
rectLight = THREE.RectAreaLight.new(0x0FFFFF, intensity, rectSize, rectSize)
rectLight.position.set(0, 0, 1)
rectLight.lookAt(0, 0, 0)
scene.add(rectLight)

raycaster = THREE.Raycaster.new()

time = 0.0003
camera.lookAt(scene.position)


async def render_always():
    while True:
        cube = modularGroup.children[0]
        cube.rotation.y += 0.003
        renderer.render(scene, camera)
        await asyncio.sleep(0.02)


asyncio.ensure_future(render_always())

stop_event = asyncio.Event()


def stop_code(event):
    stop_event.set()


async def run_code(event):
    document.querySelector("#runButton").style.display = "none"
    document.querySelector("#stopButton").style.display = "inline-block"

    code_string = window.editor.getValue()
    printouts = document.querySelector("#printouts")
    # printouts.textContent = ""
    output_container = document.querySelector("#output-container")

    FUNC_NAME = "update_pixels"

    # Define a custom stream that captures the output
    class CapturePrintouts:
        def write(self, text):
            printouts.textContent += text
            # auto-scroll to the bottom
            output_container.scrollTop = output_container.scrollHeight

    # Redirect stdout to the custom stream
    sys.stdout = CapturePrintouts()
    try:
        # Create a separate namespace for the executed code
        namespace = {}
        # Execute the user-provided code
        print("--- START EXECUTION ---")
        exec(code_string, namespace)

        # Check if the 'update_pixels' function is defined in the user-provided code
        if FUNC_NAME not in namespace:
            print(f"Error:\n '{FUNC_NAME}' function not found in the provided code.")
            return

        # Get a reference to the 'update' function
        update_pixels_func = namespace[FUNC_NAME]

        # Call the 'update' function repeatedly
        i = 0
        while not stop_event.is_set():
            set_colors(update_pixels_func(i))
            # renderer.render(scene, camera)
            await asyncio.sleep(0.5)
            i += 1
        print("--- STOP EXECUTION ---")

    except:
        print(traceback.format_exc())

    # Restore the original stdout
    sys.stdout = sys.__stdout__

    stop_event.clear()
    document.querySelector("#runButton").style.display = "inline-block"
    document.querySelector("#stopButton").style.display = "none"
