namespace SoundMasta.Forms
{
    partial class FFTAmplForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.lb_max = new System.Windows.Forms.Label();
            this.nud_scale = new System.Windows.Forms.NumericUpDown();
            this.cb_normPlot = new System.Windows.Forms.CheckBox();
            this.plot = new OxyPlot.WindowsForms.PlotView();
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.label2 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.nud_scale)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.SuspendLayout();
            // 
            // lb_max
            // 
            this.lb_max.BackColor = System.Drawing.SystemColors.Control;
            this.lb_max.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lb_max.Location = new System.Drawing.Point(135, 4);
            this.lb_max.Name = "lb_max";
            this.lb_max.Size = new System.Drawing.Size(70, 20);
            this.lb_max.TabIndex = 7;
            this.lb_max.Text = "Max =";
            this.lb_max.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // nud_scale
            // 
            this.nud_scale.DecimalPlaces = 4;
            this.nud_scale.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.nud_scale.Location = new System.Drawing.Point(64, 4);
            this.nud_scale.Maximum = new decimal(new int[] {
            999,
            0,
            0,
            0});
            this.nud_scale.Name = "nud_scale";
            this.nud_scale.Size = new System.Drawing.Size(65, 20);
            this.nud_scale.TabIndex = 2;
            this.nud_scale.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.nud_scale.ThousandsSeparator = true;
            // 
            // cb_normPlot
            // 
            this.cb_normPlot.AutoSize = true;
            this.cb_normPlot.BackColor = System.Drawing.SystemColors.Control;
            this.cb_normPlot.Location = new System.Drawing.Point(3, 7);
            this.cb_normPlot.Name = "cb_normPlot";
            this.cb_normPlot.RightToLeft = System.Windows.Forms.RightToLeft.Yes;
            this.cb_normPlot.Size = new System.Drawing.Size(57, 17);
            this.cb_normPlot.TabIndex = 2;
            this.cb_normPlot.Text = ".Норм";
            this.cb_normPlot.UseVisualStyleBackColor = false;
            this.cb_normPlot.CheckedChanged += new System.EventHandler(this.CB_normPlot_CheckedChanged);
            // 
            // plot
            // 
            this.plot.BackColor = System.Drawing.SystemColors.ControlLightLight;
            this.plot.Dock = System.Windows.Forms.DockStyle.Fill;
            this.plot.Location = new System.Drawing.Point(0, 0);
            this.plot.Name = "plot";
            this.plot.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.plot.Size = new System.Drawing.Size(800, 416);
            this.plot.TabIndex = 2;
            this.plot.Text = "plotView1";
            this.plot.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.plot.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.plot.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // splitContainer1
            // 
            this.splitContainer1.BackColor = System.Drawing.SystemColors.Control;
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer1.IsSplitterFixed = true;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            this.splitContainer1.Orientation = System.Windows.Forms.Orientation.Horizontal;
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.BackColor = System.Drawing.SystemColors.Control;
            this.splitContainer1.Panel1.Controls.Add(this.lb_max);
            this.splitContainer1.Panel1.Controls.Add(this.nud_scale);
            this.splitContainer1.Panel1.Controls.Add(this.cb_normPlot);
            this.splitContainer1.Panel1.Controls.Add(this.label2);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.plot);
            this.splitContainer1.Size = new System.Drawing.Size(800, 450);
            this.splitContainer1.SplitterDistance = 30;
            this.splitContainer1.TabIndex = 3;
            // 
            // label2
            // 
            this.label2.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.label2.Location = new System.Drawing.Point(0, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(800, 30);
            this.label2.TabIndex = 9;
            this.label2.Text = "Фурье - Амплитуды";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // FFTAmplForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.splitContainer1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FFTAmplForm";
            this.Text = "Фурье - Амплитуды";
            ((System.ComponentModel.ISupportInitialize)(this.nud_scale)).EndInit();
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label lb_max;
        private System.Windows.Forms.NumericUpDown nud_scale;
        private System.Windows.Forms.CheckBox cb_normPlot;
        private OxyPlot.WindowsForms.PlotView plot;
        private System.Windows.Forms.SplitContainer splitContainer1;
        private System.Windows.Forms.Label label2;
    }
}