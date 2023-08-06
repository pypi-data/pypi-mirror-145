#!/usr/bin/env python3
import numpy as np
import json


class calibration_object:
    """
    Object to store calibration within km3compass
    """

    TO_DICT_ATTR = {
        "AHRS_Firmware_Version": {"Unit": "", "default": ["CLB"]},
        "AHRS_Kalman_Filter_Enable": {"Unit": "", "default": ["False"]},
        "AHRS_Magnetic_Declination": {"Unit": "deg", "default": ["0.0"]},
        "AHRS_Acceleration_Gain": {"Unit": "", "default": np.full(3, 1e-3)},
        "AHRS_Acceleration_Offset": {"Unit": "g/ms^2", "attr": "_A_offsets"},
        "AHRS_Acceleration_Rotation": {"Unit": "", "attr": "_A_rot"},
        "AHRS_Gyroscope_Gain": {"Unit": "", "default": np.full(3, 8.66)},
        "AHRS_Gyroscope_Rotation": {"Unit": "", "attr": "_G_rot"},
        "AHRS_Magnetic_Rotation": {"Unit": "", "attr": "_H_rot"},
        "AHRS_Matrix_Column": {
            "Unit": "",
            "default": ["0", "1", "2", "0", "1", "2", "0", "1", "2"],
        },
        "AHRS_Matrix_Row": {
            "Unit": "",
            "default": ["0", "0", "0", "1", "1", "1", "2", "2", "2"],
        },
        "AHRS_Vector_Index": {"Unit": "", "default": ["0", "1", "2"]},
        "AHRS_Magnetic_XMin": {"Unit": "G", "attr": "get_H_xmin"},
        "AHRS_Magnetic_XMax": {"Unit": "G", "attr": "get_H_xmax"},
        "AHRS_Magnetic_YMin": {"Unit": "G", "attr": "get_H_ymin"},
        "AHRS_Magnetic_YMax": {"Unit": "G", "attr": "get_H_ymax"},
        "AHRS_Magnetic_ZMin": {"Unit": "G", "attr": "get_H_zmin"},
        "AHRS_Magnetic_ZMax": {"Unit": "G", "attr": "get_H_zmax"},
    }

    def __init__(self, **kwargs):
        self._compass_SN = 0
        self._compass_UPI = "3.4.3.4/DUMMY/X.YY"
        self._type = "default"
        self._source = "new"

        # Accelerometer related values
        self._A_norm = 1.0
        self._A_offsets = np.ones(3)
        self._A_rot = np.identity(3)

        # Compass related values
        self._H_norm = 1.0
        self._H_offsets = np.ones(3)
        self._H_rot = np.identity(3)

        # Gyroscope related values
        self._G_norm = 1.0
        self._G_offsets = np.ones(3)
        self._G_rot = np.identity(3)

        self._parent = None

        for key, item in kwargs.items():
            self.set(key, item)

    def set(self, key, value):
        """Generic function to set a calibration value"""
        if not hasattr(self, f"_{key}"):
            raise Exception(
                f'Try to set property "{key}" to calibration, which doesn\'t exist !'
            )
        setattr(self, f"_{key}", value)

    def get(self, key):
        """Generic function to get a calibration value"""
        if not hasattr(self, f"_{key}"):
            raise Exception(
                f'Try to sget property "{key}" from calibration, which doesn\'t exist !'
            )
        return getattr(self, f"_{key}")

    @property
    def get_H_xmin(self):
        return self._H_offsets[0] - 1.0

    @property
    def get_H_xmax(self):
        return self._H_offsets[0] + 1.0

    @property
    def get_H_ymin(self):
        return self._H_offsets[1] - 1.0

    @property
    def get_H_ymax(self):
        return self._H_offsets[1] + 1.0

    @property
    def get_H_zmin(self):
        return self._H_offsets[2] - 1.0

    @property
    def get_H_zmax(self):
        return self._H_offsets[2] + 1.0

    def __str__(self):
        """Produce str summary of calibration object"""
        output = "-" * 40 + "\n"
        output += f"Calibration for compass {self._compass_SN}\n"
        output += f'Type: "{self._type}", source: "{self._source}"\n'
        output += f"A norm = {self._A_norm}\n"
        output += f"A xyz offsets = {self._A_offsets}\n"
        output += f"A rotation matrix = \n{self._A_rot}\n"
        output += f"H norm = {self._H_norm}\n"
        output += f"H xyz offsets = {self._H_offsets}\n"
        output += f"H rotation matrix = \n{self._H_rot}\n"
        output += "-" * 40
        return output

    def to_dict(self):
        """Cast calibration data to dict object"""
        testParameters = []
        for key, item in self.TO_DICT_ATTR.items():
            d = {"Name": key, "Unit": item["Unit"]}
            value = None
            if "attr" in item:
                value = getattr(self, item["attr"])
            elif "default" in item:
                value = item["default"]
            if isinstance(value, np.ndarray):
                value = list(value.flatten())
            d["Values"] = value
            testParameters.append(d)
        calib_dict = {
            "TestType": self._type,
            "TestResult": "OK",
            "UPI": self._compass_UPI,
            "TestParameters": testParameters,
        }
        return calib_dict

    def to_json(self, filename=None):
        """
        Export the calibration to a json string
        If a filename is provided, dump it to file too.
        """

        calib = self.to_dict()
        json_str = json.dumps(calib)

        if filename is not None:
            with open(filename, "w") as json_file:
                json.dump(calib, json_file)

        return json_str
