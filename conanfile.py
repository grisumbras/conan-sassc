import contextlib
from conans import (
    AutoToolsBuildEnvironment,
    ConanFile,
    tools,
)


class LibSassConan(ConanFile):
    name = "sassc"
    description = "A C/C++ implementation of a Sass compiler"
    author = "Dmitry Arkhipov <grisumbras@gmail.com>"
    license = "MIT"
    homepage = "https://sass-lang.com/libsass"
    url = "https://github.com/grisumbras/conan-libsass"
    default_user = "grisumbras"
    default_channel = "testing"

    settings = "arch_build", "os_build", "compiler"

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

    def build(self):
        with self._build_context():
            autotools = AutoToolsBuildEnvironment(self)
            autotools.make()

    def package(self):
        with self._build_context():
            with tools.environment_append({"PREFIX": self.package_folder}):
                autotools = AutoToolsBuildEnvironment(self)
                autotools.install()
        self.copy("LICENSE", src=self._src_subdir,  dst="share/libsass")

    def package_id(self):
        del self.settings.compiler

    @property
    def _os_ext(self):
        return "zip" if self.settings.os_build == "Windows" else "tar.gz"

    @property
    def _src_subdir(self):
        return "sassc-{}".format(self.version)

    @contextlib.contextmanager
    def _build_context(self):
        env = {"SASS_LIBSASS_PATH": self.deps_cpp_info["libsass"].rootpath}
        with tools.environment_append(env):
            with tools.chdir(self._src_subdir):
                yield
