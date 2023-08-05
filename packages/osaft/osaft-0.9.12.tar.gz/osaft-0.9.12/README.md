# osaft

[![Coverage][cov-image]][cov-url]
[![License][lic-image]][lic-url]
[![Pipeline][pipeline-image]][pipeline-url]
[![Docs][docs-image]][docs-url]

The *osaft* Python package implements classical theories for the
computation of the acoustic scattering, acoustic streaming, and the acoustic
radiation force on a particle subjected to an ultrasonic wave. The package
provides a unified API that allows for the simple evaluation of quantities
often used in the research field of microscale acoustofluidics.
Also included in the package are plotting tools (using Matplotlib), so
generated results can easily be illustrated.

## Installation

All systems with `pip`/`python` installed

```sh
python -m pip install osaft
```

If you want to learn more go to the documentation's
[installation page](https://osaft.readthedocs.io/en/stable/installation/).

## Usage example

Examples how the *osaft* framework can be used can be found on our
[examples page](https://osaft.readthedocs.io/en/stable/examples) of the
documentation.

## Citing

A publication presenting the *osaft* framework is in preparation. This
section will be updated as soon as the article has been published.

## Release History

Find the changes introduced with new releases in the
[``CHANGELOG.md``](https://gitlab.com/acoustofluidics/osaft/-/blob/main/CHANGELOG.md).

## License
The distribution is licenced under the GNU Lesser General Public License. See
[``LICENSE.md``](https://gitlab.com/acoustofluidics/osaft/-/blob/main/LICENSE.md)
to learn more.

## Contributing

1. Fork it (<https://gitlab.com/acoustofluidics/osaft/-/forks/new>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[king]: https://osaft.readthedocs.io/en/stable/solutions/king1934/
[yosioka]: https://osaft.readthedocs.io/en/stable/solutions/yosioka1955/
[osaft]: https://osaft.readthedocs.io/en/stable/solutions/osaft1962/
[doinikov1994R]: https://osaft.readthedocs.io/en/stable/solutions/doinikov1994rigid/
[doinikov1994C]: https://osaft.readthedocs.io/en/stable/solutions/doinikov1994compressible/
[settnes]: https://osaft.readthedocs.io/en/stable/solutions/settnes2012/
[pipeline-image]: https://gitlab.com/acoustofluidics/osaft/badges/developer/pipeline.svg
[pipeline-url]: https://gitlab.com/acoustofluidics/osaft/-/pipelines/
[cov-image]: https://gitlab.com/acoustofluidics/osaft/badges/developer/coverage.svg
[cov-url]: https://gitlab.com/acoustofluidics/osaft/badges/developer/coverage.svg
[lic-image]: https://img.shields.io/badge/License-LGPL%20v3-gold.svg
[lic-url]: https://www.gnu.org/licenses/lgpl-3.0
[docs-image]: https://readthedocs.org/projects/osaft/badge/?version=stable
[docs-url]: https://osaft.readthedocs.io/en/stable/
[examples]: https://osaft.readthedocs.io/en/stable/examples
