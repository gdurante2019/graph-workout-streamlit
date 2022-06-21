#region Copyright
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

#endregion

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.IO;
using System.Linq;

namespace Dynastream.Fit
{
    /// <summary>
    /// Implements the Jump profile message.
    /// </summary>
    public class JumpMesg : Mesg
    {
        #region Fields
        #endregion

        /// <summary>
        /// Field Numbers for <see cref="JumpMesg"/>
        /// </summary>
        public sealed class FieldDefNum
        {
            public const byte Timestamp = 253;
            public const byte Distance = 0;
            public const byte Height = 1;
            public const byte Rotations = 2;
            public const byte HangTime = 3;
            public const byte Score = 4;
            public const byte PositionLat = 5;
            public const byte PositionLong = 6;
            public const byte Speed = 7;
            public const byte EnhancedSpeed = 8;
            public const byte Invalid = Fit.FieldNumInvalid;
        }

        #region Constructors
        public JumpMesg() : base(Profile.GetMesg(MesgNum.Jump))
        {
        }

        public JumpMesg(Mesg mesg) : base(mesg)
        {
        }
        #endregion // Constructors

        #region Methods
        ///<summary>
        /// Retrieves the Timestamp field
        /// Units: s</summary>
        /// <returns>Returns DateTime representing the Timestamp field</returns>
        public DateTime GetTimestamp()
        {
            Object val = GetFieldValue(253, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return TimestampToDateTime(Convert.ToUInt32(val));
            
        }

        /// <summary>
        /// Set Timestamp field
        /// Units: s</summary>
        /// <param name="timestamp_">Nullable field value to be set</param>
        public void SetTimestamp(DateTime timestamp_)
        {
            SetFieldValue(253, 0, timestamp_.GetTimeStamp(), Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the Distance field
        /// Units: m</summary>
        /// <returns>Returns nullable float representing the Distance field</returns>
        public float? GetDistance()
        {
            Object val = GetFieldValue(0, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set Distance field
        /// Units: m</summary>
        /// <param name="distance_">Nullable field value to be set</param>
        public void SetDistance(float? distance_)
        {
            SetFieldValue(0, 0, distance_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the Height field
        /// Units: m</summary>
        /// <returns>Returns nullable float representing the Height field</returns>
        public float? GetHeight()
        {
            Object val = GetFieldValue(1, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set Height field
        /// Units: m</summary>
        /// <param name="height_">Nullable field value to be set</param>
        public void SetHeight(float? height_)
        {
            SetFieldValue(1, 0, height_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the Rotations field</summary>
        /// <returns>Returns nullable byte representing the Rotations field</returns>
        public byte? GetRotations()
        {
            Object val = GetFieldValue(2, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToByte(val));
            
        }

        /// <summary>
        /// Set Rotations field</summary>
        /// <param name="rotations_">Nullable field value to be set</param>
        public void SetRotations(byte? rotations_)
        {
            SetFieldValue(2, 0, rotations_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the HangTime field
        /// Units: s</summary>
        /// <returns>Returns nullable float representing the HangTime field</returns>
        public float? GetHangTime()
        {
            Object val = GetFieldValue(3, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set HangTime field
        /// Units: s</summary>
        /// <param name="hangTime_">Nullable field value to be set</param>
        public void SetHangTime(float? hangTime_)
        {
            SetFieldValue(3, 0, hangTime_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the Score field
        /// Comment: A score for a jump calculated based on hang time, rotations, and distance.</summary>
        /// <returns>Returns nullable float representing the Score field</returns>
        public float? GetScore()
        {
            Object val = GetFieldValue(4, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set Score field
        /// Comment: A score for a jump calculated based on hang time, rotations, and distance.</summary>
        /// <param name="score_">Nullable field value to be set</param>
        public void SetScore(float? score_)
        {
            SetFieldValue(4, 0, score_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the PositionLat field
        /// Units: semicircles</summary>
        /// <returns>Returns nullable int representing the PositionLat field</returns>
        public int? GetPositionLat()
        {
            Object val = GetFieldValue(5, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToInt32(val));
            
        }

        /// <summary>
        /// Set PositionLat field
        /// Units: semicircles</summary>
        /// <param name="positionLat_">Nullable field value to be set</param>
        public void SetPositionLat(int? positionLat_)
        {
            SetFieldValue(5, 0, positionLat_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the PositionLong field
        /// Units: semicircles</summary>
        /// <returns>Returns nullable int representing the PositionLong field</returns>
        public int? GetPositionLong()
        {
            Object val = GetFieldValue(6, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToInt32(val));
            
        }

        /// <summary>
        /// Set PositionLong field
        /// Units: semicircles</summary>
        /// <param name="positionLong_">Nullable field value to be set</param>
        public void SetPositionLong(int? positionLong_)
        {
            SetFieldValue(6, 0, positionLong_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the Speed field
        /// Units: m/s</summary>
        /// <returns>Returns nullable float representing the Speed field</returns>
        public float? GetSpeed()
        {
            Object val = GetFieldValue(7, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set Speed field
        /// Units: m/s</summary>
        /// <param name="speed_">Nullable field value to be set</param>
        public void SetSpeed(float? speed_)
        {
            SetFieldValue(7, 0, speed_, Fit.SubfieldIndexMainField);
        }
        
        ///<summary>
        /// Retrieves the EnhancedSpeed field
        /// Units: m/s</summary>
        /// <returns>Returns nullable float representing the EnhancedSpeed field</returns>
        public float? GetEnhancedSpeed()
        {
            Object val = GetFieldValue(8, 0, Fit.SubfieldIndexMainField);
            if(val == null)
            {
                return null;
            }

            return (Convert.ToSingle(val));
            
        }

        /// <summary>
        /// Set EnhancedSpeed field
        /// Units: m/s</summary>
        /// <param name="enhancedSpeed_">Nullable field value to be set</param>
        public void SetEnhancedSpeed(float? enhancedSpeed_)
        {
            SetFieldValue(8, 0, enhancedSpeed_, Fit.SubfieldIndexMainField);
        }
        
        #endregion // Methods
    } // Class
} // namespace