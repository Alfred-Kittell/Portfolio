using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using NAudio.Wave;

namespace SoundMasta
{
    /// <summary>
    /// Класс для управления локальным микрофоном
    /// </summary>
    class MicrophoneLocal
    {
        /// <summary>
        /// Класс для подключение к микрофону
        /// </summary>
        private WaveIn waveIn;

        /// <summary>
        /// Класс для записи
        /// </summary>
        private WaveFileWriter writer;

        // 
        private int fileCurrRecors;

        // 
        private int fileMaxRecors;


        /// <summary>
        /// Готовность фрейма
        /// </summary>
        public event EventHandler<EventDataAvalible> onDataAvalible;

        /// <summary>
        /// Дискретность аудио карты (или хз)
        /// </summary>
        public readonly int rate;

        /// <summary>
        /// Размер буфера (2^n)
        /// </summary>
        public readonly int bufferSize;

        /// <summary>
        /// Громкость поступающего сигнала
        /// </summary>
        public double volume = 200;



        /// <summary>
        /// Базовый Конструктор
        /// </summary>
        /// <param name="audioDevice"></param>
        /// <param name="rate"></param>
        /// <param name="bufferSize"></param>
        public MicrophoneLocal(ConnectOption conOpt)
        {
            rate = conOpt.Rate;
            bufferSize = conOpt.BufferSize;

            // настройка класса управляющего микрофон
            waveIn = new WaveIn();
            waveIn.WaveFormat = new WaveFormat(rate, 1);
            waveIn.BufferMilliseconds = (int)((double)bufferSize / rate * 500.0);

            waveIn.DeviceNumber = conOpt.AudioDevice;
            //waveIn.DataAvailable += e;  // обработчик записи, при наличии записываемых данных
            
            // настройка вывода обработанных данных
            if (conOpt.onDataAvalible != null)
            {
                waveIn.DataAvailable += DataAvailable;  
                onDataAvalible += conOpt.onDataAvalible;
            }

            waveIn.RecordingStopped += RecordingStopped; // обработчик остановки


            // настройка записи в файл
            if (conOpt.OutPath != null)
            {
                fileCurrRecors = 0;
                fileMaxRecors = conOpt.OutBufferSize;
                writer = new WaveFileWriter(conOpt.OutPath, waveIn.WaveFormat);
                waveIn.DataAvailable += Write_buffer;
            }



        }

        public void SetOutputFile(string path, int bufferSize = 4096)
        {
            
        }

        /// <summary>
        /// Начать прослуживать микрофон
        /// </summary>
        /// <param name="e"></param>
        /// <param name="audioDevice"></param>
        /// <param name="outPath"></param>
        public void StartRecording()
        {


            // Начало записи
            waveIn.StartRecording();
        }

        /// <summary>
        /// Закончить прослуживать микрофон
        /// </summary>
        public void StopRecord()
        {
            // Завершаем запись
            if (waveIn != null)
            {
                waveIn.StopRecording();

            }
        }

        /// <summary>
        /// Обработчик поступающих сырых аудио данных в формате PCM 16 bit
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void DataAvailable(object sender, WaveInEventArgs e)
        {
            // выход, если нет данных
            if (e.Buffer.Length == 0)
                return;

            // подготовка к декодированию сырых данных
            var audioBytes = new byte[bufferSize];
            e.Buffer.CopyTo(audioBytes, 0);
            int BYTES_PER_POINT = 2; // число байт на аудио точку
            var inData = new double[bufferSize / BYTES_PER_POINT];

            // декодирование двоичных сырых данных
            for (int i = 0; i < inData.Length; i++)
            {
                short val = BitConverter.ToInt16(audioBytes, i * 2);
                inData[i] = val / Math.Pow(2, 16) * volume;
            }

            // создаём событие готовности фрейма
            onDataAvalible(this, new EventDataAvalible(inData));
        }

        /// <summary>
        /// Запись в файл
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Write_buffer(object sender, WaveInEventArgs e)
        {
            // запись в файл
            writer.WriteData(e.Buffer, 0, e.BytesRecorded);

            // проверка на конец записи
            fileCurrRecors++;
            if (fileCurrRecors > fileMaxRecors)
            {
                waveIn.DataAvailable -= Write_buffer;
                writer.Close();
                writer = null;
            }
        }


        /// <summary>
        /// Освобождение ресурсов после остановки
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void RecordingStopped(object sender, EventArgs e)
        {
            if (waveIn != null)
            {
                waveIn.Dispose();
                waveIn = null;
            }
            
            if (writer != null)
            {
                writer.Close();
                writer = null;
            }
        }

    }

}


///// <summary>
///// Класс для управления локальным микрофоном
///// </summary>
//class MicrophoneLocal
//{
//    /// <summary>
//    /// Класс для подключение к микрофону
//    /// </summary>
//    private WaveIn waveIn;

//    /// <summary>
//    /// Класс для записи
//    /// </summary>
//    private WaveFileWriter writer;

//    /// <summary>
//    /// Класс управления буффером
//    /// </summary>
//    public BufferedWaveProvider bwp;

//    ///// <summary>
//    ///// Дискретность аудио карты (или хз)
//    ///// </summary>
//    //private readonly int rate;

//    ///// <summary>
//    ///// Размер буфера (2^n)
//    ///// </summary>
//    //private readonly int bufferSize;


//    /// <summary>
//    /// Базовый Конструктор
//    /// </summary>
//    /// <param name="audioDevice"></param>
//    /// <param name="rate"></param>
//    /// <param name="bufferSize"></param>
//    public MicrophoneLocal(EventHandler<WaveInEventArgs> e, int audioDevice = 0,
//                           int rate = 44000, int bufferSize = 4096)
//    {
//        //rate = Rate;
//        //bufferSize = BufferSize;

//        // настройки класса управляющего микрофоном
//        waveIn = new WaveIn();
//        waveIn.DeviceNumber = audioDevice;
//        waveIn.DataAvailable += e;  // обработчик записи, при наличии записываемых данных
//        waveIn.RecordingStopped += RecordingStopped; // обработчик остановки
//        waveIn.WaveFormat = new WaveFormat(rate, 1);
//        //waveIn.BufferMilliseconds = (int)((double)bufferSize / rate * 1000.0 / 2);
//        waveIn.BufferMilliseconds = (int)((double)bufferSize / rate * 500.0);

//        // настройка класса управляющего буфером
//        bwp = new BufferedWaveProvider(waveIn.WaveFormat);
//        bwp.BufferLength = bufferSize * 2;
//        bwp.DiscardOnBufferOverflow = true;
//    }


//    public void SetOutputFile(string path, int bufferSize = 4096)
//    {
//        writer = new WaveFileWriter(path, waveIn.WaveFormat);
//        waveIn.DataAvailable += Write_buffer;
//    }

//    /// <summary>
//    /// Начать прослуживать микрофон
//    /// </summary>
//    /// <param name="e"></param>
//    /// <param name="audioDevice"></param>
//    /// <param name="outPath"></param>
//    public void StartRecording()
//    {
//        // Начало записи
//        waveIn.StartRecording();
//    }

//    /// <summary>
//    /// Закончить прослуживать микрофон
//    /// </summary>
//    public void StopRecord()
//    {
//        // Завершаем запись
//        if (waveIn != null)
//        {
//            waveIn.StopRecording();

//        }
//    }


//    private void Write_buffer(object sender, WaveInEventArgs e)
//    {
//        writer.WriteData(e.Buffer, 0, e.BytesRecorded);
//    }


//    /// <summary>
//    /// Освобождение ресурсов после остановки
//    /// </summary>
//    /// <param name="sender"></param>
//    /// <param name="e"></param>
//    private void RecordingStopped(object sender, EventArgs e)
//    {
//        if (waveIn != null)
//        {
//            waveIn.Dispose();
//            waveIn = null;
//        }

//        if (writer != null)
//        {
//            writer.Close();
//            writer = null;
//        }
//    }

//}



