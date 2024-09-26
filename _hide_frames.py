"""Modify .viser files to hide coordinate frames."""

# Reference:
#
# def serialize(
# """End the recording and serialize contents. Returns the recording as
#     bytes, which should generally be written to a file."""
#     packed_bytes = msgspec.msgpack.encode(
#         {
#             "loopStartIndex": loop_start_index,
#             "durationSeconds": time,
#             "messages": messages,
#         }
#     )
#     assert isinstance(packed_bytes, bytes)
#     return gzip.compress(packed_bytes, compresslevel=9)

import gzip
from pathlib import Path

import msgspec.msgpack
import tyro


def hide_frames(path: Path) -> dict:
    with gzip.open(path, "rb") as f:
        data = msgspec.msgpack.decode(f.read())

    for timestamp, message in data["messages"]:
        if message["type"] == "FrameMessage":
            assert "show_axes" in message
            message["show_axes"] = False

    # Write back.
    packed_bytes = msgspec.msgpack.encode(data)
    compressed_data = gzip.compress(packed_bytes, compresslevel=9)

    with open(path, "wb") as f:
        f.write(compressed_data)

    return data


def main(path_root: Path) -> None:
    for viser_file in path_root.glob("*.viser"):
        hide_frames(viser_file)


if __name__ == "__main__":
    tyro.cli(main)
