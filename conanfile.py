#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: Conan is supported on a best-effort basis. Abseil doesn't use Conan
# internally, so we won't know if it stops working. We may ask community
# members to help us debug any problems that arise.

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
from conans.model.version import Version


class AbseilConan(ConanFile):
    name = "abseil"
    url = "https://github.com/abseil/abseil-cpp"
    homepage = url
    author = "Abseil <abseil-io@googlegroups.com>"
    description = "Abseil Common Libraries (C++) from Google"
    license = "Apache-2.0"
    topics = ("conan", "abseil", "abseil-cpp", "google", "common-libraries")
    exports = ["LICENSE"]
    exports_sources = ["CMakeLists.txt", "CMake/*", "absl/*"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    def configure(self):
        if self.settings.os == "Windows" and \
           self.settings.compiler == "Visual Studio" and \
           Version(self.settings.compiler.version.value) < "14":
            raise ConanInvalidConfiguration("Abseil does not support MSVC < 14")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["-Wl,--start-group"]
        self.cpp_info.libs.extend(tools.collect_libs(self))
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["-Wl,--end-group", "pthread"])
