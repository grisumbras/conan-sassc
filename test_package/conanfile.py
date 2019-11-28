from conans import (
    ConanFile,
    python_requires,
)

b2 = python_requires("b2-helper/0.7.1@grisumbras/stable")

@b2.build_with_b2
class SasscTestConan(ConanFile):
    exports_sources = "build.jam", "*.scss"

    def b2_setup_builder(self, builder):
        builder.using("sass")
        return builder
