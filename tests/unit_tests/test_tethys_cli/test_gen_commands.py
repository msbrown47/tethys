import unittest
from unittest import mock
from pathlib import Path

import tethys_cli.gen_commands as tethys_gen_commands
from tethys_cli.gen_commands import (
    get_environment_value,
    get_settings_value,
    derive_version_from_conda_environment,
    gen_meta_yaml,
    generate_command,
    gen_vendor_static_files,
    download_vendor_static_files,
    get_destination_path,
    GEN_APACHE_OPTION,
    GEN_APACHE_SERVICE_OPTION,
    GEN_NGINX_OPTION,
    GEN_NGINX_SERVICE_OPTION,
    GEN_ASGI_SERVICE_OPTION,
    GEN_SERVICES_OPTION,
    GEN_INSTALL_OPTION,
    GEN_PORTAL_OPTION,
    GEN_META_YAML_OPTION,
    GEN_PACKAGE_JSON_OPTION,
    GEN_REQUIREMENTS_OPTION,
    VALID_GEN_OBJECTS,
)

from tethys_apps.utilities import get_tethys_src_dir

TETHYS_SRC = get_tethys_src_dir()


class CLIGenCommandsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("tethys_cli.cli_colors.write_warning")
    def test_no_conda(self, mock_warn):
        import tethys_cli.gen_commands as tethys_gen_commands
        from importlib import reload
        import builtins

        real_import = builtins.__import__

        def mock_import(name, *args):
            if name == "conda.cli.python_api":
                raise ModuleNotFoundError
            else:
                return real_import(name, *args)

        builtins.__import__ = mock_import
        reload(tethys_gen_commands)
        builtins.__import__ = real_import
        self.assertEqual(tethys_gen_commands.has_conda, False)
        mock_warn.assert_called_once()

    def test_get_environment_value(self):
        result = get_environment_value(value_name="DJANGO_SETTINGS_MODULE")

        self.assertEqual("tethys_portal.settings", result)

    def test_get_environment_value_bad(self):
        self.assertRaises(
            EnvironmentError,
            get_environment_value,
            value_name="foo_bar_baz_bad_environment_value_foo_bar_baz",
        )

    def test_get_settings_value(self):
        result = get_settings_value(value_name="INSTALLED_APPS")

        self.assertIn("tethys_apps", result)

    def test_get_settings_value_bad(self):
        self.assertRaises(
            ValueError,
            get_settings_value,
            value_name="foo_bar_baz_bad_setting_foo_bar_baz",
        )

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.get_settings_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_apache_option(
        self, mock_os_path_isfile, mock_file, mock_settings, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_APACHE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_settings.side_effect = ["/foo/workspace", "/foo/static"]

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_settings.assert_called_with("STATIC_ROOT")

        mock_write_info.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.get_settings_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_nginx_option(
        self, mock_os_path_isfile, mock_file, mock_settings, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_NGINX_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_settings.side_effect = ["/foo/workspace", "/foo/static"]

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_settings.assert_any_call("TETHYS_WORKSPACES_ROOT")
        mock_settings.assert_called_with("STATIC_ROOT")

        mock_write_info.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_nginx_service(
        self, mock_os_path_isfile, mock_file, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_NGINX_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()

        mock_write_info.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_apache_service(
        self, mock_os_path_isfile, mock_file, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_APACHE_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()

        mock_write_info.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.os.path.isdir")
    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    @mock.patch("tethys_cli.gen_commands.os.makedirs")
    def test_generate_command_portal_yaml__tethys_home_not_exists(
        self, mock_makedirs, mock_os_path_isfile, mock_file, mock_write_info, mock_isdir
    ):
        mock_args = mock.MagicMock(
            type=GEN_PORTAL_OPTION, directory=None, spec=["overwrite", "server_port"]
        )
        mock_os_path_isfile.return_value = False
        mock_isdir.side_effect = [
            False,
            True,
        ]  # TETHYS_HOME dir exists, computed dir exists

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()

        # Verify it makes the Tethys Home directory
        mock_makedirs.assert_called()
        rts_call_args = mock_write_info.call_args_list[0]
        self.assertIn("A Tethys Portal configuration file", rts_call_args.args[0])

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.render_template")
    @mock.patch("tethys_cli.gen_commands.linux_distribution")
    @mock.patch("tethys_cli.gen_commands.os.path.exists")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_service_option_nginx_conf_redhat(
        self,
        mock_os_path_isfile,
        mock_file,
        mock_env,
        mock_os_path_exists,
        mock_linux_distribution,
        mock_render_template,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_os_path_exists.return_value = True
        mock_linux_distribution.return_value = ["redhat"]
        mock_file.return_value = mock.mock_open(read_data="user foo_user").return_value

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")
        mock_os_path_exists.assert_any_call("/etc/nginx/nginx.conf")
        context = mock_render_template.call_args.args[1]
        self.assertEqual("http-", context["user_option_prefix"])
        self.assertEqual("foo_user", context["nginx_user"])

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.render_template")
    @mock.patch("tethys_cli.gen_commands.linux_distribution")
    @mock.patch("tethys_cli.gen_commands.os.path.exists")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_service_option_nginx_conf_ubuntu(
        self,
        mock_os_path_isfile,
        mock_file,
        mock_env,
        mock_os_path_exists,
        mock_linux_distribution,
        mock_render_template,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_os_path_exists.return_value = True
        mock_linux_distribution.return_value = "ubuntu"
        mock_file.return_value = mock.mock_open(read_data="user foo_user").return_value

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")
        mock_os_path_exists.assert_any_call("/etc/nginx/nginx.conf")
        context = mock_render_template.call_args.args[1]
        self.assertEqual("", context["user_option_prefix"])
        self.assertEqual("foo_user", context["nginx_user"])

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.render_template")
    @mock.patch("tethys_cli.gen_commands.linux_distribution")
    @mock.patch("tethys_cli.gen_commands.os.path.exists")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_service_option_nginx_conf_not_linux(
        self,
        mock_os_path_isfile,
        mock_file,
        mock_env,
        mock_os_path_exists,
        mock_linux_distribution,
        mock_render_template,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_os_path_exists.return_value = True
        mock_linux_distribution.side_effect = Exception
        mock_file.return_value = mock.mock_open(read_data="user foo_user").return_value

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")
        mock_os_path_exists.assert_any_call("/etc/nginx/nginx.conf")
        context = mock_render_template.call_args.args[1]
        self.assertEqual("", context["user_option_prefix"])
        self.assertEqual("foo_user", context["nginx_user"])

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_service_option(
        self, mock_os_path_isfile, mock_file, mock_env, mock_write_info
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.linux_distribution")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_service_option_distro(
        self,
        mock_os_path_isfile,
        mock_file,
        mock_env,
        mock_distribution,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_distribution.return_value = ("redhat", "linux", "")

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.os.path.isdir")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_settings_option_directory(
        self,
        mock_os_path_isfile,
        mock_file,
        mock_env,
        mock_os_path_isdir,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = "/foo/temp"
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_os_path_isdir.side_effect = [
            True,
            True,
        ]  # TETHYS_HOME exists, computed directory exists

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_os_path_isdir.assert_called_with(mock_args.directory)
        mock_env.assert_called_with("CONDA_PREFIX")

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_error")
    @mock.patch("tethys_cli.gen_commands.exit")
    @mock.patch("tethys_cli.gen_commands.os.path.isdir")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_settings_option_bad_directory(
        self,
        mock_os_path_isfile,
        mock_env,
        mock_os_path_isdir,
        mock_exit,
        mock_write_error,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = "/foo/temp"
        mock_os_path_isfile.return_value = False
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_os_path_isdir.side_effect = [
            True,
            False,
        ]  # TETHYS_HOME exists, computed directory exists
        # NOTE: to prevent our tests from exiting prematurely, we change the behavior of exit to raise an exception
        # to break the code execution, which we catch below.
        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, generate_command, args=mock_args)

        mock_os_path_isfile.assert_not_called()
        mock_os_path_isdir.assert_any_call(mock_args.directory)

        # Check if print is called correctly
        rts_call_args = mock_write_error.call_args
        self.assertIn("ERROR: ", rts_call_args.args[0])
        self.assertIn("is not a valid directory", rts_call_args.args[0])

        mock_env.assert_called_with("CONDA_PREFIX")

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.write_warning")
    @mock.patch("tethys_cli.gen_commands.exit")
    @mock.patch("tethys_cli.gen_commands.input")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_settings_pre_existing_input_exit(
        self,
        mock_os_path_isfile,
        mock_env,
        mock_input,
        mock_exit,
        mock_write_warning,
        mock_write_info,
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_args.overwrite = False
        mock_os_path_isfile.return_value = True
        mock_env.side_effect = ["/foo/conda", "conda_env"]
        mock_input.side_effect = ["foo", "no"]
        # NOTE: to prevent our tests from exiting prematurely, we change the behavior of exit to raise an exception
        # to break the code execution, which we catch below.
        mock_exit.side_effect = SystemExit

        self.assertRaises(SystemExit, generate_command, args=mock_args)

        mock_os_path_isfile.assert_called_once()

        # Check if print is called correctly
        rts_call_args = mock_write_warning.call_args
        self.assertIn("Generation of", rts_call_args.args[0])
        self.assertIn("cancelled", rts_call_args.args[0])

        mock_env.assert_called_with("CONDA_PREFIX")

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.get_environment_value")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_asgi_settings_pre_existing_overwrite(
        self, mock_os_path_isfile, mock_file, mock_env, mock_write_info
    ):
        mock_args = mock.MagicMock(conda_prefix=False)
        mock_args.type = GEN_ASGI_SERVICE_OPTION
        mock_args.directory = None
        mock_args.overwrite = True
        mock_os_path_isfile.return_value = True
        mock_env.side_effect = ["/foo/conda", "conda_env"]

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_env.assert_called_with("CONDA_PREFIX")

        mock_write_info.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    def test_generate_command_services_option(
        self, mock_os_path_isfile, mock_file, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_SERVICES_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False

        generate_command(args=mock_args)

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()

    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    @mock.patch("tethys_cli.gen_commands.write_info")
    def test_generate_command_install_option(
        self, mock_write_info, mock_os_path_isfile, mock_file
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_INSTALL_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False

        generate_command(args=mock_args)

        rts_call_args = mock_write_info.call_args_list[0]
        self.assertIn("Please review the generated install.yml", rts_call_args.args[0])

        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()

    @mock.patch("tethys_cli.gen_commands.run")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    @mock.patch("tethys_cli.gen_commands.write_warning")
    @mock.patch("tethys_cli.gen_commands.write_info")
    def test_generate_requirements_option(
        self, mock_write_info, mock_write_warn, mock_os_path_isfile, mock_file, mock_run
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_REQUIREMENTS_OPTION
        mock_args.directory = None
        mock_os_path_isfile.return_value = False

        generate_command(args=mock_args)

        mock_write_warn.assert_called_once()
        mock_write_info.assert_called_once()
        mock_os_path_isfile.assert_called_once()
        mock_file.assert_called()
        mock_run.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.os.path.join")
    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.Template")
    @mock.patch("tethys_cli.gen_commands.safe_load")
    @mock.patch("tethys_cli.gen_commands.run_command")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    @mock.patch("tethys_cli.gen_commands.os.path.isfile")
    @mock.patch("tethys_cli.gen_commands.print")
    def test_generate_command_metayaml(
        self,
        mock_print,
        mock_os_path_isfile,
        mock_file,
        mock_run_command,
        mock_load,
        mock_Template,
        _,
        mock_os_path_join,
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_META_YAML_OPTION
        mock_args.directory = None
        mock_args.pin_level = "minor"
        mock_os_path_isfile.return_value = False
        mock_os_path_join.return_value = f"{TETHYS_SRC}/conda.recipe"
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3                     py37_0    conda-forge\n"
            "bar                       4.5.6                     py37h516909a_0    conda-forge\n"
            "goo                       7.8                       py37h516909a_0    conda-forge\n"
        )
        mock_run_command.return_value = (stdout, "", 0)
        mock_load.return_value = {"dependencies": ["foo", "bar=4.5", "goo"]}
        mock_Template().render.return_value = "out"
        generate_command(args=mock_args)

        mock_run_command.assert_any_call("list", "foo")
        mock_run_command.assert_any_call("list", "goo")

        mock_print.assert_not_called()

        render_context = mock_Template().render.call_args.args[0]
        expected_context = {
            "run_requirements": ["foo=1.2.*", "bar=4.5", "goo=7.8"],
            "tethys_version": mock.ANY,
        }
        self.assertDictEqual(expected_context, render_context)
        mock_file.assert_called()
        mock_os_path_join.assert_called()

    @mock.patch("tethys_cli.gen_commands.write_info")
    @mock.patch("tethys_cli.gen_commands.derive_version_from_conda_environment")
    @mock.patch("tethys_cli.gen_commands.safe_load")
    @mock.patch("tethys_cli.gen_commands.open", new_callable=mock.mock_open)
    def test_gen_meta_yaml_overriding_dependencies(
        self, _, mock_load, mock_dvfce, mock_write_info
    ):
        mock_args = mock.MagicMock()
        mock_args.type = GEN_META_YAML_OPTION
        mock_args.directory = None
        mock_args.pin_level = "minor"

        mock_load.return_value = {
            "dependencies": [
                "foo",
                "foo=1.2.3",
                "foo>=1.2.3",
                "foo<=1.2.3",
                "foo>1.2.3",
                "foo<1.2.3",
            ]
        }

        ret = gen_meta_yaml(mock_args)

        self.assertEqual(1, mock_dvfce.call_count)
        mock_dvfce.assert_called_with("foo", level="minor")

        expected_context = {
            "run_requirements": [
                mock_dvfce(),
                "foo=1.2.3",
                "foo>=1.2.3",
                "foo<=1.2.3",
                "foo>1.2.3",
                "foo<1.2.3",
            ],
            "tethys_version": mock.ANY,
        }
        self.assertDictEqual(expected_context, ret)

    @mock.patch("tethys_cli.gen_commands.run_command")
    def test_derive_version_from_conda_environment_minor(self, mock_run_command):
        # More than three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3.4.5                 py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "minor")

        self.assertEqual("foo=1.2.*", ret)

        # Three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3                     py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "minor")

        self.assertEqual("foo=1.2.*", ret)

        # Two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2                       py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "minor")

        self.assertEqual("foo=1.2", ret)

        # Less than two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1                         py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "minor")

        self.assertEqual("foo", ret)

    @mock.patch("tethys_cli.gen_commands.run_command")
    def test_derive_version_from_conda_environment_major(self, mock_run_command):
        # More than three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3.4.5                 py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "major")

        self.assertEqual("foo=1.*", ret)

        # Three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3                     py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "major")

        self.assertEqual("foo=1.*", ret)

        # Two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2                       py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "major")

        self.assertEqual("foo=1.*", ret)

        # Less than two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1                         py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "major")

        self.assertEqual("foo=1", ret)

    @mock.patch("tethys_cli.gen_commands.run_command")
    def test_derive_version_from_conda_environment_patch(self, mock_run_command):
        # More than three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3.4.5                 py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "patch")

        self.assertEqual("foo=1.2.3.*", ret)

        # Three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3                     py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "patch")

        self.assertEqual("foo=1.2.3", ret)

        # Two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2                       py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "patch")

        self.assertEqual("foo=1.2", ret)

        # Less than two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1                         py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "patch")

        self.assertEqual("foo=1", ret)

    @mock.patch("tethys_cli.gen_commands.run_command")
    def test_derive_version_from_conda_environment_none(self, mock_run_command):
        # More than three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3.4.5                 py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "none")

        self.assertEqual("foo", ret)

        # Three version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2.3                     py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "none")

        self.assertEqual("foo", ret)

        # Two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1.2                       py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "none")

        self.assertEqual("foo", ret)

        # Less than two version numbers
        stdout = (
            "# packages in environment at /home/nswain/miniconda/envs/tethys:\n"
            "#\n"
            "# Name                    Version                   Build  Channel\n"
            "foo                       1                         py37_0    conda-forge"
        )
        mock_run_command.return_value = (stdout, "", 0)

        ret = derive_version_from_conda_environment("foo", "none")

        self.assertEqual("foo", ret)

    @mock.patch("tethys_cli.gen_commands.print")
    @mock.patch("tethys_cli.gen_commands.run_command")
    def test_derive_version_from_conda_environment_conda_list_error(
        self, mock_run_command, mock_print
    ):
        # More than three version numbers
        mock_run_command.return_value = ("", "Some error", 1)

        ret = derive_version_from_conda_environment("foo", "minor")

        self.assertEqual("foo", ret)

        rts_call_args_list = mock_print.call_args_list
        self.assertEqual(
            'ERROR: Something went wrong looking up dependency "foo" in environment',
            rts_call_args_list[0].args[0],
        )
        self.assertEqual("Some error", rts_call_args_list[1].args[0])

    def test_gen_vendor_static_files(self):
        context = gen_vendor_static_files(mock.MagicMock())
        for _, v in context.items():
            self.assertIsNotNone(v)

    @mock.patch("tethys_cli.gen_commands.call")
    def test_download_vendor_static_files(self, mock_call):
        download_vendor_static_files(mock.MagicMock())
        mock_call.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.write_error")
    @mock.patch("tethys_cli.gen_commands.call")
    def test_download_vendor_static_files_no_npm(self, mock_call, mock_error):
        mock_call.side_effect = FileNotFoundError
        download_vendor_static_files(mock.MagicMock())
        mock_call.assert_called_once()
        mock_error.assert_called_once()

    @mock.patch.object(tethys_gen_commands, "has_conda")
    @mock.patch("tethys_cli.gen_commands.write_error")
    @mock.patch("tethys_cli.gen_commands.call")
    def test_download_vendor_static_files_no_npm_no_conda(
        self, mock_call, mock_error, mock_has_conda
    ):
        mock_call.side_effect = FileNotFoundError
        mock_has_conda.__bool__ = lambda self: False
        download_vendor_static_files(mock.MagicMock())
        mock_call.assert_called_once()
        mock_error.assert_called_once()

    @mock.patch("tethys_cli.gen_commands.check_for_existing_file")
    @mock.patch("tethys_cli.gen_commands.os.path.isdir", return_value=True)
    def test_get_destination_path_vendor(self, mock_isdir, mock_check_file):

        mock_args = mock.MagicMock(
            type=GEN_PACKAGE_JSON_OPTION,
            directory=False,
        )
        result = get_destination_path(mock_args)
        mock_isdir.assert_called()
        mock_check_file.assert_called_once()
        self.assertEqual(result, f"{TETHYS_SRC}/tethys_portal/static/package.json")

    @mock.patch("tethys_cli.gen_commands.GEN_COMMANDS")
    @mock.patch("tethys_cli.gen_commands.write_path_to_console")
    @mock.patch("tethys_cli.gen_commands.render_template")
    @mock.patch("tethys_cli.gen_commands.get_destination_path")
    def test_generate_commmand_post_process_func(
        self, mock_get_path, mock_render, mock_write_path, mock_commands
    ):
        mock_commands.__getitem__.return_value = (mock.MagicMock(), mock.MagicMock())
        mock_args = mock.MagicMock(
            type="test",
        )
        generate_command(mock_args)
        mock_get_path.assert_called_once_with(mock_args)
        mock_render.assert_called_once()
        mock_write_path.assert_called_once()
        mock_commands.__getitem__.assert_called_once()

    def test_templates_exist(self):
        template_dir = Path(TETHYS_SRC) / "tethys_cli" / "gen_templates"
        for file_name in VALID_GEN_OBJECTS:
            template_path = template_dir / file_name
            self.assertTrue(template_path.exists())
