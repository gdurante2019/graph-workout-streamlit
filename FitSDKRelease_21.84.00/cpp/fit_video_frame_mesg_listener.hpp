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


#if !defined(FIT_VIDEO_FRAME_MESG_LISTENER_HPP)
#define FIT_VIDEO_FRAME_MESG_LISTENER_HPP

#include "fit_video_frame_mesg.hpp"

namespace fit
{

class VideoFrameMesgListener
{
public:
    virtual ~VideoFrameMesgListener() {}
    virtual void OnMesg(VideoFrameMesg& mesg) = 0;
};

} // namespace fit

#endif // !defined(FIT_VIDEO_FRAME_MESG_LISTENER_HPP)
