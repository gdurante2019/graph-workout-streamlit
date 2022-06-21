///////////////////////////////////////////////////////////////////////////////////
// The following FIT Protocol software provided may be used with FIT protocol
// devices only and remains the copyrighted property of Garmin International, Inc.
// The software is being provided on an "as-is" basis and as an accommodation,
// and therefore all warranties, representations, or guarantees of any kind
// (whether express, implied or statutory) including, without limitation,
// warranties of merchantability, non-infringement, or fitness for a particular
// purpose, are specifically disclaimed.
//
// Copyright 2022 Garmin International, Inc.
///////////////////////////////////////////////////////////////////////////////////
// ****WARNING****  This file is auto-generated!  Do NOT edit this file.
// Profile Version = 21.84Release
// Tag = production/akw/21.84.00-0-g894a113c
///////////////////////////////////////////////////////////////////////////////////


package com.garmin.fit;


public enum File  {
    DEVICE((short)1),
    SETTINGS((short)2),
    SPORT((short)3),
    ACTIVITY((short)4),
    WORKOUT((short)5),
    COURSE((short)6),
    SCHEDULES((short)7),
    WEIGHT((short)9),
    TOTALS((short)10),
    GOALS((short)11),
    BLOOD_PRESSURE((short)14),
    MONITORING_A((short)15),
    ACTIVITY_SUMMARY((short)20),
    MONITORING_DAILY((short)28),
    MONITORING_B((short)32),
    SEGMENT((short)34),
    SEGMENT_LIST((short)35),
    EXD_CONFIGURATION((short)40),
    MFG_RANGE_MIN((short)0xF7),
    MFG_RANGE_MAX((short)0xFE),
    INVALID((short)255);

    protected short value;

    private File(short value) {
        this.value = value;
    }

    public static File getByValue(final Short value) {
        for (final File type : File.values()) {
            if (value == type.value)
                return type;
        }

        return File.INVALID;
    }

    /**
     * Retrieves the String Representation of the Value
     * @return The string representation of the value
     */
    public static String getStringFromValue( File value ) {
        return value.name();
    }

    public short getValue() {
        return value;
    }


}
