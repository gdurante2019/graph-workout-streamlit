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


public enum AntNetwork  {
    PUBLIC((short)0),
    ANTPLUS((short)1),
    ANTFS((short)2),
    PRIVATE((short)3),
    INVALID((short)255);

    protected short value;

    private AntNetwork(short value) {
        this.value = value;
    }

    public static AntNetwork getByValue(final Short value) {
        for (final AntNetwork type : AntNetwork.values()) {
            if (value == type.value)
                return type;
        }

        return AntNetwork.INVALID;
    }

    /**
     * Retrieves the String Representation of the Value
     * @return The string representation of the value
     */
    public static String getStringFromValue( AntNetwork value ) {
        return value.name();
    }

    public short getValue() {
        return value;
    }


}
