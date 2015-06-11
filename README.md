ree-demanda
===========

Utilities to extract Spanish power generation statistics from [demanda.ree.es](http://demanda.ree.es/demanda.html). REE's service exposes a visualization of power generation statistics, as well as demand forecasts.

REE's Flash visualizer is backed by a SOAP web service providing detailing statistics. However, the web service is not publicly documented. In fact, it features a clumsy mechanism to prevent access.

This projecs aims to provide basic reference utilities to extract and manipulate REE's web service.

Read more: [Unlocking data: Power generation statistics in Spain](http://mola.io/2013/08/29/unlocking-data-spain-power-generation/)

Data
====

Full data can be downloaded in CSV format here:

- [generation\_demand\_full.csv](http://smola.github.io/ree-demanda/generation_demand_full.csv)

This data may be outdated. If you need an update, you can ping me at santi@mola.io.

License
=======

Copyright (c) 2013-2015 Santiago M. Mola

This project is released under the MIT License. A copy can be found in the LICENSE file.

Files in the `wsdl` directory are owned by Red Eléctrica de España, S.A. and are stored here only for reference.

Ffiles in the `data` directory are dumps of data produced by this tool from original data by Red Eléctrica de España, S.A.
