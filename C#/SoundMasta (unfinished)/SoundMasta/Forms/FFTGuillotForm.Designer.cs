namespace SoundMasta.Forms
{
    partial class FFTGuillotForm
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
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.lb_maxY = new System.Windows.Forms.Label();
            this.lb_maxX = new System.Windows.Forms.Label();
            this.nud_scale = new System.Windows.Forms.NumericUpDown();
            this.nud_stepY = new System.Windows.Forms.NumericUpDown();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.numericUpDown1 = new System.Windows.Forms.NumericUpDown();
            this.nud_stepX = new System.Windows.Forms.NumericUpDown();
            this.label4 = new System.Windows.Forms.Label();
            this.plot = new OxyPlot.WindowsForms.PlotView();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.nud_scale)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nud_stepY)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.nud_stepX)).BeginInit();
            this.SuspendLayout();
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
            this.splitContainer1.Panel1.Controls.Add(this.label6);
            this.splitContainer1.Panel1.Controls.Add(this.label7);
            this.splitContainer1.Panel1.Controls.Add(this.lb_maxY);
            this.splitContainer1.Panel1.Controls.Add(this.lb_maxX);
            this.splitContainer1.Panel1.Controls.Add(this.nud_scale);
            this.splitContainer1.Panel1.Controls.Add(this.nud_stepY);
            this.splitContainer1.Panel1.Controls.Add(this.label2);
            this.splitContainer1.Panel1.Controls.Add(this.label1);
            this.splitContainer1.Panel1.Controls.Add(this.label3);
            this.splitContainer1.Panel1.Controls.Add(this.numericUpDown1);
            this.splitContainer1.Panel1.Controls.Add(this.nud_stepX);
            this.splitContainer1.Panel1.Controls.Add(this.label4);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.plot);
            this.splitContainer1.Size = new System.Drawing.Size(800, 450);
            this.splitContainer1.SplitterDistance = 30;
            this.splitContainer1.TabIndex = 4;
            // 
            // label6
            // 
            this.label6.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.label6.BackColor = System.Drawing.SystemColors.Control;
            this.label6.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label6.Location = new System.Drawing.Point(727, 4);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(70, 20);
            this.label6.TabIndex = 18;
            this.label6.Text = "FS =";
            this.label6.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // label7
            // 
            this.label7.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.label7.BackColor = System.Drawing.SystemColors.Control;
            this.label7.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label7.Location = new System.Drawing.Point(651, 4);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(70, 20);
            this.label7.TabIndex = 17;
            this.label7.Text = "W =";
            this.label7.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // lb_maxY
            // 
            this.lb_maxY.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.lb_maxY.BackColor = System.Drawing.SystemColors.Control;
            this.lb_maxY.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lb_maxY.Location = new System.Drawing.Point(575, 4);
            this.lb_maxY.Name = "lb_maxY";
            this.lb_maxY.Size = new System.Drawing.Size(70, 20);
            this.lb_maxY.TabIndex = 16;
            this.lb_maxY.Text = "FM = ";
            this.lb_maxY.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // lb_maxX
            // 
            this.lb_maxX.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.lb_maxX.BackColor = System.Drawing.SystemColors.Control;
            this.lb_maxX.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.lb_maxX.Location = new System.Drawing.Point(499, 4);
            this.lb_maxX.Name = "lb_maxX";
            this.lb_maxX.Size = new System.Drawing.Size(70, 20);
            this.lb_maxX.TabIndex = 15;
            this.lb_maxX.Text = "SM =";
            this.lb_maxX.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // nud_scale
            // 
            this.nud_scale.DecimalPlaces = 4;
            this.nud_scale.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.nud_scale.Location = new System.Drawing.Point(3, 4);
            this.nud_scale.Maximum = new decimal(new int[] {
            999,
            0,
            0,
            0});
            this.nud_scale.Name = "nud_scale";
            this.nud_scale.Size = new System.Drawing.Size(65, 20);
            this.nud_scale.TabIndex = 14;
            this.nud_scale.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.nud_scale.ThousandsSeparator = true;
            // 
            // nud_stepY
            // 
            this.nud_stepY.DecimalPlaces = 2;
            this.nud_stepY.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.nud_stepY.Location = new System.Drawing.Point(89, 4);
            this.nud_stepY.Maximum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.nud_stepY.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            131072});
            this.nud_stepY.Name = "nud_stepY";
            this.nud_stepY.Size = new System.Drawing.Size(47, 20);
            this.nud_stepY.TabIndex = 9;
            this.nud_stepY.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.nud_stepY.ThousandsSeparator = true;
            this.nud_stepY.Value = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.SystemColors.Control;
            this.label2.Location = new System.Drawing.Point(74, 8);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(14, 13);
            this.label2.TabIndex = 11;
            this.label2.Text = "Y";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BackColor = System.Drawing.SystemColors.Control;
            this.label1.Location = new System.Drawing.Point(212, 8);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(42, 13);
            this.label1.TabIndex = 12;
            this.label1.Text = "max Hz";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.BackColor = System.Drawing.SystemColors.Control;
            this.label3.Location = new System.Drawing.Point(142, 8);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(14, 13);
            this.label3.TabIndex = 12;
            this.label3.Text = "X";
            // 
            // numericUpDown1
            // 
            this.numericUpDown1.Increment = new decimal(new int[] {
            1000,
            0,
            0,
            0});
            this.numericUpDown1.Location = new System.Drawing.Point(260, 4);
            this.numericUpDown1.Maximum = new decimal(new int[] {
            22000,
            0,
            0,
            0});
            this.numericUpDown1.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.numericUpDown1.Name = "numericUpDown1";
            this.numericUpDown1.Size = new System.Drawing.Size(54, 20);
            this.numericUpDown1.TabIndex = 10;
            this.numericUpDown1.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.numericUpDown1.ThousandsSeparator = true;
            this.numericUpDown1.Value = new decimal(new int[] {
            10000,
            0,
            0,
            0});
            // 
            // nud_stepX
            // 
            this.nud_stepX.DecimalPlaces = 2;
            this.nud_stepX.Increment = new decimal(new int[] {
            1,
            0,
            0,
            65536});
            this.nud_stepX.Location = new System.Drawing.Point(159, 4);
            this.nud_stepX.Maximum = new decimal(new int[] {
            1,
            0,
            0,
            0});
            this.nud_stepX.Minimum = new decimal(new int[] {
            1,
            0,
            0,
            131072});
            this.nud_stepX.Name = "nud_stepX";
            this.nud_stepX.Size = new System.Drawing.Size(47, 20);
            this.nud_stepX.TabIndex = 10;
            this.nud_stepX.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.nud_stepX.ThousandsSeparator = true;
            this.nud_stepX.Value = new decimal(new int[] {
            1,
            0,
            0,
            0});
            // 
            // label4
            // 
            this.label4.Dock = System.Windows.Forms.DockStyle.Fill;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(204)));
            this.label4.Location = new System.Drawing.Point(0, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(800, 30);
            this.label4.TabIndex = 13;
            this.label4.Text = "Фурье - Гильотина";
            this.label4.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
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
            // FFTGuillotForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.splitContainer1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.Name = "FFTGuillotForm";
            this.Text = "Гильотина";
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.nud_scale)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nud_stepY)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.nud_stepX)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.SplitContainer splitContainer1;
        private OxyPlot.WindowsForms.PlotView plot;
        private System.Windows.Forms.NumericUpDown nud_stepY;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown nud_stepX;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown numericUpDown1;
        private System.Windows.Forms.NumericUpDown nud_scale;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.Label lb_maxY;
        private System.Windows.Forms.Label lb_maxX;
    }
}