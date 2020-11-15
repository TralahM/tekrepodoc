"""repodoc main entry points, i.e commands."""
import argparse
import yaml
import os
import logging
import repodoc
from repodoc.log import configure_logger
from repodoc import writer
from repodoc import render
from repodoc import prompt

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logger = logging.getLogger("repodoc")

__all__ = [
    "writer",
    "render",
    "prompt",
    "argparse",
    "configure_logger",
    "main",
    "epilog",
    "description",
    "community_health",
    "sphinx_docs",
    "licence",
    "logger",
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
    "resolve_template_name",
    "get_main_parser",
]


def get_all_template_variables(Templates=render.Templates, logger=logger):
    """Return all template variables."""
    all_vars = []
    for t_name in Templates:
        t_vars = render.get_variables(t_name, logger=logger)
        all_vars.extend(t_vars)
    return sorted(list(set(all_vars)))


def resolve_template_name(tname):
    """Resolve template name."""
    t_name = tname.split(".j2")[0]
    if t_name in render.LicenceMap.keys():
        return render.LicenceMap.get(t_name)
    elif t_name in render.DocMap.keys():
        return render.DocMap.get(t_name)
    elif t_name in render.CommunityHealth_Map.keys():
        return render.CommunityHealth_Map.get(t_name)
    elif t_name in render.RootMap.keys():
        return render.RootMap.get(t_name)
    else:
        return


def get_template_variables(args):
    """Return all variables for the given template."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    if args.get_vars_all:
        print(yaml.dump(get_all_template_variables(logger=logger)))
        return
    elif args.get_vars_list:
        print(yaml.dump(render.TemplateNames))
        return
    else:
        template_name = args.template_name
        t_name = (
            template_name if template_name.endswith(
                ".j2") else template_name + ".j2"
        )
        t_vars = render.get_variables(
            resolve_template_name(t_name), logger=logger)
        print(yaml.dump(t_vars))
        return t_vars


def gen_default_context():
    """Generate Default Context Dict for Configuration."""
    variables = get_all_template_variables()

    def get_var_default(v):
        list_vs = ["install_requires", "console_scripts"]
        bool_vs = ["readthedocs", "pypi", "create_docs"]
        if v in list_vs:
            return [
                "",
            ]
        elif v in bool_vs:
            return True
        else:
            return ""

    return dict(zip(variables, list(map(get_var_default, variables))))


def gen_config_file(
    filename="repodoc_config.yml", context=gen_default_context(), **kwargs
):
    """Generate Sample Configuration File."""
    data = context
    with open(filename, "w") as wf:
        yaml.dump(data, wf, Dumper=Dumper)
    logger.info(f"Generated Configuration in {filename}")
    return data


def update_config_file(file, config):
    """Update Config File with config data."""
    with open(file, "w") as wf:
        yaml.dump(config, wf, Dumper=Dumper)
    logger.info(f"Updated Configuration in {file}")
    return


def config_from_file(config_file):
    """Read and Return dict of configuration parameters from file."""
    with open(config_file, "r") as cf:
        config = yaml.load(cf, Loader=Loader)
    return config


def config(args):
    """Configure Subcommand to init,set,get,list configs."""
    configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    to_append = ["install_requires", "console_scripts"]
    bool_vals = ["readthedocs", "create_docs", "pypi"]
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
        configure(args)
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
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(
            Templates=render.CommunityHealth_Templates, logger=logger
        )
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
            *render.render_template(t_name, logger=logger, **kwargs),
            logger=logger,
        )
    return


def dot_files(args):
    """Generate all dot files .gitignore,.gitattributes,.mailmap."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    kwargs = config_from_file(args.config_file)
    for t_name in render.DotTemplates:
        writer.write_rendered_template(
            *render.render_template(
                t_name,
                logger=logger,
                **kwargs,
            ),
            logger=logger,
        )
    return


def sphinx_docs(args):
    """Generate Sphinx Documentation Templates."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(
            Templates=render.DocTemplates, logger=logger
        )
        ch_vals = [
            args.author_name,
            args.program_name,
            args.version,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    for t_name in render.DocTemplates:
        writer.write_rendered_template(
            *render.render_template(t_name, logger=logger, **kwargs),
            logger=logger,
        )
    return


def licence(args):
    """Generate Licence Command."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(
            Templates=render.LicenceTemplates, logger=logger
        )
        ch_vals = [
            args.author_name,
            args.program_name,
        ]
        kwargs = dict(zip(ch_vars, ch_vals))
    writer.write_rendered_template(
        *render.render_licence(args.licence, logger=logger, **kwargs),
        logger=logger,
    )
    return


def readme(args):
    """Generate README command."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
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
    writer.write_rendered_template(
        *render.render_readme(
            logger=logger,
            **kwargs,
        ),
        logger=logger,
    )
    return


def pypi_project(args):
    """Generate Pypi Manifest,setup.cfg,setup.py Command."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    if args.use_conf:
        kwargs = config_from_file(args.config_file)
    else:
        ch_vars = get_all_template_variables(
            Templates=render.Pypi_Templates,
            logger=logger,
        )
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
            *render.render_template(t_name, logger=logger, **kwargs),
            logger=logger,
        )
    return


def bump_version(args):
    """Increment Project Package Version in setup.cfg and docs/conf.py."""
    logger = configure_logger(
        stream_level="DEBUG" if args.verbose else "INFO",
        debug_file=None,
    )
    return logger


def configure(args):
    """Return Configuration Dictionary."""
    if args.use_conf:
        context = config_from_file(args.config_file)
    else:
        context = gen_default_context()
    bool_values = [k for k, v in context.items() if isinstance(v, bool)]
    list_values = [k for k, v in context.items() if isinstance(v, list)]
    for key, default in context.items():
        if key in bool_values:
            context[key] = prompt.read_user_yes_no(key, default)
        elif key in list_values:
            context[key] = prompt.read_user_list(
                key, ",".join(default), sep=",")
        elif key == "licence":
            context[key] = prompt.read_user_choice(
                key, list(render.LicenceMap.keys()))
        else:
            context[key] = prompt.read_user_variable(key, default)
    # return context
    return gen_config_file(context=context)


def usage(args, **kwargs):
    """Handle Main repodoc Entrypoint without subcommands."""
    if args.bash_completion:
        import shtab

        print(shtab.complete(args.parser, shell="bash"))
        return
    if args.zsh_completion:
        import shtab

        print(shtab.complete(args.parser, shell="zsh"))
        return
    print(description())
    print()
    print(epilog())


def description(*args, **kwargs):
    """Return Description."""
    import art

    return art.text2art(
        f"{repodoc.__name__} {repodoc.__version__}",
        font="standard",
    )


def epilog(*args, **kwargs):
    """Return Epilog."""
    author = "Tralah M Brian (TralahM) " + "<musyoki.brian@tralahtek.com>"
    github = "https://github.com/TralahM/tekrepodoc"
    return f"""Author:\t{author}.
Project:\t<{github}>"""


def get_main_parser():
    """Return main argparse.ArgumentParser object."""
    parser = argparse.ArgumentParser(epilog=epilog())
    parser.set_defaults(
        func=usage,
        use_conf=False,
        parser=parser,
        config_file="repodoc_config.yml",
    )
    parser.add_argument(
        "-u",
        "--use-config-file",
        help="use config file for template variables.",
        action="store_true",
        dest="use_conf",
    )
    parser.add_argument(
        "-bc",
        "--bash-completion",
        help="Print Bash Completion Script.",
        action="store_true",
        dest="bash_completion",
    )
    parser.add_argument(
        "-zc",
        "--zsh-completion",
        help="Print ZSH Completion Script.",
        action="store_true",
        dest="zsh_completion",
    )
    parser.add_argument(
        "-vv",
        "--verbose",
        help="Turn on Verbose Mode.",
        action="store_true",
        dest="verbose",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{repodoc.__name__}  v{repodoc.__version__}",
    )
    subparsers = parser.add_subparsers(title="subcommands")
    # Begin vars_parser Subparser
    vars_parser = subparsers.add_parser(
        "get_vars",
        help=get_template_variables.__doc__,
    )
    vars_parser.set_defaults(func=get_template_variables)
    vp_grp = vars_parser.add_mutually_exclusive_group(required=True)
    vp_grp.add_argument(
        "-t",
        "--template_name",
        choices=render.TemplateNames,
        action="store",
        dest="template_name",
        help="name of template e.g README.md or README.md.j2",
        metavar="Template_Name.ext.j2",
    )
    vp_grp.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="get_vars_all",
        default=False,
        help="Get all variables for all available templates.",
    )
    vp_grp.add_argument(
        "-l",
        "--list-all",
        action="store_true",
        dest="get_vars_list",
        default=False,
        help="List all available template names.",
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
        default=os.path.basename(os.path.abspath(os.path.curdir)),
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
    return parser


def main():
    """Run Main Entry Point."""
    parser = get_main_parser()
    args = parser.parse_args()
    args.func(args)
    return


if __name__ == "__main__":
    main()
