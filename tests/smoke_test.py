"""Basic smoke test for release artifacts.

Ensures the packaged distribution can be installed and still round-trip
example data via the public encode/decode API.
"""

from toon_py import decode, encode


def main() -> None:
    payload = {
        "name": "Ada Lovelace",
        "age": 36,
        "skills": ["mathematics", "computing", "poetry"],
        "active": True,
    }

    serialized = encode(payload)
    restored = decode(serialized)

    if restored != payload:
        raise AssertionError(
            f"Round-trip mismatch.\nencoded={serialized!r}\n"
            f"expected={payload!r}\nactual={restored!r}"
        )


if __name__ == "__main__":
    main()
