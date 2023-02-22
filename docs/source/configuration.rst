Configuration
#############

The plugin runs in the context of a dbt project.

Project directory
************************
When you run `pytest` from the root of your project, you do **not** need to set
the project directory. If you want to run `pytest` from another location, you
point the `--dbt-project-dir`
`option <https://docs.pytest.org/en/6.2.x/usage.html#getting-help-on-version-option-names-environment-variables>`_
to the root of your project.

Target
************************
If you want to use another
`target <https://docs.getdbt.com/reference/dbt-jinja-functions/target>`_
than the default, you set the `--dbt-target`
`option <https://docs.pytest.org/en/6.2.x/usage.html#getting-help-on-version-option-names-environment-variables>`_.

Profiles directory
**********************
If you want to change dbt's profiles directory, use the `--profiles-dir` `option <https://docs.getdbt.com/dbt-cli/configure-your-profile/#advanced-customizing-a-profile-directory>`_.
