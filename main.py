import asyncio
import math
import sys
import traceback

from js import THREE, Float32Array, Object
from pyodide.ffi import create_proxy, to_js
from pyscript import document, window

canvas = document.querySelector("#c")
renderer = THREE.WebGLRenderer.new(
    Object.fromEntries(to_js({"antialias": True, "canvas": canvas}))
)

container = document.querySelector("#three-container")

camera = THREE.PerspectiveCamera.new(
    75, window.innerWidth / window.innerHeight, 0.01, 10
)
camera.position.set(0, 0, 2)

scene = THREE.Scene.new()

orbit = THREE.OrbitControls.new(camera, renderer.domElement)
orbit.enableZoom = False

geometry = THREE.IcosahedronGeometry.new(1, 1)
perms = {
    "color": "#FFFFFF",
    "vertexColors": True,
}
perms = Object.fromEntries(to_js(perms))
material = THREE.MeshStandardMaterial.new(perms)
cube = THREE.Mesh.new(geometry, material)
scene.add(cube)
count = geometry.attributes.position.count

geometry.setAttribute(
    "color", THREE.BufferAttribute.new(Float32Array.new(count * 3), 3)
)


def set_colors(colors: list[list[int]]):
    color = THREE.Color.new()
    colors1 = geometry.attributes.color
    face_count = int(count / 3)
    for i in range(face_count):
        color.setRGB(colors[i][0], colors[i][1], colors[i][2])
        colors1.setXYZ(i * 3 + 0, color.r, color.g, color.b)
        colors1.setXYZ(i * 3 + 1, color.r, color.g, color.b)
        colors1.setXYZ(i * 3 + 2, color.r, color.g, color.b)
    colors1.needsUpdate = True


ambientLight = THREE.AmbientLight.new()
scene.add(ambientLight)


def resizeRendererToDisplaySize(renderer):
    canvas = renderer.domElement
    pixelRatio = window.devicePixelRatio
    width = math.floor(canvas.clientWidth * pixelRatio)
    height = math.floor(canvas.clientHeight * pixelRatio)
    needResize = canvas.width != width or canvas.height != height
    if needResize:
        renderer.setSize(width, height, False)

    return needResize


code_is_running = False


def render(*args):
    global code_is_running

    if code_is_running:
        cube.rotation.y += 0.003

    if resizeRendererToDisplaySize(renderer):
        canvas = renderer.domElement
        camera.aspect = canvas.clientWidth / canvas.clientHeight
        camera.updateProjectionMatrix()

    renderer.render(scene, camera)
    window.requestAnimationFrame(create_proxy(render))


render()

stop_event = asyncio.Event()


def stop_code(event):
    stop_event.set()


async def run_code(event):
    global code_is_running
    document.querySelector("#runButton").style.display = "none"
    document.querySelector("#stopButton").style.display = "inline-block"

    code_string = window.editor.getValue()
    printouts = document.querySelector("#printouts")
    # printouts.textContent = ""
    printouts_container = document.querySelector("#printouts-container")

    FUNC_NAME = "update_pixels"

    # Define a custom stream that captures the output
    class CapturePrintouts:
        def write(self, text):
            printouts.textContent += text
            # auto-scroll to the bottom
            printouts_container.scrollTop = printouts_container.scrollHeight

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
        code_is_running = True
        while not stop_event.is_set():
            set_colors(update_pixels_func(i))
            # renderer.render(scene, camera)
            await asyncio.sleep(0.5)
            i += 1
        print("--- STOP EXECUTION ---")

    except:
        print(traceback.format_exc())

    code_is_running = False

    # Restore the original stdout
    sys.stdout = sys.__stdout__

    stop_event.clear()
    document.querySelector("#runButton").style.display = "inline-block"
    document.querySelector("#stopButton").style.display = "none"
