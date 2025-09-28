from aiohttp import web
from synth_numpy import AudioSynthesizer
import atexit
from aiohttp_swagger import setup_swagger  # <-- add this import


NOTE_STATES = [False for n in range(0, 128)]
STATE_QUEUE = []

# Initialize audio synthesizer (set to 50% volume as requested)
synth = AudioSynthesizer(volume=0.5)


def _reset_notes():
    global NOTE_STATES
    NOTE_STATES = [False for n in range(0, 128)]
    synth.reset_notes()  # Stop all audio


async def hello(request):
    """---
    description: Simple hello endpoint
    tags:
    - misc
    """
    return web.Response(text="Hello, world!")


async def get_note(request):
    """---
    description: Get note state (True/False)
    tags:
    - notes
    parameters:
    - name: note_number
      in: path
      required: true
      type: integer
    """
    global NOTE_STATES
    note_number = request.match_info.get("note_number")
    note_number = int(note_number)
    return web.json_response(NOTE_STATES[note_number])


async def put_note(request):
    """---
    description: Play a note (set state True)
    tags:
    - notes
    parameters:
    - name: note_number
      in: path
      required: true
      type: integer
    """
    global NOTE_STATES
    note_number = request.match_info.get("note_number")
    note_number = int(note_number)
    NOTE_STATES[note_number] = True

    # Start playing the note
    synth.add_note(note_number)

    return web.json_response(NOTE_STATES[note_number])


async def delete_note(request):
    """---
    description: Stop a note (set state False)
    tags:
    - notes
    parameters:
    - name: note_number
      in: path
      required: true
      type: integer
    """
    global NOTE_STATES
    note_number = request.match_info.get("note_number")
    note_number = int(note_number)
    NOTE_STATES[note_number] = False

    # Stop playing the note
    synth.remove_note(note_number)

    return web.json_response(NOTE_STATES[note_number])


async def reset_all_notes(request):
    """---
    description: Stop all notes
    tags:
    - notes
    """
    global NOTE_STATES
    _reset_notes()
    return web.json_response(NOTE_STATES)


async def get_all_notes(request):
    """---
    description: Get all note states
    tags:
    - notes
    """
    global NOTE_STATES
    return web.json_response(NOTE_STATES)


async def index(request):
    return web.FileResponse("index.html")


app = web.Application()
app.router.add_get("/", index)

app.router.add_get("/note/{note_number}", get_note)
app.router.add_put("/note/{note_number}", put_note)
app.router.add_delete("/note/{note_number}", delete_note)
app.router.add_post("/notes/reset", reset_all_notes)
app.router.add_get("/notes", get_all_notes)

# Add Swagger docs endpoint
setup_swagger(
    app, swagger_url="/docs", ui_version=3, title="Notes as a Service (NoAAS)"
)


if __name__ == "__main__":
    # Start the audio synthesizer
    synth.start()

    # Ensure proper cleanup on exit
    atexit.register(synth.stop)

    web.run_app(app, port=8080)
