using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

using NAudio.Wave;
using NAudio.FileFormats;
using NAudio.CoreAudioApi;
using NAudio;

using OxyPlot;
using OxyPlot.Axes;
using OxyPlot.Series;
using Microsoft.SqlServer.Server;

using System.Runtime.Serialization.Formatters.Binary;
using System.Numerics;
using Accord.Math;
using Microsoft.VisualBasic.ApplicationServices;
using SoundMasta.Forms;
using System.Linq.Expressions;
using RtspClientSharp.RawFrames;
using RtspClientSharp.Rtsp;
using RtspClientSharp;
using System.Threading;
using System.Net;

namespace SoundMasta
{
    public partial class MainForm : Form
    {
        string demo_path = "..//демки//";

        private int rate = 48000; // sample rate of the sound card 
        private int bufferSize = (int)Math.Pow(2, 12); // must be a multiple of 2 | 2^n -> n max 16

        MicrophoneLocal micro;

        Demo demo;

        bool microRead = false;
        bool demoRecord = false;
        bool demoLoad = false;

        double[] scaleBuf = new double[] { 1.05, -0.05, 1.05, 0, 1.05, -0.05 };

        List<Form> forms = new List<Form>();
        SampleForm sampleForm;
        FFTAmplForm fftAmplForm;
        FFTPhaseForm fftPhaseForm;
        FFTGuillotForm fftGuillotForm;
        SpectrogramForm spectrogramForm;
        List<SplitContainer> spliters = new List<SplitContainer>();

        double[] workSpace;
        double workStep;
        double workDiscr;
        int workSize;

        List<double[]> funcs = new List<double[]>();

        public MainForm()
        {
            InitializeComponent();

            GeneratorVisible_Click(null, null);
            //micro_2 = new MicrophoneControl(rate, bufferSize, "имя_файла.wav");
        }

        // #####################################################

        // Подключение к микрофону
        private void Micro_Connect_Click(object sender, EventArgs e)
        {
            try
            {
                if (!microRead)
                {
                    // 
                    bufferSize = (int)Math.Pow(2, (int)nud_record_buf.Value);
                    int buffMsec = (int)((double)bufferSize / rate * 500.0); // 42
                    double fftPointSpacingHz = (double)buffMsec / (bufferSize/2);

                    // 
                    Create_WorkSpace(bufferSize / 2, fftPointSpacingHz);


                    ConnectOption testConnect = new ConnectOption()
                    {
                        Type = MicrophonType.Local,
                        AudioDevice = (int)nud_device.Value,
                        Rate = rate,
                        BufferSize = bufferSize,
                        OutPath = "Test.wav",
                        OutBufferSize = 100,
                        onDataAvalible = DataAvailable
                    };

                    // настройки микрофона
                    micro = new MicrophoneLocal(testConnect);
                    micro.StartRecording();

                    // настройка интерфейса
                    butt_micro_connect.BackColor = Color.Red;
                    butt_micro_connect.Text = "Отключить";
                    microRead = true;
                }
                else
                {
                    micro.StopRecord();

                    // настройка интерфейса
                    butt_micro_connect.BackColor = Color.Lime;
                    butt_micro_connect.Text = "Поключить";
                    microRead = false;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        // Запись демки
        private void butt_demo_record_Click(object sender, EventArgs e)
        {
            try
            {
                if (!demoRecord)
                {
                    int frameNums = (int)nud_frames_size.Value;
                    label24.Text = "0/" + frameNums;
                    demo = new Demo(frameNums, bufferSize/2, workStep, workDiscr);

                    butt_demo_record.BackColor = Color.Red;
                    butt_demo_record.Text = "Остановить";
                    demoRecord = true;
                }
                else
                {
                    string name = demo_path + tb_demoName_record.Text + ".demo";
                    FileStream serFile = new FileStream(name, FileMode.Create, FileAccess.Write, FileShare.ReadWrite);
                    BinaryFormatter ser = new BinaryFormatter();
                    demo.frameSelect = 0;
                    ser.Serialize(serFile, demo); // сериализуем
                    serFile.Close();

                    butt_demo_record.BackColor = Color.Lime;
                    butt_demo_record.Text = "Запись";
                    demoRecord = false;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        // Загрузка демки
        private void butt_demo_load_Click(object sender, EventArgs e)
        {
            try
            {
                if (!demoLoad)
                {

                    //string name = demo_path + tb_demoName_load.Text + ".demo";
                    string name = demo_path + cb_SelectName.Text + ".demo";

                    FileStream filik = new FileStream(name, FileMode.Open, FileAccess.Read, FileShare.Read);
                    BinaryFormatter binf = new BinaryFormatter();
                    demo = (Demo)binf.Deserialize(filik);
                    demo.frameSelect = 0;
                    filik.Close();

                    Create_WorkSpace(demo.frameSize, demo.step);
                    label30.Text = (demo.step * demo.frameSize) + " ms";
                    label32.Text = (demo.step * demo.frameSize * demo.frameNums) + " ms";

                    butt_demo_load.BackColor = Color.Red;
                    butt_demo_load.Text = "Остановить";
                    demoLoad = true;

                    int frameInd = demo.frameSelect;
                    for (int i = 0; i < workSize; i++)
                    {
                        workSpace[i] = demo.frames[frameInd, i];
                    }

                    label26.Text = string.Format("{0}/{1}", demo.frameSelect + 1, demo.frameNums);
                    Plot_Update();
                }
                else
                {
                    butt_demo_load.BackColor = Color.Lime;
                    butt_demo_load.Text = "Загрузить";
                    demoLoad = false;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        // Получение данных из входного буфера 
        void DataAvailable(object sender, EventDataAvalible e)
        {
            e.BuffVal.CopyTo(workSpace, 0);

            // запись демки
            if (demoRecord)
            {
                int frameInd = demo.frameSelect;
                for (int i = 0; i < workSpace.Length; i++)
                {
                    demo.frames[frameInd, i] = workSpace[i];
                }

                label24.Text = string.Format("{0}/{1}", frameInd+1, demo.frameNums);
                demo.Next();

                // конец записи
                if (demo.frameSelect == 0)
                {
                    butt_demo_record_Click(sender, null);
                }
            }

            Plot_Update();
        }

        // Отобразить предыдущий фрейм в демке
        private void PreviousFrame_Click(object sender, EventArgs e)
        {
            if (timer1.Enabled)
            {
                checkBox1.Checked = false;
            }

            if (demoLoad)
            {
                demo.Previous();
                int frameInd = demo.frameSelect;
                for (int i = 0; i < workSize; i++)
                {
                    workSpace[i] = demo.frames[frameInd, i];
                }

                label26.Text = string.Format("{0}/{1}", demo.frameSelect + 1, demo.frameNums);
                Plot_Update();
            }
        }

        // Отобразить следующий фрейм в демке
        private void NextFrame_Click(object sender, EventArgs e)
        {
            if (timer1.Enabled && sender.GetType().Name != "Timer")
            {
                checkBox1.Checked = false;
            }

            if (demoLoad)
            {
                demo.Next();
                int frameInd = demo.frameSelect;
                for (int i = 0; i < workSize; i++)
                {
                    workSpace[i] = demo.frames[frameInd, i];
                }

                label26.Text = string.Format("{0}/{1}", demo.frameSelect + 1, demo.frameNums);
                Plot_Update();
            }
        }

        // #####################################################

        private void GeneratorVisible_Click(object sender, EventArgs e)
        {
            if (mainGenSplit.Panel2Collapsed)
            {
                mainGenSplit.Panel2Collapsed = false;
                butt_generatorVisible.BackColor = Color.FromKnownColor(KnownColor.LightCyan);
            }
            else
            {
                mainGenSplit.Panel2Collapsed = true;
                butt_generatorVisible.BackColor = Color.FromKnownColor(KnownColor.Control);

            }
        }

        private void AudioVisible_Click(object sender, EventArgs e)
        {
            if (mainAudioSplit.Panel1Collapsed)
            {
                mainAudioSplit.Panel1Collapsed = false;
                butt_audioVisible.BackColor = Color.FromKnownColor(KnownColor.LightCyan);
            }
            else
            {
                mainAudioSplit.Panel1Collapsed = true;
                butt_audioVisible.BackColor = Color.FromKnownColor(KnownColor.Control);

            }
        }

        private void BTT_ShowForm_Click(object sender, EventArgs e)
        {
            Form form = null;
            var s = sender as Button;
            switch(s.Name)
            {
                case "btt_showSample":
                    if (sampleForm == null)
                    {
                        sampleForm = new SampleForm(this);
                        form = sampleForm;
                    }
                    else
                    {
                        s.BackColor = Color.FromKnownColor(KnownColor.Control);
                        forms.Remove(sampleForm);
                        sampleForm.Close();
                        sampleForm = null;
                        CreateSeparators();
                    }
                    break;
                case "btt_showFFTAmpl":
                    if (fftAmplForm == null)
                    {
                        fftAmplForm = new FFTAmplForm(this);
                        form = fftAmplForm;
                    }
                    else
                    {
                        s.BackColor = Color.FromKnownColor(KnownColor.Control);
                        forms.Remove(fftAmplForm);
                        fftAmplForm.Close();
                        fftAmplForm = null;
                        CreateSeparators();
                    }
                    break;
                case "btt_showFFTPhase":
                    if (fftPhaseForm == null)
                    {
                        fftPhaseForm = new FFTPhaseForm(this);
                        form = fftPhaseForm;
                    }
                    else
                    {
                        s.BackColor = Color.FromKnownColor(KnownColor.Control);
                        forms.Remove(fftPhaseForm);
                        fftPhaseForm.Close();
                        fftPhaseForm = null;
                        CreateSeparators();
                    }
                    break;
                case "btt_showFFTGuillot":
                    if (fftGuillotForm == null)
                    {
                        fftGuillotForm = new FFTGuillotForm(this);
                        form = fftGuillotForm;
                    }
                    else
                    {
                        s.BackColor = Color.FromKnownColor(KnownColor.Control);
                        forms.Remove(fftGuillotForm);
                        fftGuillotForm.Close();
                        fftGuillotForm = null;
                        CreateSeparators();
                    }
                    break;
                case "btt_Spectogram":
                    if (spectrogramForm == null)
                    {
                        spectrogramForm = new SpectrogramForm(this);
                        form = spectrogramForm;
                    }
                    else
                    {
                        s.BackColor = Color.FromKnownColor(KnownColor.Control);
                        forms.Remove(spectrogramForm);
                        spectrogramForm.Close();
                        spectrogramForm = null;
                        CreateSeparators();
                    }
                    break;
            }

            if (form != null)
            {
                s.BackColor = Color.FromKnownColor(KnownColor.Bisque);
                form.TopLevel = false;
                form.AutoScroll = true;
                form.Dock = DockStyle.Fill;
                forms.Add(form);
                form.Show();
                CreateSeparators();
            }
        }

        private void CreateSeparators()
        {
            spliters.Clear();
            mainGenSplit.Panel1.Controls.Clear();

            switch (forms.Count)
            {
                case 0: break;
                case 1:
                    {
                        mainGenSplit.Panel1.Controls.Add(forms[0]);
                        break;
                    }
                    
                case 2:
                    {
                        SplitContainer spliter = new SplitContainer() 
                        { 
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        spliters.Add(spliter);
                        mainGenSplit.Panel1.Controls.Add(spliter);
                        spliter.Panel1.Controls.Add(forms[0]);
                        spliter.Panel2.Controls.Add(forms[1]);
                        break;
                    }
                   
                case 3:
                    {
                        SplitContainer spliter_1 = new SplitContainer()
                        {
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        SplitContainer spliter_2 = new SplitContainer()
                        {
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        spliters.Add(spliter_1);
                        spliters.Add(spliter_2);
                        mainGenSplit.Panel1.Controls.Add(spliter_1);
                        spliter_1.Panel2.Controls.Add(spliter_2);
                        spliter_1.Panel1.Controls.Add(forms[0]);
                        spliter_2.Panel1.Controls.Add(forms[1]);
                        spliter_2.Panel2.Controls.Add(forms[2]);
                        break;
                    }
                case 4:
                    {
                        SplitContainer spliter_1 = new SplitContainer()
                        {
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        SplitContainer spliter_2 = new SplitContainer()
                        {
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        SplitContainer spliter_3 = new SplitContainer()
                        {
                            Dock = DockStyle.Fill,
                            Orientation = Orientation.Horizontal,
                            BorderStyle = BorderStyle.Fixed3D
                        };
                        spliters.Add(spliter_1);
                        spliters.Add(spliter_2);
                        spliters.Add(spliter_3);
                        mainGenSplit.Panel1.Controls.Add(spliter_1);
                        spliter_1.Panel1.Controls.Add(spliter_2);
                        spliter_1.Panel2.Controls.Add(spliter_3);
                        spliter_2.Panel1.Controls.Add(forms[0]);
                        spliter_2.Panel2.Controls.Add(forms[1]);
                        spliter_3.Panel1.Controls.Add(forms[2]);
                        spliter_3.Panel2.Controls.Add(forms[3]);
                        break;
                    }
            }
        }

        private void CreateWorkSpace_Click(object sender, EventArgs e)
        {
            groupBox2.Enabled = true;
            funcs.Clear();
            dataFunc.Rows.Clear();
            statusBox.Items.Clear();

            int size = (int)Math.Pow(2, (int)nud_WorkSize.Value);
            double step = (double)nud_WorkStep.Value / 1000; // msec

            Create_WorkSpace(size, step);
            Plot_Update();

            statusBox.Items.Add(string.Format("Созданно: рабочее пространство - точек: {0}", size));
        }

        private void AddFunc_Click(object sender, EventArgs e)
        {
            double A = (double)nud_paramA.Value;
            double omega = (double)nud_paramF.Value;
            double Ph = (double)nud_paramPh.Value;

            double[] Y = Gen_sin(workSize, workStep, A, omega, Ph);

            double int_start = (double)nud_FuncStart.Value;
            double int_end = (double)nud_FuncEnd.Value;

            string param = string.Format("A:{0} | ω:{1} | φ:{2} | Hz:{3}", A, omega, Ph, Math.Round(omega/(2*Math.PI), 2));
            string interval = string.Format("{0} - {1}", int_start, int_end);
            dataFunc.Rows.Add(true, "sin", param, interval);

            funcs.Add(Y);

            for (int i = 0; i < workSize; i++)
            {
                workSpace[i] += Y[i];
            }
            Plot_Update();
        }

        private void CB_SelectName_DropDown(object sender, EventArgs e)
        {
            var f = Directory.GetFiles(demo_path, "*.demo");
            for (int i = 0; i<f.Length; i++)
            {
                //f[i] = f[i].Split('\\').Last().Split('.')[0];
                f[i] = f[i].Split('/').Last().Split('.')[0];
            }

            cb_SelectName.Items.Clear();
            cb_SelectName.Items.AddRange(f);
        }

        private void CB_SelectName_SelectedIndexChanged(object sender, EventArgs e)
        {
            // отключаем воспроизведение, если оно уже идёт
            if (demoLoad)
            {
                butt_demo_load_Click(sender, e);
            }

            butt_demo_load_Click(sender, e);
        }

        private void CB_CheckedChanged(object sender, EventArgs e)
        {
            var s = sender as CheckBox;
            switch(s.Name)
            {
                case "checkBox1": timer1.Enabled = s.Checked; break;
            }
        }

        private void NUD_ValueChanged(object sender, EventArgs e)
        {
            var s = sender as NumericUpDown;
            switch (s.Name)
            {
                case "nud_Auto_Interval": timer1.Interval = (int)s.Value; break;
            }
        }

        // #####################################################

        private void Create_WorkSpace(int Size, double Step)
        {
            workSize = Size;
            workStep = Step; // сразу переводим в секунды
            workSpace = new double[Size];
            workDiscr = (Size - 1) / ((Step * Size) - (Step * 0));
        }

        private void Plot_Update()
        {
            if (workSpace == null) return;

            if (sampleForm != null)
            {
                sampleForm.Update_Plot(workStep, workSpace);
            }

            if (fftAmplForm != null || fftPhaseForm != null || fftGuillotForm != null || spectrogramForm != null)
            {
                // вычисление спектра
                var spectre = Fourie.FFT(workSpace);
                //var spectre = Fourier(workSpace);
                double[] fft_X = new double[workSize / 2];
                double[] fft_ampl = spectre.Item1;
                double[] fft_phase = spectre.Item2;
                for (int i = 0; i < workSize / 2; i++)
                {
                    fft_X[i] = i * (workDiscr / workSize) * 1000;  // герцы
                    //fft_X[i] = i * (workDiscr / workSize);       // герцы
                    //fft_X[i] = 2 * Math.PI * (i * (workDiscr / workSize));  // omega
                }

                if (fftAmplForm != null)
                {
                    fftAmplForm.Update_Plot(fft_X, fft_ampl);
                }

                if (fftPhaseForm != null)
                {
                    fftPhaseForm.Update_Plot(fft_X, fft_phase);
                }

                if (fftGuillotForm != null)
                {
                    fftGuillotForm.Update_Plot(fft_X, fft_ampl);
                }

                if (spectrogramForm != null)
                {
                    spectrogramForm.Update_Plot(fft_X, fft_ampl);
                }
            }

        }

        // #####################################################

        static private double[] Gen_sin(int num, double step, double A, double omega, double Ph)
        {
            double[] Y = new double[num];

            for (int t = 0; t < num; t++)
            {
                //Y[t] += A * Math.Sin(2 * Math.PI * (discr * t) * Math.Pow(F, -1) + Ph);
                Y[t] += A * Math.Sin(omega * (step * t) + Ph);
            }

            return Y;
        }

        // #####################################################


        // Нормализация по мин макс
        public double[] MinMax_Scale(double [] data, double scaleLine, bool minControl = false)
        {
            double[] buf = new double[data.Length];
            data.CopyTo(buf, 0);

            double x_max = buf.Max();
            if (scaleLine != 0 && x_max < scaleLine)
            {
                x_max = scaleLine;
            }
            double x_min = buf.Min();
            if (minControl && scaleLine != 0 && x_min > -scaleLine)
            {
                x_min = -scaleLine;
            }
            double divider = x_max - x_min;

            for (int i = 0; i< buf.Length; i++)
            {
                buf[i] = divider != 0 ? (buf[i] - x_min) / divider : 0;
            }
            return buf;
        }

        //  
        public bool[,] Guillotine(double[] x, double[] y, double stepX, double stepY, double scale, double maxX = 10000)
        {
            double maxAmp = y.Max();
            double maxHz = x[Array.IndexOf(y, maxAmp)];

            int height = (int)(1 / stepY) + 1;      // высота
            //int width = (int)(maxX / stepX);    // ширина
            int width = (int)(10 / stepX) + 1;    // ширина
            bool[,] result = new bool[height, width];

            double[] scale_Y = MinMax_Scale(y, scale);

            for (int i = 0; i < x.Length; i++)
            {
                if (x[i] > maxX) continue;

                int h = (int)(scale_Y[i] / stepY);
                //int w = (int)(x[i] / stepX);
                int w = (int)((x[i] / maxHz) / stepX);

                if (w >= width) continue;

                result[h, w] = true;

                if (h > 0)
                {
                    for (int j = h; j >= 0; j--)
                    {
                        result[j, w] = true;
                    }
                }

            }

            return result;
        }


        public List<bool[]> Guillotine_2(double[] x, double[] y, double stepX, double stepY)
        {
            List<bool[]> result = new List<bool[]>();
            List<int[]> ind = new List<int[]>();

            double maxAmp = y.Max();
            double maxHz = x[Array.IndexOf(y, maxAmp)];

            for (int i = 9; i >= 0; i--)
            {
                double val_up = (i + 1) * maxAmp * stepY;
                double val_dn = i * maxAmp * stepY;
                //var ii = y.Where(t => t >= val_dn && t < val_up);
                var ii = y.Select((item, index) => new { Item = item, Index = index }).Where(t => t.Item >= val_dn && t.Item <= val_up).Select(t => t.Index);
                ind.Add(ii.ToArray());
            }



            return result;
        }

        private void dataFunc_RowsRemoved(object sender, DataGridViewRowsRemovedEventArgs e)
        {
            if (funcs.Count > 0)
            {
                int ind = e.RowIndex;
                for (int i = 0; i < workSize; i++)
                {
                    workSpace[i] -= funcs[ind][i];
                }
                funcs.RemoveAt(ind);

                if (funcs.Count == 0)
                {
                    for (int i = 0; i < workSize; i++)
                    {
                        workSpace[i] = 0;
                    }
                }

                Plot_Update();
            }
        }


        private void button1_Click(object sender, EventArgs e)
        {
            //var serverUri = new Uri("rtsp://rtsp.streamcoders.com/sample.mp4");
            var serverUri = new Uri("rtsp://192.168.1.110:558/");
            var credentials = new NetworkCredential("admin", "123456");

            var connectionParameters = new ConnectionParameters(serverUri, credentials);
            var cancellationTokenSource = new CancellationTokenSource();

            Task connectTask = ConnectAsync(connectionParameters, cancellationTokenSource.Token);

            Console.WriteLine("Press any key to cancel");
            Console.ReadLine();

            //cancellationTokenSource.Cancel();

            Console.WriteLine("Canceling");
            //connectTask.Wait(CancellationToken.None);
        }
        private static async Task ConnectAsync(ConnectionParameters connectionParameters, CancellationToken token)
        {
            try
            {
                TimeSpan delay = TimeSpan.FromSeconds(5);

                using (var rtspClient = new RtspClient(connectionParameters))
                {
                    //rtspClient.FrameReceived += (sender, frame) => Console.WriteLine($"New frame {frame.Timestamp}: {frame.GetType().Name}");
                    rtspClient.FrameReceived += TestFrame;

                    while (true)
                    {
                        Console.WriteLine("Connecting...");

                        try
                        {
                            await rtspClient.ConnectAsync(token);
                        }
                        catch (OperationCanceledException)
                        {
                            return;
                        }
                        catch (RtspClientException e)
                        {
                            Console.WriteLine(e.ToString());
                            await Task.Delay(delay, token);
                            continue;
                        }

                        Console.WriteLine("Connected.");

                        try
                        {
                            await rtspClient.ReceiveAsync(token);
                        }
                        catch (OperationCanceledException)
                        {
                            return;
                        }
                        catch (RtspClientException e)
                        {
                            Console.WriteLine(e.ToString());
                            await Task.Delay(delay, token);
                        }
                    }
                }
            }
            catch (OperationCanceledException)
            {
            }
        }

        private static void TestFrame(object sender, RawFrame frame)
        {
            Console.WriteLine($"New frame {frame.Timestamp}: {frame.GetType().Name}");
        }
    }

    [Serializable]
    public struct Demo
    {
        public double[,] frames;

        public int frameSize;
        public int frameNums;
        public int frameSelect;
        public double step;
        public double discr;

        public Demo (int FrameNums, int FrameSize, double Step, double Discr)
        {
            frames = new double[FrameNums, FrameSize];

            frameSize = FrameSize;
            frameNums = FrameNums;
            step = Step;
            discr = Discr;

            frameSelect = 0;
        }

        // Вернуть индекс предыдущего фрейма
        public int Previous()
        {
            frameSelect--;
            if (frameSelect < 0)
            {
                frameSelect = frameNums-1;
            }
            return frameSelect;
        }
        
        // Вернуть индекс следующего фрейма
        public int Next()
        {
            frameSelect++;
            if (frameSelect >= frameNums)
            {
                frameSelect = 0;
            }
            return frameSelect;
        }
    }
}

/*
    void waveIn_DataAvailable(object sender, WaveInEventArgs e)
    {
        if (InvokeRequired)
        {
            BeginInvoke(new EventHandler<WaveInEventArgs>(waveIn_DataAvailable), sender, e);
        }
        else
        {
            //Записываем данные из буфера в файл
            micro.Write_buffer(e.Buffer, e.BytesRecorded);
        }
    }
*/
