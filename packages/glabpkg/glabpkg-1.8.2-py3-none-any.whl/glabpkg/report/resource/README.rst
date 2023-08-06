.. {# pkglts, glabreport, after doc

{% for name in git.permanent_branches -%}
{{ name }}: |{{ name }}_build|_ {%- if 'test' is available %}|{{ name }}_coverage|_{% endif %}

.. |{{ name }}_build| image:: {{ gitlab.url }}/badges/{{ name }}/pipeline.svg
.. _{{ name }}_build: {{ gitlab.url }}/commits/{{ name }}
{%- if 'test' is available %}
.. |{{ name }}_coverage| image:: {{ gitlab.url }}/badges/{{ name }}/coverage.svg
.. _{{ name }}_coverage: {{ gitlab.url }}/commits/{{ name }}
{% endif %}

{% endfor -%}
.. #}

Instructions
------------

To compile the documentation, you need a python environment with sphinx.

.. code-block:: bash

    $ conda activate myenv
    (myenv)$ cd report
    (myenv)$ make html

The resulting document should be in **report/build/html/index.html**

If you want to replay the analysis, all the scripts that generated the figures
are in the **script** folder.
