import os
import contextlib
from conans import (
    AutoToolsBuildEnvironment,
    ConanFile,
    tools,
)


class SasscConan(ConanFile):
    name = "sassc"
    description = "libsass command line driver"
    author = "Dmitry Arkhipov <grisumbras@gmail.com>"
    license = "MIT"
    homepage = "https://sass-lang.com/libsass"
    url = "https://github.com/grisumbras/conan-sassc"
    default_user = "grisumbras"
    default_channel = "testing"

    settings = "arch_build", "os_build", "compiler"
    exports = "LICENSE", "*.patch"

    def requirements(self):
        self.requires("libsass/{version}@{user}/{channel}".format(
            version=self.version,
            user=self.user,
            channel=self.channel,
        ))

    def source(self):
        url = "https://github.com/sass/sassc/archive/{version}.{ext}".format(
            version=self.version,
            ext=self._os_ext,
        )
        tools.get(url)
        tools.patch(
            base_path=self._src_subdir, patch_file="make.patch", strip=1
        )

    def build(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make(vars=self._fixed_vars(autotools))

    def package(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            autotools.install(vars=self._fixed_vars(autotools))
        self.copy("LICENSE", src=self._src_subdir, dst="share/sassc")

    def package_id(self):
        del self.settings.compiler

    def package_info(self):
        self.env_info.PATH = [os.path.join(self.package_folder, "bin")]

    @property
    def _os_ext(self):
        return "zip" if self.settings.os_build == "Windows" else "tar.gz"

    @property
    def _src_subdir(self):
        return "sassc-{}".format(self.version)

    def _fixed_vars(self, autotools):
        vars = autotools.vars
        for var in ["CXXFLAGS", "CFLAGS"]:
            vars[var] += " " + vars["CPPFLAGS"]
        return vars

    @contextlib.contextmanager
    def _build_context(self):
        if self.options["libsass"].shared:
            libsass_build_type = "shared"
        else:
            libsass_build_type = "static"
        env = {
            "PREFIX": self.package_folder,
            "SASS_LIBSASS_PATH": self.deps_cpp_info["libsass"].rootpath,
            "BUILD": libsass_build_type
        }
        with tools.environment_append(env):
            with tools.chdir(self._src_subdir):
                yield
