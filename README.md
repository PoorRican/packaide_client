# Overview

This is a simple API wrapper that allows interaction with a [PackaideServer](https://github.com/PoorRica/packaide_server) instance.

The API allows for passing multiple SVG files to the server, which are then nested into one or more SVG files. The
resulting SVG files are then returned to the client.


## Installation

```bash
pip install packaide_client
```


## Usage

The main class is a `PackaideClient` which exposes a single method `pack`. This method takes a list of SVG strings,
height and width (in inches) and returns a list of SVG strings. The resulting SVG strings will have the nested shapes.

As a side note, the original size (ie: `viewBox`) of the input SVG files has no influence on the size of the output SVG
files. The output SVG will always conform to the height and width parameters. However, if any shape or path in the input
SVG files is too large to fit in the output SVG, a `ValueError` will be always be raised.

## Example

```python
from packaide_client import PackaideClient

# URL is the address of the server instance, usually operating on port 8000
URL = "http://localhost:8000"

client = PackaideClient(URL)

svg1 = "<svg>...</svg>"
svg2 = "<svg>...</svg>"

results = client.pack([svg1, svg2], height=60, width=40,
                      tolerance=.1,
                      offset=5,
                      rotations=4)  # Returns a list of SVGs

# results can be passed to other functions
for sheet in results:
    print(sheet)

# Or written to a files
for i, sheet in enumerate(results):
    with open(f"sheet_{i}.svg", "w") as f:
        f.write(sheet)
```


## Parameters

The `pack` method takes the following parameters:
- `svgs`: A list of SVG strings to be nested
- `height`: The height of the output SVG in inches
- `width`: The width of the output SVG in inches
- `tolerance`: The tolerance used when quantizing curves (Discretization tolerance)
- `offset`: The offset distance around each shape (dilation)
- `rotations`: The number of rotations to attempt when nesting shapes.