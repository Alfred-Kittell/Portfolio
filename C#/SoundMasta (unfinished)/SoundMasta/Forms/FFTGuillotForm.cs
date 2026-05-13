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
    public partial class FFTGuillotForm : Form
    {
        MainForm main;
        double[] scaleBuf = new double[] { 1.10, -0.05 };

        public FFTGuillotForm(MainForm M)
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
                Minimum = -1,
                Maximum = 10,
                Title = "Hz"
            });
            model.Axes.Add(new LinearAxis
            {
                Position = AxisPosition.Left,
                MajorGridlineColor = OxyColors.Black,
                MajorGridlineStyle = LineStyle.Automatic,
                Minimum = -0.05,
                Maximum = 1.10,
                //Title = "Амплитуда"
            });

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
            double scale = (double)nud_scale.Value;
            double stepX = (double)nud_stepX.Value;
            double stepY = (double)nud_stepY.Value;
            double maxX = (double)numericUpDown1.Value;

            double maxAmp = y.Max();
            double maxHz = x[Array.IndexOf(y, maxAmp)];

            lb_maxY.Text = "SM = " + Math.Round(maxAmp, 2);
            lb_maxX.Text = "FM = " + Math.Round(maxHz, 2);


            ScatterSeries series = plot.Model.Series[0] as ScatterSeries;
            series.Points.Clear();
            //List<bool[]> guill = main.Guillotine(x, y, (double)nud_stepY.Value, (double)nud_stepX.Value);
            bool[,] guill = main.Guillotine(x, y, stepX, stepY, scale, maxX);

            for (int i = 0; i < guill.GetLength(0); i++)
            {
                for (int j = 0; j < guill.GetLength(1); j++)
                {
                    if (!guill[i,j]) continue;

                    double buf_y = i * stepY;
                    double buf_x = j * stepX;
                    //double buf_x = (j * stepX) / maxHz;
                        
                    series.Points.Add(new ScatterPoint(buf_x, buf_y));
                }
            }


            //plot.Model.Axes[0].Minimum = (-1 * stepX) / maxHz;
            //plot.Model.Axes[0].Maximum = (guill.GetLength(1) * stepX) / maxHz;
            plot.InvalidatePlot(true);
        }

    }
}
