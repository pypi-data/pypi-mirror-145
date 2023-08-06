#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from labstep.entities.molecule.model import Molecule
import labstep.generic.entity.repository as entityRepository
from labstep.constants import UNSPECIFIED


def getMolecule(user, guid, extraParams={}):
    return entityRepository.getEntity(user, Molecule, guid, extraParams)


def editMolecule(molecule, name=UNSPECIFIED, data=UNSPECIFIED, inchis=UNSPECIFIED, extraParams={}):
    params = {
        "name": name,
        "data": data,
        "inchis": inchis,
        **extraParams,
    }
    return entityRepository.editEntity(molecule, params)


def newMolecule(user, extraParams={}):
    params = {
        "name": 'Untitled',
        **extraParams,
    }

    return entityRepository.newEntity(user, Molecule, params)
