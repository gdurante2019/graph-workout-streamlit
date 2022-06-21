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


import XCTest

import FITTests
import ActivityEncodeTests
import DecodeEasyMethodTests
import SwiftDecoderTests

var tests = [XCTestCaseEntry]()
tests += FITTests.allTests()
tests += FITDateTests.allTests()
tests += ActivityEncode.allTests()
tests += DecodeEasyMethodTests.allTests()
tests += SwiftDecoderTests.allTests()
XCTMain(tests)
