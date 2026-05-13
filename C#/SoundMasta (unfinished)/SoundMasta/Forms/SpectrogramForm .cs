using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using OxyPlot;
using OxyPlot.Axes;
using OxyPlot.Series;

namespace SoundMasta.Forms
{
    public partial class SpectrogramForm : Form
    {
        MainForm main;
        double[] scaleBuf = new double[] { 1.10, 0 };
        Queue<double[]> specBuf = new Queue<double[]>();
        int specMax = 100;

        public SpectrogramForm(MainForm M)
        {
            InitializeComponent();

            main = M;
            plot.Model = Prepare_Plot();
        }

        private PlotModel Prepare_Plot()
        {
            PlotModel model = new PlotModel();
            model.Axes.Add(new LinearAxis
            {
                Position = AxisPosition.Bottom,
                MajorGridlineColor = OxyColors.Black,
                MajorGridlineStyle = LineStyle.Automatic,
                Maximum = 10000,
                Title = "Hz",
                FontSize = 20,
            });
            model.Axes.Add(new LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineColor = OxyColors.Black,
                MajorGridlineStyle = LineStyle.Automatic,
                Minimum = 0,
                Maximum = 1,
                //Title = "Амплитуда"
                FontSize = 20,
            });

            //model.Series.Add(new LineSeries
            //{
            //    Title = "Амплитуды",
            //    StrokeThickness = 5,
            //    MarkerSize = 5,
            //    MarkerType = MarkerType.Diamond,
            //});

            model.Series.Add(new ScatterSeries
            {
                Title = "Сеть",
                MarkerSize = 5,
                MarkerType = MarkerType.Diamond,
                MarkerStroke = OxyColor.FromRgb(200, 100, 100)
            });

            return model;
        }

        private void CB_normPlot_CheckedChanged(object sender, EventArgs e)
        {
            Axis ax = plot.Model.Axes[1];
            double buf = ax.Maximum;
            ax.Maximum = scaleBuf[0];
            scaleBuf[0] = buf;
            buf = ax.Minimum;
            ax.Minimum = scaleBuf[1];
            scaleBuf[1] = buf;
        }

        // #####################################################

        public void Update_Plot(double[] x, double[] y)
        {
            lb_max.Text = "Max = " + Math.Round(y.Max(), 2);

            //double[] buf_y = cb_normPlot.Checked ? main.MinMax_Scale(y, (double)nud_scale.Value) : y;
            double[] buf_y = main.MinMax_Scale(y, (double)nud_scale.Value);

            Add_Frame(buf_y);

            ScatterSeries series = plot.Model.Series[0] as ScatterSeries;
            series.Points.Clear();

            double i = 0;
            foreach (var item in specBuf)
            {
                for (int j = 0; j < x.Length; j++)
                {
                    //series.Points.Add(new ScatterPoint(x[j], specBuf[i], buf_y[j] * 5));
                    series.Points.Add(new ScatterPoint(x[j], i, item[j] * 5));
                }
                i+= 0.01;
            }

            plot.InvalidatePlot(true);
        }

        private void Add_Frame(double[] frame)
        {
            if (specBuf.Count >= specMax)
            {
                specBuf.Dequeue();
            }

            specBuf.Enqueue(frame);
        }
    }
}
