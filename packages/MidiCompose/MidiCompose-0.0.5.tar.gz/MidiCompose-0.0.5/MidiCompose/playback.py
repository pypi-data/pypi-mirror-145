import mido
from mido import MidiFile

def play_mid(mid: MidiFile, port_name: str = "loopMIDI Port 1") -> None:
    port = None
    try:
        port = mido.open_output(port_name)
        for msg in mid.play():
            port.send(msg)
    except:
        e = f"Failed to open output port `{port_name}`\n" \
            f"Available ports: {mido.get_output_names()}"
        raise Exception(e)
    finally:
        if port:
            port.close()

if __name__ == '__main__':
    print(mido.get_output_names())