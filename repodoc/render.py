"""Jinja2 template renderer."""
import jinja2
import jinja2.meta

Loader = jinja2.PackageLoader(package_name="repodoc", package_path="templates")
Environment = jinja2.Environment(
    loader=Loader,
    extensions=[
        "jinja2_time.TimeExtension",
    ],
)
Templates = Environment.list_templates()
LicenceTemplates = [x for x in Templates if x.startswith("licences")]
LicenceMap = {x.split("/")[-1].split(".j2")[0]: x for x in LicenceTemplates}
DocTemplates = [x for x in Templates if x.startswith("docs")]
DocTemplates.append("readthedocs.yml.j2")
DocMap = {x.split("/")[-1].split(".j2")[0]: x for x in DocTemplates}
CommunityHealth_Templates = [x for x in Templates if x.startswith(".github")]
CommunityHealth_Map = {
    x.split("/")[-1].split(".j2")[0]: x for x in CommunityHealth_Templates
}
Pypi_Templates = ["MANIFEST.in.j2", "setup.cfg.j2", "setup.py.j2"]
RootTemplates = [x for x in Templates if "/" not in x]
RootMap = {x.split("/")[-1].split(".j2")[0]: x for x in RootTemplates}
DotTemplates = [x for x in RootTemplates if x.startswith(".")]
DotMap = {x.split("/")[-1].split(".j2")[0]: x for x in DotTemplates}


def get_variables(template_name):
    """Return all undeclared variables in template."""
    template_source = Environment.loader.get_source(
        Environment, template_name)[0]
    parsed_content_ast = Environment.parse(template_source)
    variables = jinja2.meta.find_undeclared_variables(parsed_content_ast)
    return list(variables)


def get_output_filename(template_name):
    """Return Destination output filename for given template_name."""
    return template_name.split(".j2")[0]


def render_template(template_name, **kwargs):
    """Render template_name with kwargs."""
    template = Environment.get_template(template_name)
    return (get_output_filename(template_name), template.render(**kwargs))


def render_gitattributes(**kwargs):
    """Render .gitattributes.j2 with kwargs."""
    template_name = ".gitattributes.j2"
    return render_template(template_name, **kwargs)


def render_contributing(**kwargs):
    """Render .github/CONTRIBUTING.rst.j2 with kwargs."""
    template_name = ".github/CONTRIBUTING.rst.j2"
    return render_template(template_name, **kwargs)


def render_gitignore(**kwargs):
    """Render .gitignore.j2 with kwargs."""
    template_name = ".gitignore.j2"
    return render_template(template_name, **kwargs)


def render_mailmap(**kwargs):
    """Render .mailmap.j2 with kwargs."""
    template_name = ".mailmap.j2"
    return render_template(template_name, **kwargs)


def render_code_of_conduct(**kwargs):
    """Render .github/CODE_OF_CONDUCT.md.j2 with kwargs."""
    template_name = ".github/CODE_OF_CONDUCT.md.j2"
    return render_template(template_name, **kwargs)


def render_security(**kwargs):
    """Render .github/SECURITY.md.j2 with kwargs."""
    template_name = ".github/SECURITY.md.j2"
    return render_template(template_name, **kwargs)


def render_support(**kwargs):
    """Render .github/SUPPORT.md.j2 with kwargs."""
    template_name = ".github/SUPPORT.md.j2"
    return render_template(template_name, **kwargs)


def render_funding(**kwargs):
    """Render .github/FUNDING.yml.j2 with kwargs."""
    template_name = ".github/FUNDING.yml.j2"
    return render_template(template_name, **kwargs)


def render_manifest(**kwargs):
    """Render MANIFEST.in.j2 with kwargs."""
    template_name = "MANIFEST.in.j2"
    return render_template(template_name, **kwargs)


def render_pull_request_template(**kwargs):
    """Render .github/PULL_REQUEST_TEMPLATE.md.j2 with kwargs."""
    template_name = ".github/PULL_REQUEST_TEMPLATE.md.j2"
    return render_template(template_name, **kwargs)


def render_readme(**kwargs):
    """Render README.md.j2 with kwargs."""
    template_name = "README.md.j2"
    return render_template(template_name, **kwargs)


def render_bug_report(**kwargs):
    """Render .github/ISSUE_TEMPLATE/bug_report.md.j2 with kwargs."""
    template_name = ".github/ISSUE_TEMPLATE/bug_report.md.j2"
    return render_template(template_name, **kwargs)


def render_docs_makefile(**kwargs):
    """Render docs/Makefile.j2 with kwargs."""
    template_name = "docs/Makefile.j2"
    return render_template(template_name, **kwargs)


def render_docs_api(**kwargs):
    """Render docs/api.rst.j2 with kwargs."""
    template_name = "docs/api.rst.j2"
    return render_template(template_name, **kwargs)


def render_docs_makebat(**kwargs):
    """Render docs/make.bat.j2 with kwargs."""
    template_name = "docs/make.bat.j2"
    return render_template(template_name, **kwargs)


def render_docs_requirements(**kwargs):
    """Render docs/requirements.txt.j2 with kwargs."""
    template_name = "docs/requirements.txt.j2"
    return render_template(template_name, **kwargs)


def render_docs_conf(**kwargs):
    """Render docs/conf.py.j2 with kwargs."""
    template_name = "docs/conf.py.j2"
    return render_template(template_name, **kwargs)


def render_docs_contents(**kwargs):
    """Render docs/contents.rst.j2 with kwargs."""
    template_name = "docs/contents.rst.j2"
    return render_template(template_name, **kwargs)


def render_docs_index(**kwargs):
    """Render docs/index.rst.j2 with kwargs."""
    template_name = "docs/index.rst.j2"
    return render_template(template_name, **kwargs)


def render_feature_request(**kwargs):
    """Render .github/ISSUE_TEMPLATE/feature_request.md.j2."""
    template_name = ".github/ISSUE_TEMPLATE/feature_request.md.j2"
    return render_template(template_name, **kwargs)


def render_issue_template_config(**kwargs):
    """Render .github/ISSUE_TEMPLATE/config.yml.j2."""
    template_name = ".github/ISSUE_TEMPLATE/config.yml.j2"
    return render_template(template_name, **kwargs)


def render_licence(licence, **kwargs):
    """Render LICENCE.j2."""
    template_name = LicenceMap.get(licence)
    return ("LICENCE", render_template(template_name, **kwargs)[-1])


def render_readthedocs(**kwargs):
    """Render readthedocs.yml.j2."""
    template_name = "readthedocs.yml.j2"
    return render_template(template_name, **kwargs)


def render_setup_cfg(**kwargs):
    """Render setup.cfg.j2."""
    template_name = "setup.cfg.j2"
    return render_template(template_name, **kwargs)


def render_setup_py(**kwargs):
    """Render setup.py.j2."""
    template_name = "setup.py.j2"
    return render_template(template_name, **kwargs)
