"""repodoc main entry points, i.e commands."""
import argparse
import yaml

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from . import writer
from . import render

__all__ = [
    "writer",
    "render",
    "argparse",
    "main",
    "community_health",
    "sphinx_docs",
    "licence",
    "readme",
    "pypi_project",
    "usage",
    "configure",
    "gen_config_file",
    "config_from_file",
    "get_all_template_variables",
    "bump_version",
    "dot_files",
    "update_config_file",
]


def get_all_template_variables(Templates=render.Templates):
    """Return all template variables."""
    all_vars = []
    for t_name in Templates:
        t_vars = render.get_variables(t_name)
        all_vars.extend(t_vars)
    return sorted(list(set(all_vars)))


def get_template_variables(args):
    """Return all variables for the given template."""
    template_name = args.template_name
    t_name = template_name if template_name.endswith(
        ".j2") else template_name + ".j2"
    t_vars = render.get_variables(t_name)
    print(yaml.dump(t_vars))
    return t_vars


def gen_config_file(*args, **kwargs):
    """Generate Sample Configuration File."""
    filename = "repodoc_config.yml"
    variables = get_all_template_variables()
    list_vs = ["install_requires", "console_scripts"]
    values = ["" if v not in list_vs else [""] for v in variables]
    # values = variables
    data = dict(zip(variables, values))
    with open(filename, "w") as wf:
        yaml.dump(data, wf, Dumper=Dumper)
    print(f"Generated Configuration in {filename}")
    return data


def update_config_file(file, config):
    """Update Config File with config data."""
    with open(file, "w") as wf:
        yaml.dump(config, wf, Dumper=Dumper)
    print(f"Updated Configuration in {file}")
    return


def config_from_file(config_file):
    """Read and Return dict of configuration parameters from file."""
    with open(config_file, "r") as cf:
        config = yaml.load(cf, Loader=Loader)
    return config


def config(args):
    """Configure Subcommand to init,set,get,list configs."""
    to_append = ["install_requires", "console_scripts"]
    bool_vals = ["readthedocs"]
    config = config_from_file(args.config_file)
    if args.list:
        print(yaml.dump(config))
    if args.get:
        print(config.get(args.get))
    if args.add:
        if args.add[0] in to_append:
            config[args.add[0]] = config[args.add[0]].append(args.add[1])
        else:
            if args.add[0] in bool_vals:
                if args.add[1].upper() == "True".upper():
                    config[args.add[0]] = True
                else:
                    config[args.add[0]] = False
            else:
                config[args.add[0]] = args.add[1]
        update_config_file(args.config_file, config)
    if args.init:
        gen_config_file()
    if args.set:
        if args.set[0] in to_append:
            config[args.set[0]] = args.set[1].split(",")
        else:
            if args.set[0] in bool_vals:
                if args.set[1].upper() == "True".upper():
                    config[args.set[0]] = True
                else:
                    config[args.set[0]] = False
            else:
                config[args.set[0]] = args.set[1]
        update_config_file(args.config_file, config)
    return


def community_health(args):
    """Generate Community Health Guidelines."""
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(
            Templates=render.CommunityHealth_Templates)
        ch_vals = [
            args.author_email,
            args.author_name,
            args.author_username,
            args.licence,
            args.program_name,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    for t_name in render.CommunityHealth_Templates:
        writer.write_rendered_template(
            *render.render_template(t_name, **kwargs))
    return


def dot_files(args):
    """Generate all dot files .gitignore,.gitattributes,.mailmap."""
    kwargs = config_from_file(args.config_file)
    dotfile_templates = [".gitignore.j2", ".gitattributes.j2", ".mailmap.j2"]
    for t_name in dotfile_templates:
        writer.write_rendered_template(
            *render.render_template(t_name, **kwargs),
        )
    return


def sphinx_docs(args):
    """Generate Sphinx Documentation Templates."""
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(Templates=render.DocTemplates)
        ch_vals = [
            args.author_name,
            args.program_name,
            args.version,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    for t_name in render.DocTemplates:
        writer.write_rendered_template(
            *render.render_template(t_name, **kwargs))
    return


def licence(args):
    """Generate Licence Command."""
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(Templates=render.LicenceTemplates)
        ch_vals = [
            args.author_name,
            args.program_name,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    writer.write_rendered_template(
        *render.render_licence(args.licence, **kwargs))
    return


def readme(args):
    """Generate README command."""
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        t_name = "README.md.j2"
        ch_vars = render.get_variables(t_name)
        ch_vals = [
            args.author_username,
            args.repo_name,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    writer.write_rendered_template(*render.render_readme(**kwargs))
    return


def pypi_project(args):
    """Generate Pypi Manifest,setup.cfg,setup.py Command."""
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(Templates=render.Pypi_Templates)
        ch_vals = [
            args.author_email,
            args.author_name,
            args.author_username,
            args.console_scripts,
            args.install_requires,
            args.package_name,
            args.program_description,
            args.program_name,
            args.version,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    for t_name in render.Pypi_Templates:
        writer.write_rendered_template(
            *render.render_template(t_name, **kwargs))
    return


def bump_version(args):
    """Increment Project Package Version in setup.cfg and docs/conf.py."""
    return


def configure(**kwargs):
    """Return Configuration Dictionary."""
    return


def usage(*args, **kwargs):
    """Print Usage Instructions."""
    return


def main():
    """Run Main Entry Point."""
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=usage, use_conf=False,
                        config_file="repodoc_config.yml")
    parser.add_argument(
        "-u",
        "--use-config-file",
        help="use config file for template variables.",
        action="store_true",
        dest="use_conf",
    )
    subparsers = parser.add_subparsers()
    # Begin vars_parser Subparser
    vars_parser = subparsers.add_parser(
        "get_vars",
        help=get_template_variables.__doc__,
    )
    vars_parser.set_defaults(func=get_template_variables)
    vars_parser.add_argument(
        "template_name",
        help="name of template e.g README.md or README.md.j2",
        metavar="Template_Name.ext.j2",
    )
    # End vars_parser Subparser
    # Begin config Subparser
    config_parser = subparsers.add_parser(
        "config",
        help=config.__doc__,
    )
    config_parser.set_defaults(
        func=config,
        add=False,
        set=False,
        get=False,
    )
    config_parser.add_argument(
        "-f",
        "--file",
        help="use given config file",
        action="store",
        dest="config_file",
        default="repodoc_config.yml",
        type=str,
    )
    config_parser.add_argument(
        "-l",
        "--list",
        help="list all",
        action="store_true",
    )
    config_parser.add_argument(
        "--init",
        help=gen_config_file.__doc__,
        action="store_true",
    )
    config_parser.add_argument(
        "--get",
        help="get value: name",
        action="store",
        dest="get",
        metavar="name",
    )
    config_parser.add_argument(
        "--set",
        help="set value of variable: name value",
        action="store",
        dest="set",
        metavar=("name", "value"),
        nargs=2,
    )
    config_parser.add_argument(
        "--add",
        help="add a new variable: name value",
        action="store",
        dest="add",
        metavar=("name", "value"),
        nargs=2,
    )
    # End config Subparser
    # Begin Licence Subparser
    licence_parser = subparsers.add_parser(
        "licence",
        help=licence.__doc__,
    )
    licence_parser.set_defaults(func=licence)
    licence_parser.add_argument(
        "licence",
        choices=list(render.LicenceMap.keys()),
        default="MIT",
        help="Type of Licence to generate.",
    )
    licence_parser.add_argument(
        "-a",
        "--author-name",
        action="store",
        dest="author_name",
        default="Tralah M Brian",
        help="Author Name",
    )
    licence_parser.add_argument(
        "-p",
        "--program-name",
        action="store",
        dest="program_name",
        required=True,
        help="Program Name",
    )
    # End Licence Subparser
    # Begin README Subparser
    readme_parser = subparsers.add_parser(
        "readme",
        help=readme.__doc__,
    )
    readme_parser.set_defaults(func=readme)
    # End README Subparser
    # Begin COM_HEALTH Subparser
    community_health_parser = subparsers.add_parser(
        "community_health",
        aliases=["comh", "ch"],
        help=community_health.__doc__,
    )
    community_health_parser.set_defaults(func=community_health)
    # End COM_HEALTH Subparser
    # Begin PYPI Subparser
    pypi_project_parser = subparsers.add_parser(
        "pypi_project",
        aliases=[
            "pypi",
        ],
        help=pypi_project.__doc__,
    )
    pypi_project_parser.set_defaults(func=pypi_project)
    # End PYPI Subparser
    # Begin SPHINX Subparser
    sphinx_docs_parser = subparsers.add_parser(
        "sphinx_docs",
        aliases=["docs", "sphinx"],
        help=sphinx_docs.__doc__,
    )
    sphinx_docs_parser.set_defaults(func=sphinx_docs)
    # End SPHINX Subparser
    # Begin dot_files Subparser
    dot_files_parser = subparsers.add_parser(
        "dot_files",
        aliases=["dots"],
        help=dot_files.__doc__,
    )
    dot_files_parser.set_defaults(func=dot_files)
    # End dot_files Subparser
    args = parser.parse_args()
    args.func(args)
    return


if __name__ == "__main__":
    main()
