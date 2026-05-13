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
    public partial class SampleForm : Form
    {
        MainForm main;
        double[] scaleBuf = new double[] { 1.05, -0.05};

        public SampleForm(MainForm M)
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
                Title = "ms"
            });
            model.Axes.Add(new LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineColor = OxyColors.Black,
                MajorGridlineStyle = LineStyle.Automatic,
                Minimum = -5,
                Maximum = 5,
            });

            model.Series.Add(new LineSeries { Title = "Сигнал", StrokeThickness = 1, MarkerType = MarkerType.Diamond });

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

        public void Update_Plot(double workStep, double[] sample)
        {
            lb_max.Text = "Max = " + Math.Round(sample.Max(), 2);

            double[] sample_Y = cb_normPlot.Checked ? main.MinMax_Scale(sample, (double)nud_scale.Value, true) : sample;

            LineSeries series = plot.Model.Series[0] as LineSeries;
            series.Points.Clear();
            for (int i = 0; i < sample.Length; i++)
            {
                double sample_x = i * workStep;
                series.Points.Add(new DataPoint(sample_x, sample_Y[i]));
            }

            plot.InvalidatePlot(true);
        }


    }
}
