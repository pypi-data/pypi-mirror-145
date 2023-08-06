# BELA Dashboard

BELA Dashboard is a web-based user interface for visualising and analysing BELA transcripts.
To learn how to create BELA transcripts, please refer to the [BELA convention documentation](https://blipntu.github.io/belacon/).

BELA Dashboard uses the [Python bela package](https://github.com/letuananh/bela) to process transcripts under the hood.
Users who want to perform batch processing or data extraction can use [bela](https://github.com/letuananh/bela) package directly using Python scripts.

## Installation

**belaweb** is available on [PyPI](https://pypi.org/project/belaweb/) and can be installed using pip:

```bash
pip install belaweb
```

## Development

To run belaweb locally for testing, there is a minimal WSGI application available at https://github.com/letuananh/belaweb

```bash
# activate a Python (virtual) environment with belaweb package installed
cd belaweb-wsgi-min
./manage.py runserver
```

Then access belaweb locally using a browser: http://localhost:8000/bela/gui/

## License

**belaweb** package is licensed under MIT License.
The following packages are included:

- [Chart.js v2.9.4](https://www.chartjs.org/docs/2.9.4/) - MIT License
