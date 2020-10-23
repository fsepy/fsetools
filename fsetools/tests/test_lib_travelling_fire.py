# -*- coding: utf-8 -*-

from fsetools.lib.fse_travelling_fire import _test_fire as test_fire_travelling
from fsetools.lib.fse_travelling_fire import _test_fire_backup as test_fire_travelling_backup
from fsetools.lib.fse_travelling_fire import _test_fire_multiple_beam_location as test_fire_travelling_multiple
from fsetools.lib.fse_travelling_fire_flux import _test_fire as test_fire_travelling_flux

test_fire_travelling()
test_fire_travelling_backup()
test_fire_travelling_multiple()
test_fire_travelling_flux()
