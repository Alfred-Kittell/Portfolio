using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SoundMasta
{
    class MicrophoneBase
    {
        /// <summary>
        /// Имя устройства
        /// </summary>
        public readonly string name;

        /// <summary>
        /// Дискретность аудио карты (или хз)
        /// </summary>
        public readonly int rate;

        // 
        private int fileCurrRecors;

        // 
        private int fileMaxRecors;

    }



    /// <summary>
    /// Настройки соединения с микрофоном
    /// </summary>
    class ConnectOption
    {
        public MicrophonType Type { get; set; } = MicrophonType.Local;

        public int AudioDevice { get; set; } = 0;

        public Uri Uri { get; set; } = null;

        public int Rate { get; set; } = 44000;

        public int BufferSize { get; set; } = 4096;

        public double Volume { get; set; } = 200;

        public string OutPath { get; set; } = null;

        public int OutBufferSize { get; set; } = 10;

        public EventHandler<EventDataAvalible> onDataAvalible { get; set; } = null;


    }


    /// <summary>
    /// 
    /// </summary>
    enum MicrophonType
    {
        Local = 1,
        RTSP
    }

    class EventDataAvalible : EventArgs
    {
        public double[] BuffVal { get; }
        public double[] BuffMs { get; }

        //public EventDataAvalible(double[] buffval, double[] buffmsec)
        public EventDataAvalible(double[] buffval)
        {
            BuffVal = new double[buffval.Length];
            buffval.CopyTo(BuffVal, 0);

            //BuffMs = new double[buffmsec.Length];
            //buffmsec.CopyTo(BuffMs, 0);
        }
    }



}
