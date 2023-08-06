.. {# pkglts, glabpkg, after doc
{% for name in git.permanent_branches %}
{{ name }}: |{{ name }}_build|_ |{{ name }}_coverage|_

.. |{{ name }}_build| image:: {{ gitlab.url }}/badges/{{ name }}/pipeline.svg
.. _{{ name }}_build: {{ gitlab.url }}/commits/{{ name }}

.. |{{ name }}_coverage| image:: {{ gitlab.url }}/badges/{{ name }}/coverage.svg
.. _{{ name }}_coverage: {{ gitlab.url }}/commits/{{ name }}
{% endfor -%}
.. #}
